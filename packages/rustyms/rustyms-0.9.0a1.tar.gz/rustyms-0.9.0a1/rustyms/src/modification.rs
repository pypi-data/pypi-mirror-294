//! Handle modification related issues, access provided if you want to dive deeply into modifications in your own code.

use itertools::Itertools;
use ordered_float::OrderedFloat;
use serde::{Deserialize, Serialize};

use std::{
    cmp::Ordering,
    collections::HashSet,
    fmt::{Display, Write},
};

use crate::{
    glycan::{GlycanStructure, MonoSaccharide},
    molecular_charge::CachedCharge,
    ontologies::CustomDatabase,
    peptide::Linked,
    placement_rule::PlacementRule,
    system::{Mass, OrderedMass},
    AmbiguousLabel, AminoAcid, Chemical, DiagnosticIon, Fragment, LinearPeptide, Model,
    MolecularFormula, Multi, NeutralLoss, SequenceElement, SequencePosition, Tolerance,
    WithinTolerance,
};

include!("shared/modification.rs");

impl ModificationId {
    /// Get the accession number name for the ontology
    pub fn url(&self) -> Option<String> {
        match self.ontology {
            Ontology::Unimod => Some(format!(
                "https://www.unimod.org/modifications_view.php?editid1={}",
                self.id
            )),
            Ontology::Psimod => Some(format!(
                "https://ontobee.org/ontology/MOD?iri=http://purl.obolibrary.org/obo/MOD_{:05}",
                self.id
            )),
            Ontology::Gnome => Some(format!(
                "https://gnome.glyomics.org/StructureBrowser.html?focus={}",
                self.name
            )),
            Ontology::Resid => Some(format!(
                "https://proteininformationresource.org/cgi-bin/resid?id=AA{:04}",
                self.id
            )),
            Ontology::Xlmod | Ontology::Custom => None,
        }
    }
}

impl Chemical for SimpleModification {
    fn formula(&self, sequence_index: SequencePosition, peptide_index: usize) -> MolecularFormula {
        match self {
            Self::Mass(m) => MolecularFormula::with_additional_mass(m.value),
            Self::Formula(elements) => elements.clone(),
            Self::Glycan(monosaccharides) => monosaccharides
                .iter()
                .fold(MolecularFormula::default(), |acc, i| {
                    acc + i.0.formula(sequence_index, peptide_index) * i.1 as i32
                }),
            Self::GlycanStructure(glycan) | Self::Gno(GnoComposition::Structure(glycan), _) => {
                glycan.formula(sequence_index, peptide_index)
            }
            Self::Database { formula, .. } | Self::Linker { formula, .. } => formula.clone(),
            Self::Gno(GnoComposition::Mass(m), _) => {
                MolecularFormula::with_additional_mass(m.value)
            }
        }
    }
}

/// The result of checking if a modification can be placed somewhere.
#[derive(Debug, PartialEq, Eq, Serialize, Deserialize, Clone)]
pub enum RulePossible {
    /// This modification cannot be placed
    No,
    /// This modification can be placed and if it is a cross-link it can be placed on both ends
    Symmetric(HashSet<usize>),
    /// This modification can be placed and if it is a cross-link it can only be placed on the 'left' side of the cross-link
    AsymmetricLeft(HashSet<usize>),
    /// This modification can be placed and if it is a cross-link it can only be placed on the 'right' side of the cross-link
    AsymmetricRight(HashSet<usize>),
}

impl RulePossible {
    /// Flatten this into a bool, check if the rule is not [`Self::No`]
    pub fn possible(self) -> bool {
        self != Self::No
    }
}

impl std::ops::Add for RulePossible {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        match (self, rhs) {
            (Self::Symmetric(a), _) | (_, Self::Symmetric(a)) => Self::Symmetric(a),
            (Self::AsymmetricLeft(l), Self::AsymmetricRight(r))
            | (Self::AsymmetricRight(l), Self::AsymmetricLeft(r)) => {
                let overlap: HashSet<usize> = l.intersection(&r).copied().collect();
                if overlap.is_empty() {
                    Self::No
                } else {
                    Self::Symmetric(overlap)
                }
            }
            (Self::AsymmetricLeft(l), _) | (_, Self::AsymmetricLeft(l)) => Self::AsymmetricLeft(l),
            (Self::AsymmetricRight(r), _) | (_, Self::AsymmetricRight(r)) => {
                Self::AsymmetricRight(r)
            }
            _ => Self::No,
        }
    }
}

impl std::iter::Sum for RulePossible {
    fn sum<I: Iterator<Item = Self>>(iter: I) -> Self {
        iter.fold(Self::No, |acc, i| acc + i)
    }
}

impl SimpleModification {
    /// Get a url for more information on this modification. Only defined for modifications from ontologies.
    #[allow(clippy::missing_panics_doc)]
    pub fn ontology_url(&self) -> Option<String> {
        match self {
            Self::Mass(_) | Self::Formula(_) | Self::Glycan(_) | Self::GlycanStructure(_) => None,
            Self::Database { id, .. } | Self::Linker { id, .. } => id.url(),
            Self::Gno(_, name) => Some(format!(
                "https://gnome.glyomics.org/StructureBrowser.html?focus={name}",
            )),
        }
    }

    /// Check to see if this modification can be placed on the specified element
    pub fn is_possible(&self, seq: &SequenceElement, position: SequencePosition) -> RulePossible {
        match self {
            Self::Database { specificities, .. } => {
                // If any of the rules match the current situation then it can be placed
                let matching: HashSet<usize> = specificities
                    .iter()
                    .enumerate()
                    .filter_map(|(index, (rules, _, _))| {
                        PlacementRule::any_possible(rules, seq, position).then_some(index)
                    })
                    .collect();
                if matching.is_empty() {
                    RulePossible::No
                } else {
                    RulePossible::Symmetric(matching)
                }
            }
            Self::Linker { specificities, .. } => specificities
                .iter()
                .enumerate()
                .map(|(index, spec)| match spec {
                    LinkerSpecificity::Symmetric(rules, _, _) => {
                        if PlacementRule::any_possible(rules, seq, position) {
                            RulePossible::Symmetric(HashSet::from([index]))
                        } else {
                            RulePossible::No
                        }
                    }
                    LinkerSpecificity::Asymmetric((rules_left, rules_right), _, _) => {
                        let left = PlacementRule::any_possible(rules_left, seq, position);
                        let right = PlacementRule::any_possible(rules_right, seq, position);
                        if left && right {
                            RulePossible::Symmetric(HashSet::from([index]))
                        } else if left {
                            RulePossible::AsymmetricLeft(HashSet::from([index]))
                        } else if right {
                            RulePossible::AsymmetricRight(HashSet::from([index]))
                        } else {
                            RulePossible::No
                        }
                    }
                })
                .sum::<RulePossible>(),
            _ => RulePossible::Symmetric(HashSet::default()),
        }
    }

    /// Display a modification either normalised to the internal representation or as fully valid ProForma
    /// (no glycan structure or custom modifications).
    /// # Errors
    /// When the given writer errors.
    pub fn display(&self, f: &mut impl Write, specification_compliant: bool) -> std::fmt::Result {
        match self {
            Self::Mass(m) => {
                write!(f, "{:+}", m.value)?;
            }
            Self::Formula(elements) => {
                write!(f, "Formula:{}", elements.hill_notation())?;
            }
            Self::Glycan(monosaccharides) => write!(
                f,
                "Glycan:{}",
                monosaccharides
                    .iter()
                    .fold(String::new(), |acc, m| acc + &format!("{}{}", m.0, m.1))
            )?,
            Self::GlycanStructure(glycan) if specification_compliant => write!(
                f,
                "Glycan:{}|INFO:Structure:{glycan}",
                glycan
                    .composition()
                    .iter()
                    .fold(String::new(), |mut acc, (g, a)| {
                        write!(&mut acc, "{g}{a}").unwrap();
                        acc
                    })
            )?,
            Self::GlycanStructure(glycan) => write!(f, "GlycanStructure:{glycan}")?,
            Self::Database {
                formula,
                id:
                    ModificationId {
                        name,
                        ontology: Ontology::Custom,
                        ..
                    },
                ..
            } if specification_compliant => {
                write!(f, "Formula:{formula}|INFO:Custom:{name}")?;
            }
            Self::Database {
                id:
                    ModificationId {
                        name,
                        ontology: Ontology::Custom,
                        ..
                    },
                ..
            } if specification_compliant => {
                write!(f, "C:{name}")?;
            }
            Self::Database { id, .. } => {
                write!(f, "{}:{}", id.ontology.char(), id.name)?;
            }
            Self::Gno(_, name) => write!(f, "{}:{name}", Ontology::Gnome.char())?,
            Self::Linker { id, .. } => write!(f, "{}:{}", id.ontology.char(), id.name)?,
        }
        Ok(())
    }
}

impl Display for SimpleModification {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.display(f, true)
    }
}

impl From<SimpleModification> for Modification {
    fn from(value: SimpleModification) -> Self {
        Self::Simple(value)
    }
}

impl CrossLinkSide {
    /// Get all allowed placement rules with all applicable neutral losses, stubs, and diagnostic ions.
    pub(crate) fn allowed_rules(
        &self,
        linker: &SimpleModification,
    ) -> (
        Vec<NeutralLoss>,
        Vec<(MolecularFormula, MolecularFormula)>,
        Vec<DiagnosticIon>,
    ) {
        let selected_rules = match self {
            Self::Left(r) | Self::Right(r) | Self::Symmetric(r) => r,
        };
        let mut neutral = Vec::new();
        let mut stubs = Vec::new();
        let mut diagnostic = Vec::new();

        match linker {
            SimpleModification::Linker { specificities, .. } => {
                for rule in specificities
                    .iter()
                    .enumerate()
                    .filter_map(|(i, r)| selected_rules.contains(&i).then_some(r))
                {
                    match rule {
                        LinkerSpecificity::Asymmetric(_, n, d) => {
                            diagnostic.extend_from_slice(d);
                            match self {
                                Self::Left(_) => stubs.extend(n.iter().cloned()),
                                Self::Right(_) => {
                                    stubs.extend(n.iter().map(|(l, r)| (r.clone(), l.clone())));
                                }
                                Self::Symmetric(_) => stubs.extend(n.iter().flat_map(|(l, r)| {
                                    vec![(l.clone(), r.clone()), (r.clone(), l.clone())]
                                })),
                            }
                        }
                        LinkerSpecificity::Symmetric(_, n, d) => {
                            stubs.extend_from_slice(n);
                            diagnostic.extend_from_slice(d);
                        }
                    }
                }
            }
            SimpleModification::Database { specificities, .. } => {
                for rule in specificities
                    .iter()
                    .enumerate()
                    .filter_map(|(i, r)| selected_rules.contains(&i).then_some(r))
                {
                    neutral.extend_from_slice(&rule.1);
                    diagnostic.extend_from_slice(&rule.2);
                }
            }
            _ => (),
        };
        (neutral, stubs, diagnostic)
    }
}

impl Modification {
    /// Get the formula for the whole addition (or subtraction) for this modification
    pub(crate) fn formula_inner(
        &self,
        all_peptides: &[LinearPeptide<Linked>],
        visited_peptides: &[usize],
        applied_cross_links: &mut Vec<CrossLinkName>,
        allow_ms_cleavable: bool,
        sequence_index: SequencePosition,
        peptide_index: usize,
    ) -> (Multi<MolecularFormula>, HashSet<CrossLinkName>) {
        match self {
            // A linker that is not cross-linked is hydrolysed
            Self::Simple(SimpleModification::Linker { formula, .. }) => (
                (formula.clone() + molecular_formula!(H 2 O 1)).into(),
                HashSet::new(),
            ),
            Self::Simple(s) => (
                s.formula(sequence_index, peptide_index).into(),
                HashSet::new(),
            ),
            Self::CrossLink {
                peptide,
                linker,
                name,
                side,
                ..
            } => {
                let link = (!applied_cross_links.contains(name))
                    .then(|| {
                        applied_cross_links.push(name.clone());
                        linker.formula(sequence_index, peptide_index)
                    })
                    .unwrap_or_default();
                let (_, stubs, _) = side.allowed_rules(linker);

                if allow_ms_cleavable && !stubs.is_empty() {
                    let mut options: Vec<MolecularFormula> = stubs
                        .iter()
                        .map(|s| {
                            s.0.clone().with_labels(&[AmbiguousLabel::CrossLinkBroken(
                                name.clone(),
                                s.0.clone(),
                            )])
                        })
                        .unique()
                        .collect();
                    let mut seen_peptides = HashSet::from([name.clone()]);
                    options.extend_from_slice(&if visited_peptides.contains(peptide) {
                        vec![link.with_labels(&[AmbiguousLabel::CrossLinkBound(name.clone())])]
                    } else {
                        let (f, seen) = all_peptides[*peptide].formulas_inner(
                            *peptide,
                            all_peptides,
                            visited_peptides,
                            applied_cross_links,
                            false,
                        );
                        seen_peptides.extend(seen);
                        (f + link)
                            .with_labels(&[AmbiguousLabel::CrossLinkBound(name.clone())])
                            .to_vec()
                    });

                    (options.into(), seen_peptides)
                } else if visited_peptides.contains(peptide) {
                    (
                        link.with_labels(&[AmbiguousLabel::CrossLinkBound(name.clone())])
                            .into(),
                        HashSet::from([name.clone()]),
                    )
                } else {
                    let (f, mut seen) = all_peptides[*peptide].formulas_inner(
                        *peptide,
                        all_peptides,
                        visited_peptides,
                        applied_cross_links,
                        false,
                    );
                    seen.insert(name.clone());
                    (
                        (f + link).with_labels(&[AmbiguousLabel::CrossLinkBound(name.clone())]),
                        seen,
                    )
                }
            }
        }
    }

    /// Get the formula for a modification, if it is a cross linked modification only get the cross link
    pub fn formula(&self) -> MolecularFormula {
        match self {
            Self::Simple(s) => s.formula(SequencePosition::default(), 0),
            Self::CrossLink { linker, .. } => linker.formula(SequencePosition::default(), 0),
        }
    }
}

impl Modification {
    /// Check if this is a simple modification
    pub const fn simple(&self) -> Option<&SimpleModification> {
        match self {
            Self::Simple(sim) => Some(sim),
            Self::CrossLink { .. } => None,
        }
    }

    /// Check if this is a simple modification
    pub fn into_simple(self) -> Option<SimpleModification> {
        match self {
            Self::Simple(sim) => Some(sim),
            Self::CrossLink { .. } => None,
        }
    }

    /// Get a url for more information on this modification. Only defined for modifications from ontologies.
    #[allow(clippy::missing_panics_doc)]
    pub fn ontology_url(&self) -> Option<String> {
        match self {
            Self::Simple(modification) => modification.ontology_url(),
            Self::CrossLink { linker, .. } => linker.ontology_url(),
        }
    }

    /// Check to see if this modification can be placed on the specified element
    pub fn is_possible(&self, seq: &SequenceElement, position: SequencePosition) -> RulePossible {
        self.simple()
            .map_or(RulePossible::Symmetric(HashSet::new()), |s| {
                s.is_possible(seq, position)
            })
    }

    /// Generate theoretical fragments for side chains (glycans)
    pub(crate) fn generate_theoretical_fragments(
        &self,
        model: &Model,
        peptidoform_index: usize,
        peptide_index: usize,
        charge_carriers: &mut CachedCharge,
        full_formula: &Multi<MolecularFormula>,
        attachment: Option<(AminoAcid, usize)>,
    ) -> Vec<Fragment> {
        if let Self::Simple(simple) = self {
            simple.generate_theoretical_fragments(
                model,
                peptidoform_index,
                peptide_index,
                charge_carriers,
                full_formula,
                attachment,
            )
        } else {
            Vec::new()
        }
    }
}

impl SimpleModification {
    /// Search matching modification based on what modification is provided. If a mass modification is provided
    /// it returns all modifications with that mass (within the tolerance). If a formula is provided it returns
    /// all modifications with that formula. If a glycan composition is provided it returns all glycans with
    /// that composition. Otherwise it returns the modification itself.
    pub fn search(
        modification: &Self,
        tolerance: Tolerance<Mass>,
        custom_database: Option<&CustomDatabase>,
    ) -> ModificationSearchResult {
        match modification {
            Self::Mass(mass) => ModificationSearchResult::Mass(
                mass.into_inner(),
                tolerance,
                [
                    Ontology::Unimod,
                    Ontology::Psimod,
                    Ontology::Gnome,
                    Ontology::Xlmod,
                    Ontology::Custom,
                ]
                .iter()
                .flat_map(|o| {
                    o.lookup(custom_database)
                        .iter()
                        .map(|(i, n, m)| (*o, *i, n, m))
                })
                .filter(|(_, _, _, m)| {
                    tolerance.within(
                        &mass.into_inner(),
                        &m.formula(SequencePosition::default(), 0)
                            .monoisotopic_mass(),
                    )
                })
                .map(|(o, i, n, m)| (o, i, n.clone(), m.clone()))
                .collect(),
            ),
            Self::Formula(formula) => ModificationSearchResult::Formula(
                formula.clone(),
                [
                    Ontology::Unimod,
                    Ontology::Psimod,
                    Ontology::Gnome,
                    Ontology::Xlmod,
                    Ontology::Custom,
                ]
                .iter()
                .flat_map(|o| {
                    o.lookup(custom_database)
                        .iter()
                        .map(|(i, n, m)| (*o, *i, n, m))
                })
                .filter(|(_, _, _, m)| *formula == m.formula(SequencePosition::default(), 0))
                .map(|(o, i, n, m)| (o, i, n.clone(), m.clone()))
                .collect(),
            ),
            Self::Glycan(glycan) => {
                let search = MonoSaccharide::search_composition(glycan.clone());
                ModificationSearchResult::Glycan(
                    glycan.clone(),
                    Ontology::Gnome
                        .lookup(custom_database)
                        .iter()
                        .filter(|(_, _, m)| {
                            if let Self::Gno(GnoComposition::Structure(structure), _) = m {
                                MonoSaccharide::search_composition(structure.composition())
                                    == *search
                            } else {
                                false
                            }
                        })
                        .map(|(i, n, m)| (Ontology::Gnome, *i, n.clone(), m.clone()))
                        .collect(),
                )
            }
            m => ModificationSearchResult::Single(m.clone()),
        }
    }

    /// Generate theoretical fragments for side chains (glycans)
    pub(crate) fn generate_theoretical_fragments(
        &self,
        model: &Model,
        peptidoform_index: usize,
        peptide_index: usize,
        charge_carriers: &mut CachedCharge,
        full_formula: &Multi<MolecularFormula>,
        attachment: Option<(AminoAcid, usize)>,
    ) -> Vec<Fragment> {
        if let Self::GlycanStructure(glycan) = self {
            glycan
                .clone()
                .determine_positions()
                .generate_theoretical_fragments(
                    model,
                    peptidoform_index,
                    peptide_index,
                    charge_carriers,
                    full_formula,
                    attachment,
                )
        } else if let Self::Gno(GnoComposition::Structure(glycan), _) = self {
            glycan
                .clone()
                .determine_positions()
                .generate_theoretical_fragments(
                    model,
                    peptidoform_index,
                    peptide_index,
                    charge_carriers,
                    full_formula,
                    attachment,
                )
        } else if let Self::Glycan(composition) = self {
            MonoSaccharide::theoretical_fragments(
                composition,
                model,
                peptidoform_index,
                peptide_index,
                charge_carriers,
                full_formula,
                attachment,
            )
        } else {
            Vec::new()
        }
    }
}

/// The result of a modification search, see [`Modification::search`].
pub enum ModificationSearchResult {
    /// The modification was already defined
    Single(SimpleModification),
    /// All modifications with the same mass, within the tolerance
    Mass(
        Mass,
        Tolerance<Mass>,
        Vec<(Ontology, usize, String, SimpleModification)>,
    ),
    /// All modifications with the same formula
    Formula(
        MolecularFormula,
        Vec<(Ontology, usize, String, SimpleModification)>,
    ),
    /// All modifications with the same glycan composition
    Glycan(
        Vec<(MonoSaccharide, isize)>,
        Vec<(Ontology, usize, String, SimpleModification)>,
    ),
}

/// The structure to lookup ambiguous modifications, with a list of all modifications (the order is fixed) with for each modification their name and the actual modification itself (if already defined)
pub type AmbiguousLookup = Vec<(String, Option<SimpleModification>)>;
/// The structure to lookup cross-links, with a list of all linkers (the order is fixed) with for each linker their name or None if it is a branch and the actual linker itself (if already defined)
pub type CrossLinkLookup = Vec<(CrossLinkName, Option<SimpleModification>)>;

/// An ambiguous modification which could be placed on any of a set of locations
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Debug, Serialize, Deserialize)]
pub struct AmbiguousModification {
    /// The id to compare be able to find the other locations where this modifications can be placed
    pub id: usize,
    /// The modification itself
    pub modification: SimpleModification,
    /// If present the localisation score, meaning the chance/ratio for this modification to show up on this exact spot
    pub localisation_score: Option<OrderedFloat<f64>>,
    /// The name of the group
    pub group: String,
    /// If this is the preferred location or not
    pub preferred: bool,
}

impl Chemical for AmbiguousModification {
    fn formula(&self, sequence_index: SequencePosition, peptide_index: usize) -> MolecularFormula {
        self.modification.formula(sequence_index, peptide_index)
    }
}

impl Modification {
    /// Display a modification either normalised to the internal representation or as fully valid ProForma
    /// (no glycan structure or custom modifications).
    /// # Errors
    /// When the given writer errors.
    pub fn display(&self, f: &mut impl Write, specification_compliant: bool) -> std::fmt::Result {
        match self {
            Self::Simple(sim) => sim.display(f, specification_compliant),
            Self::CrossLink { name, linker, .. } => write!(f, "{linker}{name}"),
        }
    }
}

impl Display for Modification {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.display(f, true)
    }
}

impl Display for CrossLinkName {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Branch => write!(f, "#BRANCH"),
            Self::Name(n) => write!(f, "#XL{n}"),
        }
    }
}

include!("shared/ontology.rs");

#[test]
#[allow(clippy::missing_panics_doc)]
fn test_reading_custom_modifications_json() {
    use serde_json;
    let data = r#"[ [ 1, "uranium linker", { "Linker": { "specificities": [ { "Asymmetric": [ [ [ { "AminoAcid": [ [ "Selenocysteine" ], "AnyCTerm" ] }, { "AminoAcid": [ [ "GlutamicAcid" ], "Anywhere" ] } ], [ { "AminoAcid": [ [ "Selenocysteine" ], "AnyNTerm" ] } ] ], [ [ { "elements": [ [ "U", null, 1 ] ], "additional_mass": 0.0 }, { "elements": [ [ "U", null, 1 ] ], "additional_mass": 0.0 } ] ], [ { "elements": [ [ "Te", null, 1 ] ], "additional_mass": 0.0 }, { "elements": [ [ "Ne", null, 1 ] ], "additional_mass": 0.0 }, { "elements": [ [ "H", null, 2 ], [ "He", null, 3 ] ], "additional_mass": 0.0 }, { "elements": [ [ "H", null, 1 ], [ "He", null, 2 ] ], "additional_mass": 0.0 }, { "elements": [ [ "I", null, 1 ], [ "Er", null, 1 ] ], "additional_mass": 0.0 }, { "elements": [ [ "H", null, 12 ], [ "C", null, 12 ], [ "O", null, 1 ] ], "additional_mass": 0.0 } ] ] } ], "formula": { "elements": [ [ "U", null, 2 ] ], "additional_mass": 0.0 }, "id": { "ontology": "Custom", "name": "Uranium linker", "id": 1, "description": "Have some uranium, its delicious!", "synonyms": [], "cross_ids": [ [ "Pubmed", "21714143" ] ] }, "length": 23.9 } } ], [ 2, "helium", { "Database": { "specificities": [ [ [ { "AminoAcid": [ [ "Alanine" ], "Anywhere" ] } ], [], [] ], [ [ { "AminoAcid": [ [ "Methionine" ], "Anywhere" ] } ], [ { "Loss": { "elements": [], "additional_mass": 12.0 } } ], [] ] ], "formula": { "elements": [ [ "He", null, 2 ] ], "additional_mass": 0.0 }, "id": { "ontology": "Custom", "name": "Helium", "id": 2, "description": "heeeelium", "synonyms": [ "heeeelium", "funny gas" ], "cross_ids": [ [ "Pubmed", "42" ], [ "Unimod", "12" ], [ "Resid", "A12" ] ] } } } ], [ 3, "db18", { "Database": { "specificities": [ [ [ { "AminoAcid": [ [ "Cysteine" ], "Anywhere" ] } ], [ { "Gain": { "elements": [], "additional_mass": 372.25 } }, { "Gain": { "elements": [], "additional_mass": 373.258 } }, { "Gain": { "elements": [], "additional_mass": 371.242 } }, { "Gain": { "elements": [], "additional_mass": 240.171 } }, { "Gain": { "elements": [], "additional_mass": 239.163 } }, { "Gain": { "elements": [], "additional_mass": 241.179 } }, { "Gain": { "elements": [], "additional_mass": 197.129 } }, { "Gain": { "elements": [], "additional_mass": 198.137 } }, { "Gain": { "elements": [], "additional_mass": 196.121 } }, { "Gain": { "elements": [], "additional_mass": 619.418 } }, { "Gain": { "elements": [], "additional_mass": 621.4343 } }, { "Gain": { "elements": [], "additional_mass": 649.465 } }, { "Gain": { "elements": [], "additional_mass": 677.497 } }, { "Gain": { "elements": [], "additional_mass": 618.41 } }, { "Gain": { "elements": [], "additional_mass": 620.426 } }, { "Gain": { "elements": [], "additional_mass": 648.457 } }, { "Gain": { "elements": [], "additional_mass": 676.489 } }, { "Gain": { "elements": [], "additional_mass": 620.426 } }, { "Gain": { "elements": [], "additional_mass": 622.442 } }, { "Gain": { "elements": [], "additional_mass": 650.473 } }, { "Gain": { "elements": [], "additional_mass": 678.504 } }, { "Gain": { "elements": [], "additional_mass": 28.006 } } ], [ { "elements": [], "additional_mass": 372.25 }, { "elements": [], "additional_mass": 240.171 }, { "elements": [], "additional_mass": 197.129 }, { "elements": [], "additional_mass": 619.418 }, { "elements": [], "additional_mass": 621.434 }, { "elements": [], "additional_mass": 649.465 }, { "elements": [], "additional_mass": 677.497 } ] ] ], "formula": { "elements": [], "additional_mass": 676.489 }, "id": { "ontology": "Custom", "name": "DB18", "id": 3, "description": "", "synonyms": [], "cross_ids": [] } } } ], [ 4, "disulfide", { "Linker": { "specificities": [ { "Symmetric": [ [ { "AminoAcid": [ [ "Cysteine" ], "Anywhere" ] } ], [ [ { "elements": [], "additional_mass": 0.0 }, { "elements": [], "additional_mass": 0.0 } ], [ { "elements": [ [ "H", null, -1 ] ], "additional_mass": 0.0 }, { "elements": [], "additional_mass": 0.0 } ], [ { "elements": [ [ "H", null, -1 ] ], "additional_mass": 0.0 }, { "elements": [ [ "H", null, -1 ] ], "additional_mass": 0.0 } ] ], [] ] } ], "formula": { "elements": [ [ "H", null, -2 ] ], "additional_mass": 0.0 }, "id": { "ontology": "Custom", "name": "Disulfide", "id": 4, "description": "A disulfide with all potential neutral losses", "synonyms": [], "cross_ids": [] }, "length": 0.0 } } ], [ 5, "dsso", { "Linker": { "specificities": [ { "Symmetric": [ [ { "AminoAcid": [ [ "Lysine" ], "Anywhere" ] } ], [ [ { "elements": [ [ "H", null, 1 ], [ "C", null, 3 ], [ "N", null, -1 ], [ "O", null, 3 ], [ "S", null, 1 ] ], "additional_mass": 0.0 }, { "elements": [ [ "H", null, 1 ], [ "C", null, 3 ], [ "N", null, -1 ], [ "O", null, 2 ] ], "additional_mass": 0.0 } ] ], [] ] } ], "formula": { "elements": [ [ "H", null, 2 ], [ "C", null, 6 ], [ "N", null, -2 ], [ "O", null, 5 ], [ "S", null, 1 ] ], "additional_mass": 0.0 }, "id": { "ontology": "Custom", "name": "DSSO", "id": 5, "description": "", "synonyms": [], "cross_ids": [] }, "length": 0.0 } } ]]"#;
    let mods: Vec<(usize, String, SimpleModification)> = serde_json::from_str(data).unwrap();
    assert!(mods.len() > 1);
}
