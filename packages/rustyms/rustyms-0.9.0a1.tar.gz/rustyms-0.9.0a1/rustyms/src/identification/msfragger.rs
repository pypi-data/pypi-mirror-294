use std::path::{Path, PathBuf};

//Spectrum	Spectrum.File	Peptide	Modified sequence	Extended.Peptide	Prev.AA	Next.AA	Peptide.Length	Charge	Retention	Observed.Mass	Calibrated.Observed.Mass	Observed.M.Z	Calibrated.Observed.M.Z	Calculated.Peptide.Mass	Calculated.M.Z	Delta.Mass	Expectation	Hyperscore	Nextscore	PeptideProphet.Probability	Number.of.Enzymatic.Termini	Number.of.Missed.Cleavages	Protein.Start	Protein.End	Intensity	Assigned.Modifications	Observed.Modifications	Purity	Is.Unique	Protein	Protein.ID	Entry.Name	Gene	Protein.Description	Mapped.Genes	Mapped.Proteins	condition	group
use crate::{
    error::{Context, CustomError},
    helper_functions::{explain_number_error, InvertResult},
    ontologies::CustomDatabase,
    peptide::{SloppyParsingParameters, VerySimple},
    system::{usize::Charge, Mass, MassOverCharge, Time},
    LinearPeptide,
};
use itertools::Itertools;
use serde::{Deserialize, Serialize};

use super::{
    common_parser::{Location, OptionalLocation},
    csv::{parse_csv, CsvLine},
    BoxedIdentifiedPeptideIter, IdentifiedPeptide, IdentifiedPeptideSource, MetaData,
};

static NUMBER_ERROR: (&str, &str) = (
    "Invalid MSFragger line",
    "This column is not a number but it is required to be a number in this MSFragger format",
);
static BOOL_ERROR: (&str, &str) = (
    "Invalid MSFragger line",
    "This column is not a boolean but it is required to be a boolean ('true' or 'false') in this MSFragger format",
);

format_family!(
    /// The format for any MSFragger file
    MSFraggerFormat,
    /// The data from any MSFragger file
    MSFraggerData,
    MSFraggerVersion, [&V21, &V22], b'\t';
    required {
        spectrum: MSFraggerID, |location: Location, _| location.as_str().parse::<MSFraggerID>().map_err(|err| err.with_context(location.context()));
        spectrum_file: String, |location: Location, _| Ok(location.get_string());
        peptide: Option<LinearPeptide<VerySimple>>, |location: Location, custom_database: Option<&CustomDatabase>| location.or_empty().parse_with(|location| LinearPeptide::sloppy_pro_forma(
            location.full_line(),
            location.location.clone(),
            custom_database,
            SloppyParsingParameters {ignore_prefix_lowercase_n: true},
        ));
        extended_peptide: String, |location: Location, _| Ok(location.get_string());
        z: Charge, |location: Location, _| location.parse::<usize>(NUMBER_ERROR).map(Charge::new::<crate::system::e>);
        rt: Time, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(Time::new::<crate::system::time::s>);
        experimental_mass: Mass, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(Mass::new::<crate::system::dalton>);
        calibrated_experimental_mass: Mass, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(Mass::new::<crate::system::dalton>);
        experimental_mz: MassOverCharge, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(MassOverCharge::new::<crate::system::mz>);
        calibrated_experimental_mz: MassOverCharge, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(MassOverCharge::new::<crate::system::mz>);
        expectation: f64, |location: Location, _| location.parse(NUMBER_ERROR);
        hyperscore: f64, |location: Location, _| location.parse(NUMBER_ERROR).map(|s: f64| s / 100.0);
        next_score: f64, |location: Location, _| location.parse(NUMBER_ERROR).map(|s: f64| s / 100.0);
        peptide_prophet_probability: f64, |location: Location, _| location.parse(NUMBER_ERROR);
        enzymatic_termini: usize, |location: Location, _| location.parse(NUMBER_ERROR);
        missed_cleavages: usize, |location: Location, _| location.parse(NUMBER_ERROR);
        protein_start: usize, |location: Location, _| location.parse(NUMBER_ERROR);
        protein_end: usize, |location: Location, _| location.parse(NUMBER_ERROR);
        intensity: f64, |location: Location, _| location.parse(NUMBER_ERROR);
        assigned_modifications: String, |location: Location, _| Ok(location.get_string());
        purity: f64, |location: Location, _| location.parse(NUMBER_ERROR);
        is_unique: bool, |location: Location, _| location.parse(BOOL_ERROR);
        protein: String, |location: Location, _| Ok(location.get_string());
        protein_id: String, |location: Location, _| Ok(location.get_string());
        entry_name: String, |location: Location, _| Ok(location.get_string());
        gene: String, |location: Location, _| Ok(location.get_string());
        protein_description: String, |location: Location, _| Ok(location.get_string());
        mapped_genes: Vec<String>, |location: Location, _| Ok(location.get_string().split(',').map(|s| s.trim().to_string()).collect_vec());
        mapped_proteins: Vec<String>, |location: Location, _| Ok(location.get_string().split(',').map(|s| s.trim().to_string()).collect_vec());
    }
    optional {
        condition: String, |location: Location, _| Ok(Some(location.get_string()));
        group: String, |location: Location, _| Ok(Some(location.get_string()));
    }
);

impl From<MSFraggerData> for IdentifiedPeptide {
    fn from(value: MSFraggerData) -> Self {
        Self {
            score: Some(value.hyperscore),
            metadata: MetaData::MSFragger(value),
        }
    }
}

/// All possible MSFragger versions
#[derive(Clone, Eq, PartialEq, Ord, PartialOrd, Hash, Debug, Default, Serialize, Deserialize)]
pub enum MSFraggerVersion {
    /// Version 21
    #[default]
    #[allow(clippy::upper_case_acronyms)]
    V21,
    /// Version 22
    V22,
}

impl std::fmt::Display for MSFraggerVersion {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::result::Result<(), std::fmt::Error> {
        write!(
            f,
            "{}",
            match self {
                Self::V21 => "v21",
                Self::V22 => "v22",
            }
        )
    }
}

/// v21
pub const V21: MSFraggerFormat = MSFraggerFormat {
    version: MSFraggerVersion::V21,
    spectrum: "spectrum",
    spectrum_file: "spectrum file",
    peptide: "modified peptide",
    extended_peptide: "extended peptide",
    z: "charge",
    rt: "retention",
    experimental_mass: "observed mass",
    calibrated_experimental_mass: "calibrated observed mass",
    experimental_mz: "observed m/z",
    calibrated_experimental_mz: "calibrated observed m/z",
    expectation: "expectation",
    hyperscore: "hyperscore",
    next_score: "nextscore",
    peptide_prophet_probability: "peptideprophet probability",
    enzymatic_termini: "number of enzymatic termini",
    missed_cleavages: "number of missed cleavages",
    protein_start: "protein start",
    protein_end: "protein end",
    intensity: "intensity",
    assigned_modifications: "assigned modifications",
    purity: "purity",
    is_unique: "is unique",
    protein: "protein",
    protein_id: "protein id",
    entry_name: "entry name",
    gene: "gene",
    protein_description: "protein description",
    mapped_genes: "mapped genes",
    mapped_proteins: "mapped proteins",
    condition: Some("condition"),
    group: Some("group"),
};

/// v22
pub const V22: MSFraggerFormat = MSFraggerFormat {
    version: MSFraggerVersion::V22,
    spectrum: "spectrum",
    spectrum_file: "spectrum file",
    peptide: "modified peptide",
    extended_peptide: "extended peptide",
    z: "charge",
    rt: "retention",
    experimental_mass: "observed mass",
    calibrated_experimental_mass: "calibrated observed mass",
    experimental_mz: "observed m/z",
    calibrated_experimental_mz: "calibrated observed m/z",
    expectation: "expectation",
    hyperscore: "hyperscore",
    next_score: "nextscore",
    peptide_prophet_probability: "probability",
    enzymatic_termini: "number of enzymatic termini",
    missed_cleavages: "number of missed cleavages",
    protein_start: "protein start",
    protein_end: "protein end",
    intensity: "intensity",
    assigned_modifications: "assigned modifications",
    purity: "purity",
    is_unique: "is unique",
    protein: "protein",
    protein_id: "protein id",
    entry_name: "entry name",
    gene: "gene",
    protein_description: "protein description",
    mapped_genes: "mapped genes",
    mapped_proteins: "mapped proteins",
    condition: Some("condition"),
    group: Some("group"),
};

/// The scans identifier for a MSFragger identification
#[derive(Clone, Eq, PartialEq, Ord, PartialOrd, Hash, Debug, Default, Serialize, Deserialize)]
pub struct MSFraggerID {
    /// The file, if defined
    pub file: PathBuf,
    /// The scan number triplet
    pub scan: (usize, usize, usize),
}

impl std::fmt::Display for MSFraggerID {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}.{}.{}.{}",
            self.file.to_string_lossy(),
            self.scan.0,
            self.scan.1,
            self.scan.2,
        )
    }
}

impl std::str::FromStr for MSFraggerID {
    type Err = CustomError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let split = s.rsplitn(4, '.').collect_vec();
        if split.len() == 4 {
            Ok(Self {
                file: Path::new(&split[3]).to_owned(),
                scan: (
                    split[2].parse().map_err(|err| {
                        CustomError::error(
                            "Invalid MSFragger ID",
                            format!("The scan number {}", explain_number_error(&err)),
                            Context::None,
                        )
                    })?,
                    split[1].parse().map_err(|err| {
                        CustomError::error(
                            "Invalid MSFragger ID",
                            format!("The scan number {}", explain_number_error(&err)),
                            Context::None,
                        )
                    })?,
                    split[0].parse().map_err(|err| {
                        CustomError::error(
                            "Invalid MSFragger ID",
                            format!("The scan number {}", explain_number_error(&err)),
                            Context::None,
                        )
                    })?,
                ),
            })
        } else {
            Err(CustomError::error(
                "Invalid MSFragger ID",
                "An MSFragger ID should consist of 4 parts separated by dots (file.scan.scan.scan)",
                Context::None,
            ))
        }
    }
}
