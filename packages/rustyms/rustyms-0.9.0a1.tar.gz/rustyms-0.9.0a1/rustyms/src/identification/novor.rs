use super::{
    common_parser::Location,
    csv::{parse_csv, CsvLine},
    BoxedIdentifiedPeptideIter, IdentifiedPeptide, IdentifiedPeptideSource, MetaData,
};
use crate::{
    error::CustomError,
    helper_functions::InvertResult,
    ontologies::CustomDatabase,
    peptide::{SloppyParsingParameters, VerySimple},
    system::{usize::Charge, Mass, MassOverCharge, Ratio, Time},
    LinearPeptide,
};
use serde::{Deserialize, Serialize};

static NUMBER_ERROR: (&str, &str) = (
    "Invalid Novor line",
    "This column is not a number but it is required to be a number in this Novor format",
);

format_family!(
    /// The format for Novor data
    NovorFormat,
    /// The Novor data
    NovorData,
    NovorVersion, [&OLD_DENOVO, &OLD_PSM, &NEW_DENOVO, &NEW_PSM], b',';
    required {
        scan: usize, |location: Location, _| location.parse(NUMBER_ERROR);
        mz: MassOverCharge, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(MassOverCharge::new::<crate::system::mz>);
        z: Charge, |location: Location, _| location.parse::<usize>(NUMBER_ERROR).map(Charge::new::<crate::system::e>);
        mass: Mass, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(Mass::new::<crate::system::dalton>);
        ppm: Ratio, |location: Location, _| location.parse(NUMBER_ERROR).map(Ratio::new::<crate::system::ratio::ppm>);
        score: f64, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(|f| f / 100.0);
        peptide: LinearPeptide<VerySimple>, |location: Location, custom_database: Option<&CustomDatabase>| LinearPeptide::sloppy_pro_forma(
            location.full_line(),
            location.location.clone(),
            custom_database,
            SloppyParsingParameters::default(),
        );
    }
    optional {
        id: usize, |location: Location, _| location.parse::<usize>(NUMBER_ERROR);
        spectra_id: usize, |location: Location, _| location.parse::<usize>(NUMBER_ERROR);
        fraction: usize, |location: Location, _| location
            .apply(|l| Location {
                line: l.line,
                location: l.location.start + 1..l.location.end,
            }) // Skip the F of the F{num} definition
            .parse::<usize>(NUMBER_ERROR);
        rt: Time, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(Time::new::<crate::system::time::min>);
        mass_err: Mass, |location: Location, _| location.parse::<f64>(NUMBER_ERROR).map(Mass::new::<crate::system::dalton>);
        length: usize, |location: Location, _| location.parse::<usize>(NUMBER_ERROR);
        peptide_no_ptm: String, |location: Location, _| Ok(Some(location.get_string()));
        protein: usize, |location: Location, _| location.parse::<usize>(NUMBER_ERROR);
        protein_start: usize, |location: Location, _| location.parse::<usize>(NUMBER_ERROR);
        protein_origin:String, |location: Location, _| Ok(Some(location.get_string()));
        protein_all: String, |location: Location, _| Ok(Some(location.get_string()));
        database_sequence: String, |location: Location, _| Ok(Some(location.get_string()));
        local_confidence: Vec<f64>, |location: Location, _| location.array('-')
                    .map(|l| l.parse::<f64>(NUMBER_ERROR).map(|v| v / 100.0))
                    .collect::<Result<Vec<_>, _>>();
    }
);

impl From<NovorData> for IdentifiedPeptide {
    fn from(value: NovorData) -> Self {
        Self {
            score: Some(value.score.clamp(-1.0, 1.0)),
            metadata: MetaData::Novor(value),
        }
    }
}

/// All available Novor versions
#[derive(Clone, Eq, PartialEq, Ord, PartialOrd, Hash, Debug, Default, Serialize, Deserialize)]
pub enum NovorVersion {
    /// An older version for the denovo file
    #[default]
    OldDenovo,
    /// An older version for the psms file
    OldPSM,
    /// Seen since v3.36.893 (not necessarily the time it was rolled out)
    NewDenovo,
    /// Seen since v3.36.893 (not necessarily the time it was rolled out)
    NewPSM,
}
impl std::fmt::Display for NovorVersion {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::result::Result<(), std::fmt::Error> {
        write!(
            f,
            "{}",
            match self {
                Self::OldDenovo => "Older Denovo",
                Self::OldPSM => "Older PSM",
                Self::NewDenovo => "New Denovo",
                Self::NewPSM => "New PSM",
            }
        )
    }
}

/// The older supported format for denovo.csv files from Novor
///# -
/// 1       Fraction
/// 2       Scan #
/// 3       m/z
/// 4       z
/// 5       Score
/// 6       Peptide Mass
/// 7       Error (ppm)
/// 8       Length
/// 9       De Novo Peptide
/// 10      DB Sequence
/// <https://github.com/snijderlab/stitch/issues/156#issuecomment-1097862072>
pub const OLD_DENOVO: NovorFormat = NovorFormat {
    version: NovorVersion::OldDenovo,
    scan: "scan #",
    mz: "m/z",
    z: "z",
    mass: "peptide mass",
    ppm: "error (ppm)",
    score: "score",
    peptide: "de novo peptide",
    id: None,
    spectra_id: None,
    fraction: Some("fraction"),
    rt: None,
    mass_err: None,
    length: Some("length"),
    peptide_no_ptm: None,
    protein: None,
    protein_start: None,
    protein_origin: None,
    protein_all: None,
    database_sequence: Some("db sequence"),
    local_confidence: None,
};

/// The older supported format for psms.csv files from Novor
///# -
/// 1       ID
/// 2       Fraction
/// 3       Scan
/// 4       m/z
/// 5       z
/// 6       Score
/// 7       Mass
/// 8       Error (ppm)
/// 9       # Proteins
/// 10      Sequence
/// <https://github.com/snijderlab/stitch/issues/156#issuecomment-1097862072>
pub const OLD_PSM: NovorFormat = NovorFormat {
    version: NovorVersion::OldPSM,
    scan: "scan",
    mz: "m/z",
    z: "z",
    mass: "mass",
    ppm: "error (ppm)",
    score: "score",
    peptide: "sequence",
    id: Some("id"),
    spectra_id: None,
    fraction: Some("fraction"),
    rt: None,
    mass_err: None,
    length: None,
    peptide_no_ptm: None,
    protein: Some("# proteins"),
    protein_start: None,
    protein_origin: None,
    protein_all: None,
    database_sequence: None,
    local_confidence: None,
};

/// denovo: `# id, scanNum, RT, mz(data), z, pepMass(denovo), err(data-denovo), ppm(1e6*err/(mz*z)), score, peptide, aaScore,`
pub const NEW_DENOVO: NovorFormat = NovorFormat {
    version: NovorVersion::NewDenovo,
    scan: "scannum",
    mz: "mz(data)",
    z: "z",
    mass: "pepmass(denovo)",
    ppm: "ppm(1e6*err/(mz*z))",
    score: "score",
    peptide: "peptide",
    id: Some("# id"),
    spectra_id: None,
    fraction: Some("fraction"),
    rt: None,
    mass_err: Some("err(data-denovo)"),
    length: None,
    peptide_no_ptm: None,
    protein: Some("# proteins"),
    protein_start: None,
    protein_origin: None,
    protein_all: None,
    database_sequence: None,
    local_confidence: Some("aascore"),
};

/// PSM: `#id, spectraId, scanNum, RT, mz, z, pepMass, err, ppm, score, protein, start, length, origin, peptide, noPTMPeptide, aac, allProteins`
pub const NEW_PSM: NovorFormat = NovorFormat {
    version: NovorVersion::NewPSM,
    scan: "scannum",
    mz: "mz",
    z: "z",
    mass: "pepmass",
    ppm: "ppm",
    score: "score",
    peptide: "peptide",
    id: Some("#id"),
    spectra_id: None,
    fraction: Some("fraction"),
    rt: None,
    mass_err: Some("err(data-denovo)"),
    length: Some("length"),
    peptide_no_ptm: Some("noptmpeptide"),
    protein: Some("protein"),
    protein_start: Some("start"),
    protein_origin: Some("origin"),
    protein_all: Some("allproteins"),
    database_sequence: None,
    local_confidence: Some("aac"),
};
