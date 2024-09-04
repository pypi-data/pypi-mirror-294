use ordered_float::OrderedFloat;
use serde::{Deserialize, Serialize};

use crate::{
    formula::MolecularFormula, AminoAcid, DiagnosticIon, LinkerSpecificity, ModificationId,
    NeutralLoss, SimpleModification,
};

#[derive(Debug, Default)]
pub struct OntologyModification {
    pub formula: MolecularFormula,
    pub name: String,
    pub ontology: Ontology,
    pub id: usize,
    pub description: String,
    pub synonyms: Vec<String>,
    pub cross_ids: Vec<(String, String)>,
    pub data: ModData,
}

#[derive(Debug)]
pub enum ModData {
    Mod {
        specificities: Vec<(Vec<PlacementRule>, Vec<NeutralLoss>, Vec<DiagnosticIon>)>,
    },
    Linker {
        length: Option<OrderedFloat<f64>>,
        specificities: Vec<LinkerSpecificity>,
    },
}

impl Default for ModData {
    fn default() -> Self {
        Self::Mod {
            specificities: Vec::new(),
        }
    }
}

impl OntologyModification {
    /// Simplify the placement rules
    pub fn simplify_rules(&mut self) {
        if let ModData::Mod {
            specificities: ref mut rules,
            ..
        } = self.data
        {
            let mut new = Vec::new();
            for rule in rules.iter() {
                if new.is_empty() {
                    new.push(rule.clone());
                } else {
                    let mut found = false;
                    for new_rule in &mut new {
                        // Check if there is a rule with the same neutral loss and diagnostic ions (these can be location specific)
                        if new_rule.1 == rule.1 && new_rule.2 == rule.2 {
                            found = true;
                            // Check if there are other rules in this set of neutral&diagnostic that also use AA placements
                            // If there are, and they are on the same position, merge the AA set
                            for position in &rule.0 {
                                let mut pos_found = false;
                                for new_position in &mut new_rule.0 {
                                    if let (
                                        PlacementRule::AminoAcid(new_aa, new_pos),
                                        PlacementRule::AminoAcid(aa, pos),
                                    ) = (new_position, position)
                                    {
                                        if *new_pos == *pos {
                                            new_aa.extend(aa);
                                            new_aa.sort_unstable();
                                            pos_found = true;
                                            break;
                                        }
                                    }
                                }
                                if !pos_found {
                                    new_rule.0.push(position.clone());
                                }
                            }
                        }
                    }
                    if !found {
                        new.push(rule.clone());
                    }
                }
            }
            rules.clear();
            rules.extend(new);
        }
    }

    pub fn into_mod(mut self) -> (usize, String, SimpleModification) {
        self.simplify_rules();
        let id = ModificationId {
            ontology: self.ontology,
            name: self.name.clone(),
            id: self.id,
            description: self.description,
            synonyms: self.synonyms,
            cross_ids: self.cross_ids,
        };
        match self.data {
            ModData::Mod { specificities } => (
                self.id,
                self.name.to_ascii_lowercase(),
                SimpleModification::Database {
                    id,
                    formula: self.formula,
                    specificities,
                },
            ),
            ModData::Linker {
                specificities,
                length,
            } => (
                self.id,
                self.name.to_ascii_lowercase(),
                SimpleModification::Linker {
                    specificities,
                    formula: self.formula,
                    id,
                    length,
                },
            ),
        }
    }
}

include!("../shared/placement_rule.rs");
include!("../shared/ontology.rs");

impl TryInto<Position> for u8 {
    type Error = String;
    fn try_into(self) -> Result<Position, Self::Error> {
        match self {
            b'1' => Ok(Position::Anywhere),
            b'2' => Ok(Position::Anywhere),
            b'3' => Ok(Position::AnyNTerm),
            b'4' => Ok(Position::AnyCTerm),
            b'5' => Ok(Position::ProteinNTerm),
            b'6' => Ok(Position::ProteinCTerm),
            n => Err(format!("Outside range: {n}")),
        }
    }
}

impl TryInto<Position> for &str {
    type Error = String;
    fn try_into(self) -> Result<Position, Self::Error> {
        match self {
            "" => Ok(Position::Anywhere),
            "Anywhere" => Ok(Position::Anywhere),
            "Any N-term" => Ok(Position::AnyNTerm),
            "Any C-term" => Ok(Position::AnyCTerm),
            "Protein N-term" => Ok(Position::ProteinNTerm),
            "Protein C-term" => Ok(Position::ProteinCTerm),
            n => Err(format!("Not valid position: {n}")),
        }
    }
}
