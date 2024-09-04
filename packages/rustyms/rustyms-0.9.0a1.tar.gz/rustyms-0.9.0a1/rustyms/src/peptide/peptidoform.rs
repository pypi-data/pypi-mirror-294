use std::{collections::HashSet, fmt::Write};

use itertools::Itertools;
use serde::{Deserialize, Serialize};

use crate::{
    modification::{CrossLinkName, CrossLinkSide, RulePossible, SimpleModification},
    peptide::Linked,
    system::usize::Charge,
    Fragment, LinearPeptide, Model, MolecularFormula, Multi, MultiChemical, SequencePosition,
};
/// A single peptidoform, can contain multiple linear peptides
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Debug, Serialize, Deserialize, Hash)]
pub struct Peptidoform(pub(crate) Vec<LinearPeptide<Linked>>);

impl MultiChemical for Peptidoform {
    /// Gives all possible formulas for this peptidoform (including breakage of cross-links that can break).
    /// Assumes all peptides in this peptidoform are connected.
    /// If there are no peptides in this peptidoform it returns [`Multi::default`].
    fn formulas(
        &self,
        _sequence_index: SequencePosition,
        _peptide_index: usize,
    ) -> Multi<MolecularFormula> {
        self.0
            .first()
            .map(|p| p.formulas(0, &self.0, &[], &mut Vec::new(), true))
            .unwrap_or_default()
    }
}

impl Peptidoform {
    /// Gives all possible formulas for this peptidoform (including breakage of cross-links that can break).
    /// Assumes all peptides in this peptidoform are connected.
    /// If there are no peptides in this peptidoform it returns [`Multi::default`].
    pub(super) fn formulas_inner(&self) -> (Multi<MolecularFormula>, HashSet<CrossLinkName>) {
        self.0
            .first()
            .map(|p| p.formulas_inner(0, &self.0, &[], &mut Vec::new(), true))
            .unwrap_or_default()
    }

    /// Generate the theoretical fragments for this peptide collection.
    pub fn generate_theoretical_fragments(
        &self,
        max_charge: Charge,
        model: &Model,
        peptidoform_index: usize,
    ) -> Vec<Fragment> {
        let mut base = Vec::new();
        for (index, peptide) in self.peptides().iter().enumerate() {
            base.extend(peptide.generate_theoretical_fragments_inner(
                max_charge,
                model,
                peptidoform_index,
                index,
                &self.0,
            ));
        }
        base
    }

    /// Assume there is exactly one peptide in this collection.
    pub fn singular(mut self) -> Option<LinearPeptide<Linked>> {
        if self.0.len() == 1 {
            self.0.pop()
        } else {
            None
        }
    }

    /// Get all peptides making up this `Peptidoform`
    pub fn peptides(&self) -> &[LinearPeptide<Linked>] {
        &self.0
    }

    /// Add a cross-link to this peptidoform and check if it is placed according to its placement rules.
    /// The positions are first the peptide index and second the sequence index.
    pub fn add_cross_link(
        &mut self,
        position_1: (usize, SequencePosition),
        position_2: (usize, SequencePosition),
        linker: SimpleModification,
        name: CrossLinkName,
    ) -> bool {
        let pos_1 = self.0.get(position_1.0).map(|seq| &seq[position_1.1]);
        let pos_2 = self.0.get(position_2.0).map(|seq| &seq[position_2.1]);
        if let (Some(pos_1), Some(pos_2)) = (pos_1, pos_2) {
            let left = linker.is_possible(pos_1, position_1.1);
            let right = linker.is_possible(pos_2, position_1.1);
            let specificity = if matches!(
                linker,
                SimpleModification::Formula(_)
                    | SimpleModification::Glycan(_)
                    | SimpleModification::GlycanStructure(_)
                    | SimpleModification::Gno(_, _)
                    | SimpleModification::Mass(_)
            ) {
                Some((
                    CrossLinkSide::Symmetric(HashSet::default()),
                    CrossLinkSide::Symmetric(HashSet::default()),
                ))
            } else {
                match (left, right) {
                    (RulePossible::Symmetric(a), RulePossible::Symmetric(b)) => {
                        let intersection: HashSet<usize> = a.intersection(&b).copied().collect();
                        if intersection.is_empty() {
                            None
                        } else {
                            Some((
                                CrossLinkSide::Symmetric(intersection.clone()),
                                CrossLinkSide::Symmetric(intersection),
                            ))
                        }
                    }
                    (
                        RulePossible::AsymmetricLeft(a),
                        RulePossible::AsymmetricRight(b) | RulePossible::Symmetric(b),
                    ) => {
                        let intersection: HashSet<usize> = a.intersection(&b).copied().collect();
                        if intersection.is_empty() {
                            None
                        } else {
                            Some((
                                CrossLinkSide::Left(intersection.clone()),
                                CrossLinkSide::Right(intersection),
                            ))
                        }
                    }
                    (
                        RulePossible::AsymmetricRight(a),
                        RulePossible::AsymmetricLeft(b) | RulePossible::Symmetric(b),
                    ) => {
                        let intersection: HashSet<usize> = a.intersection(&b).copied().collect();
                        if intersection.is_empty() {
                            None
                        } else {
                            Some((
                                CrossLinkSide::Right(intersection.clone()),
                                CrossLinkSide::Left(intersection),
                            ))
                        }
                    }
                    _ => None,
                }
            };
            if let Some((left, right)) = specificity {
                self.0[position_1.0].add_modification(
                    position_1.1,
                    crate::Modification::CrossLink {
                        peptide: position_2.0,
                        sequence_index: position_2.1,
                        linker: linker.clone(),
                        name: name.clone(),
                        side: left,
                    },
                );
                self.0[position_2.0].add_modification(
                    position_2.1,
                    crate::Modification::CrossLink {
                        peptide: position_1.0,
                        sequence_index: position_1.1,
                        linker,
                        name,
                        side: right,
                    },
                );
                true
            } else {
                false
            }
        } else {
            false
        }
    }

    /// Display this peptidoform.
    /// `specification_compliant` Displays this peptidoform either normalised to the internal representation or as fully spec compliant ProForma
    /// (no glycan structure or custom modifications).
    /// # Panics
    /// When some peptides do not have the same global isotope modifications.
    /// # Errors
    /// If the underlying formatter errors.
    pub fn display(
        &self,
        f: &mut impl Write,
        show_global_mods: bool,
        specification_compliant: bool,
    ) -> std::fmt::Result {
        if show_global_mods {
            let global_equal = self
                .peptides()
                .iter()
                .map(|p| &p.global)
                .tuple_windows()
                .all(|(a, b)| a == b);
            assert!(global_equal, "Not all global isotope modifications on all peptides on this peptidoform are identical");
            let empty = Vec::new();
            let global = self.peptides().first().map_or(&empty, |p| &p.global);
            for (element, isotope) in global {
                write!(
                    f,
                    "<{}{}>",
                    isotope.map(|i| i.to_string()).unwrap_or_default(),
                    element
                )?;
            }
        }

        let mut first = true;
        for p in self.peptides() {
            if !first {
                write!(f, "//")?;
            }
            p.display(f, false, specification_compliant)?;
            first = false;
        }
        Ok(())
    }
}

impl std::fmt::Display for Peptidoform {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.display(f, true, true)
    }
}
