use itertools::Itertools;
use std::collections::HashMap;

use crate::{
    error::{Context, CustomError},
    modification::{AmbiguousModification, CrossLinkName, SimpleModification},
    placement_rule::Position,
    LinearPeptide, Linked, Modification, Peptidoform, SequencePosition,
};

use super::GlobalModification;

/// Validate all cross links
/// # Errors
/// If there is a cross link with more then 2 locations. Or if there never is a definition for this cross link.
/// Or if there are peptides that cannot be reached from the first peptide.
pub fn cross_links(
    peptides: Vec<LinearPeptide<Linked>>,
    cross_links_found: HashMap<usize, Vec<(usize, SequencePosition)>>,
    cross_link_lookup: &[(CrossLinkName, Option<SimpleModification>)],
    line: &str,
) -> Result<Peptidoform, CustomError> {
    let mut peptidoform = Peptidoform(peptides);
    for (id, locations) in cross_links_found {
        let definition = &cross_link_lookup[id];
        if let Some(linker) = &definition.1 {
            match locations.len() {
                0 => {return Err(CustomError::error(
                    "Invalid cross-link",
                    format!("The cross-link named '{}' has no listed locations, this is an internal error please report this", definition.0),
                    Context::full_line(0, line),
                ))},
                1 => (), // TODO: assumed that the modification is already placed so this works out fine (it is not)
                2 => {
                    if !peptidoform.add_cross_link(locations[0], locations[1], linker.clone(), definition.0.clone()) {
                        return Err(CustomError::error(
                            "Invalid cross-link",
                            format!("The cross-link named '{}' cannot be placed according to its location specificities", definition.0),
                            Context::full_line(0, line),
                        ))
                    }
                },
                _ => {return Err(CustomError::error(
                    "Invalid cross-link",
                    format!("The cross-link named '{}' has more than 2 attachment locations, only cross-links spanning two locations are allowed", definition.0),
                    Context::full_line(0, line),
                ))}
            }
        } else {
            let (c, name, description) = if definition.0 == CrossLinkName::Branch {
                ("MOD", "00134", " N6-glycyl-L-lysine")
            } else {
                ("X", "DSS", "")
            };
            return Err(CustomError::error(
                "Invalid cross-link",
                format!("The cross-link named '{0}' is never defined, for example for {name}{description} define it like: '[{c}:{name}{0}]'", definition.0),
                Context::full_line(0, line),
            ));
        }
    }

    // Check if all peptides can be reached from the first one
    let mut found_peptides = Vec::new();
    let mut stack = vec![0];

    while let Some(index) = stack.pop() {
        found_peptides.push(index);
        if let Some(Modification::CrossLink { peptide, .. }) = &peptidoform.0[index].n_term {
            if !found_peptides.contains(peptide) && !stack.contains(peptide) {
                stack.push(*peptide);
            }
        }
        if let Some(Modification::CrossLink { peptide, .. }) = &peptidoform.0[index].c_term {
            if !found_peptides.contains(peptide) && !stack.contains(peptide) {
                stack.push(*peptide);
            }
        }
        for seq in &peptidoform.0[index].sequence {
            for modification in &seq.modifications {
                if let Modification::CrossLink { peptide, .. } = modification {
                    if !found_peptides.contains(peptide) && !stack.contains(peptide) {
                        stack.push(*peptide);
                    }
                }
            }
        }
    }

    if found_peptides.len() != peptidoform.peptides().len() {
        return Err(CustomError::error(
            "Unconnected peptidoform",
            "Not all peptides in this peptidoform are connected with cross-links or branches, if separate peptides were intended use the chimeric notation `+` instead of the peptidoform notation `//`.",
             Context::full_line(0, line),
        ));
    }

    Ok(peptidoform)
}

impl LinearPeptide<Linked> {
    /// Apply a global modification if this is a global isotope modification with invalid isotopes it returns false
    #[must_use]
    pub(super) fn apply_global_modifications(
        &mut self,
        global_modifications: &[GlobalModification],
    ) -> bool {
        for modification in global_modifications {
            match modification {
                GlobalModification::Fixed(pos, aa, modification) => {
                    for (_, seq) in self.sequence.iter_mut().enumerate().filter(|(index, seq)| {
                        pos.is_possible(SequencePosition::Index(*index))
                            && aa.map_or(true, |aa| aa == seq.aminoacid)
                            && modification
                                .is_possible(seq, SequencePosition::Index(*index))
                                .possible()
                    }) {
                        match pos {
                            Position::Anywhere => {
                                seq.modifications.push(modification.clone().into());
                            }
                            Position::AnyNTerm | Position::ProteinNTerm => {
                                self.n_term = Some(Modification::Simple(modification.clone()));
                            }
                            Position::AnyCTerm | Position::ProteinCTerm => {
                                self.c_term = Some(Modification::Simple(modification.clone()));
                            }
                        }
                    }
                }
                GlobalModification::Isotope(el, isotope) if el.is_valid(*isotope) => {
                    self.global.push((*el, *isotope));
                }
                GlobalModification::Isotope(..) => return false,
            }
        }
        true
    }

    /// Place all global unknown positions at all possible locations as ambiguous modifications
    /// # Errors
    /// When a mod cannot be placed anywhere
    pub(super) fn apply_unknown_position_modification(
        &mut self,
        unknown_position_modifications: &[SimpleModification],
    ) -> Result<(), CustomError> {
        for (unknown_mod_index, modification) in unknown_position_modifications.iter().enumerate() {
            let id = self.ambiguous_modifications.len();
            let length = self.len();
            let positions = (0..length)
                .filter(|i| {
                    if modification
                        .is_possible(&self.sequence[*i], SequencePosition::Index(*i))
                        .possible()
                    {
                        self.sequence[*i]
                            .possible_modifications
                            .push(AmbiguousModification {
                                id,
                                modification: modification.clone(),
                                localisation_score: None,
                                group: format!("u{unknown_mod_index}"),
                                preferred: false,
                            });
                        true
                    } else {
                        false
                    }
                })
                .collect_vec();
            if positions.is_empty() {
                return Err(CustomError::error("Modification of unknown position cannot be placed", "There is no position where this modification can be placed based on the placement rules in the database.", Context::show(modification)));
            }
            self.ambiguous_modifications.push(positions);
        }
        Ok(())
    }

    /// Place all ranged unknown positions at all possible locations as ambiguous modifications
    /// # Errors
    /// When a mod cannot be placed anywhere
    /// # Panics
    /// It panics when information for an ambiguous modification is missing (name/mod).
    pub(super) fn apply_ranged_unknown_position_modification(
        &mut self,
        ranged_unknown_position_modifications: &[(usize, usize, SimpleModification)],
        mut start_ambiguous_index: usize,
        mut start_ambiguous_group_id: usize,
    ) -> Result<(), CustomError> {
        for (start, end, modification) in ranged_unknown_position_modifications {
            #[allow(clippy::unnecessary_filter_map)]
            // Side effects so the lint does not apply here
            let positions = (*start..=*end)
                .filter_map(|i| {
                    if modification
                        .is_possible(&self.sequence[i], SequencePosition::Index(i))
                        .possible()
                    {
                        self.sequence[i]
                            .possible_modifications
                            .push(AmbiguousModification {
                                id: start_ambiguous_index,
                                modification: modification.clone(),
                                localisation_score: None,
                                group: format!("u{start_ambiguous_group_id}"),
                                preferred: false,
                            });
                        Some(i)
                    } else {
                        None
                    }
                })
                .collect_vec();
            if positions.is_empty() {
                return Err(CustomError::error("Modification of unknown position on a range cannot be placed", "There is no position where this modification can be placed based on the placement rules in the database.", Context::show(modification)));
            }
            self.ambiguous_modifications.push(positions);
            start_ambiguous_index += 1;
            start_ambiguous_group_id += 1;
        }
        Ok(())
    }
}

impl<T> LinearPeptide<T> {
    /// # Errors
    /// If a modification rule is broken it returns an error.
    pub(crate) fn enforce_modification_rules(&self) -> Result<(), CustomError> {
        for (position, seq) in self.iter(..) {
            seq.enforce_modification_rules(position.sequence_index)?;
        }
        Ok(())
    }
}
