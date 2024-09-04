use std::{ffi::OsString, io::Write, iter, path::Path};

use regex::Regex;

use crate::{formula::MolecularFormula, NeutralLoss};

use super::{
    obo::OboOntology,
    ontology_modification::{OntologyModification, OntologyModificationList, PlacementRule},
    ModData,
};

pub fn build_unimod_ontology(out_dir: &OsString, debug: bool) {
    let mods = parse_unimod(debug);

    let dest_path = Path::new(&out_dir).join("unimod.dat");
    let mut file = std::fs::File::create(dest_path).unwrap();
    let final_mods = mods.into_iter().map(|m| m.into_mod()).collect::<Vec<_>>();
    file.write_all(&bincode::serialize::<OntologyModificationList>(&final_mods).unwrap())
        .unwrap();
}

fn parse_unimod(_debug: bool) -> Vec<OntologyModification> {
    let obo = OboOntology::from_file("databases/unimod.obo.gz").expect("Not a valid obo file");
    let mut mods = Vec::new();

    for obj in obo.objects {
        if obj.name != "Term" {
            continue;
        }
        let mut take = false;
        let mut modification = OntologyModification {
            id: obj.lines["id"][0]
                .split_once(':')
                .expect("Incorrect psi mod id, should contain a colon")
                .1
                .parse()
                .expect("Incorrect psi mod id, should be numerical"),
            name: obj.lines["name"][0].to_string(),
            ontology: super::ontology_modification::Ontology::Unimod,
            ..OntologyModification::default()
        };
        if let Some(values) = obj.lines.get("def") {
            assert!(values.len() == 1);
            let line = values[0][1..].split_once('\"').unwrap();
            modification.description = line.0.to_string();
            let ids = line.1.trim();
            modification.cross_ids = ids[1..ids.len() - 1]
                .split(',')
                .map(|id| id.trim().split_once(':').unwrap())
                .filter(|(r, _)| *r != "UNIMODURL")
                .map(|(r, i)| (r.to_string(), i.replace("\\:", ":").to_string())) // Some urls have escaped colons
                .collect();
        }
        if let Some(values) = obj.lines.get("synonym") {
            for line in values {
                let line = line[1..].split_once('\"').unwrap();
                modification.synonyms.push(line.0.to_string());
            }
        }
        if let Some(xref) = obj.lines.get("xref") {
            let re_position = Regex::new("spec_(\\d+)_position \"(.+)\"").unwrap();
            let re_site = Regex::new("spec_(\\d+)_site \"(.+)\"").unwrap();
            let re_neutral_loss =
                Regex::new("spec_(\\d+)_neutral_loss_\\d+_composition \"(.+)\"").unwrap();
            let mut mod_rules = Vec::new();
            for line in xref {
                if line.starts_with("delta_composition") {
                    modification.formula =
                        MolecularFormula::from_unimod(line, 19..line.len()).unwrap();
                    take = true;
                } else if let Some(groups) = re_position.captures(line) {
                    let index = groups.get(1).unwrap().as_str().parse::<usize>().unwrap() - 1;
                    let position = groups.get(2).unwrap().as_str().to_string();
                    if mod_rules.len() <= index {
                        mod_rules.extend(
                            iter::repeat((String::new(), String::new(), Vec::new()))
                                .take(index + 1 - mod_rules.len()),
                        );
                    }
                    mod_rules[index].1 = position;
                } else if let Some(groups) = re_site.captures(line) {
                    let index = groups.get(1).unwrap().as_str().parse::<usize>().unwrap() - 1;
                    let site = groups.get(2).unwrap().as_str().to_string();
                    if mod_rules.len() <= index {
                        mod_rules.extend(
                            iter::repeat((String::new(), String::new(), Vec::new()))
                                .take(index + 1 - mod_rules.len()),
                        );
                    }
                    mod_rules[index].0.push_str(&site);
                } else if let Some(groups) = re_neutral_loss.captures(line) {
                    let index = groups.get(1).unwrap().as_str().parse::<usize>().unwrap() - 1;
                    if !groups
                        .get(2)
                        .is_some_and(|g| g.is_empty() || g.as_str() == "0")
                    {
                        let loss = NeutralLoss::Loss(
                            MolecularFormula::from_unimod(groups.get(2).unwrap().as_str(), ..)
                                .unwrap(),
                        );
                        if mod_rules.len() <= index {
                            mod_rules.extend(
                                iter::repeat((String::new(), String::new(), Vec::new()))
                                    .take(index + 1 - mod_rules.len()),
                            );
                        }
                        mod_rules[index].2.push(loss);
                    }
                } else {
                    continue;
                }
            }
            if let ModData::Mod {
                specificities: rules,
                ..
            } = &mut modification.data
            {
                rules.extend(mod_rules.into_iter().filter_map(|rule| {
                    match (rule.0.as_str(), rule.1.as_str()) {
                        ("C-term", pos) => Some((
                            vec![PlacementRule::Terminal(pos.try_into().unwrap())],
                            rule.2,
                            Vec::new(),
                        )),
                        ("N-term", pos) => Some((
                            vec![PlacementRule::Terminal(pos.try_into().unwrap())],
                            rule.2,
                            Vec::new(),
                        )),
                        ("", "") => None,
                        (aa, pos) => Some((
                            vec![PlacementRule::AminoAcid(
                                aa.chars()
                                    .map(|c| {
                                        c.try_into().unwrap_or_else(|_| panic!("Not an AA: {c}"))
                                    })
                                    .collect(),
                                pos.try_into().unwrap(),
                            )],
                            rule.2,
                            Vec::new(),
                        )),
                    }
                }));
            }
        }
        if take {
            mods.push(modification);
        }
    }

    mods
}
