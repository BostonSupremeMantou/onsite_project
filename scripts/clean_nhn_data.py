from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_CLEAN = ROOT / "data" / "cleaned"
OUTPUT_PROCESSED = ROOT / "data" / "processed"

RAW_FILES = {
    "patient": ROOT / "NHN Patient Readmission Dataset.csv",
    "financial": ROOT / "NHN Financial Impact Dataset.csv",
    "care": ROOT / "NHN Care Coordination Dataset.csv",
    "dictionary": ROOT / "NHN Data Dictionary.csv",
}

COLUMN_ALIASES = {
    "prior_admissions12_m": "prior_admissions_12m",
    "edvisits12_m": "ed_visits_12m",
    "readmitted_within30_days": "readmitted_within_30_days",
}


def to_snake_case(value: str) -> str:
    value = value.strip().replace("%", " percent ")
    value = re.sub(r"[^0-9A-Za-z]+", "_", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_").lower()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        COLUMN_ALIASES.get(to_snake_case(str(col)), to_snake_case(str(col)))
        for col in df.columns
    ]
    return df


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        cleaned = df[col].astype("string").str.strip()
        df[col] = cleaned.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
    return df


def require_unique_patient_id(df: pd.DataFrame, name: str) -> None:
    if "patient_id" not in df.columns:
        raise ValueError(f"{name} is missing patient_id")
    duplicate_count = int(df["patient_id"].duplicated().sum())
    if duplicate_count:
        raise ValueError(f"{name} has {duplicate_count} duplicate patient_id values")


def validate_binary_values(df: pd.DataFrame, columns: list[str], name: str) -> None:
    for col in columns:
        observed = set(df[col].dropna().unique().tolist())
        if not observed.issubset({0, 1}):
            raise ValueError(f"{name}.{col} has non-binary values: {sorted(observed)}")


def add_group_median_imputation(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    output_col: str,
) -> pd.DataFrame:
    df = df.copy()
    medians = df.groupby(group_col, dropna=False)[value_col].median()
    overall_median = df[value_col].median()
    imputed = df[value_col].copy()
    missing = imputed.isna()
    imputed.loc[missing] = (
        df.loc[missing, group_col].map(medians).fillna(overall_median)
    )
    df[output_col] = imputed
    return df


def clean_data_dictionary() -> dict[str, pd.DataFrame]:
    raw = read_csv(RAW_FILES["dictionary"])
    header_rows = raw.index[
        raw["Dataset"].astype("string").str.strip().eq("Dataset")
        & raw["Field"].astype("string").str.strip().eq("Purpose")
    ].tolist()

    if header_rows:
        split_idx = header_rows[0]
        field_dictionary = raw.iloc[:split_idx].dropna(how="all").copy()
        dataset_dictionary = raw.iloc[split_idx + 1 :].dropna(how="all").copy()
    else:
        field_dictionary = raw.dropna(how="all").copy()
        dataset_dictionary = pd.DataFrame(columns=["Dataset", "Field", "Description"])

    field_dictionary = field_dictionary.rename(
        columns={
            "Dataset": "source_dataset",
            "Field": "field",
            "Description": "description",
        }
    )
    dataset_dictionary = dataset_dictionary.rename(
        columns={
            "Dataset": "source_dataset",
            "Field": "purpose",
            "Description": "join_key",
        }
    )

    return {
        "field_dictionary": field_dictionary,
        "dataset_dictionary": dataset_dictionary,
    }


def clean_patient() -> pd.DataFrame:
    patient = normalize_columns(read_csv(RAW_FILES["patient"]))
    patient = clean_text_columns(patient)
    require_unique_patient_id(patient, "patient")

    patient["patient_id"] = patient["patient_id"].astype("int64")
    numeric_cols = [
        "age",
        "chronic_conditions",
        "prior_admissions_12m",
        "length_of_stay_days",
        "ed_visits_12m",
        "readmitted_within_30_days",
    ]
    for col in numeric_cols:
        patient[col] = pd.to_numeric(patient[col], errors="coerce")

    validate_binary_values(patient, ["readmitted_within_30_days"], "patient")

    patient["insurance_type_missing_flag"] = patient["insurance_type"].isna().astype(int)
    patient["follow_up_status_missing_flag"] = patient["follow_up_status"].isna().astype(int)
    patient["length_of_stay_days_missing_flag"] = (
        patient["length_of_stay_days"].isna().astype(int)
    )

    patient["insurance_type"] = patient["insurance_type"].fillna("Unknown")
    patient["follow_up_status"] = patient["follow_up_status"].fillna("Unknown")

    patient = add_group_median_imputation(
        patient,
        value_col="length_of_stay_days",
        group_col="primary_diagnosis",
        output_col="length_of_stay_days_imputed",
    )

    patient["age_group"] = pd.cut(
        patient["age"],
        bins=[17, 34, 49, 64, 74, 84, np.inf],
        labels=["18-34", "35-49", "50-64", "65-74", "75-84", "85+"],
        right=True,
    ).astype("string")
    patient["chronic_condition_bucket"] = pd.cut(
        patient["chronic_conditions"],
        bins=[-1, 0, 2, 4, np.inf],
        labels=["0", "1-2", "3-4", "5+"],
        right=True,
    ).astype("string")
    patient["prior_admissions_bucket"] = pd.cut(
        patient["prior_admissions_12m"],
        bins=[-1, 0, 1, 2, np.inf],
        labels=["0", "1", "2", "3+"],
        right=True,
    ).astype("string")
    patient["ed_visits_bucket"] = pd.cut(
        patient["ed_visits_12m"],
        bins=[-1, 0, 1, 2, np.inf],
        labels=["0", "1", "2", "3+"],
        right=True,
    ).astype("string")
    patient["readmission_label"] = np.where(
        patient["readmitted_within_30_days"].eq(1),
        "Readmitted",
        "Not readmitted",
    )

    patient["patient_data_quality_issue_count"] = patient[
        [
            "insurance_type_missing_flag",
            "follow_up_status_missing_flag",
            "length_of_stay_days_missing_flag",
        ]
    ].sum(axis=1)
    return patient


def clean_financial() -> pd.DataFrame:
    financial = normalize_columns(read_csv(RAW_FILES["financial"]))
    require_unique_patient_id(financial, "financial")
    financial["patient_id"] = financial["patient_id"].astype("int64")

    financial_cols = [
        "readmission_cost",
        "reimbursement_amount",
        "penalty_cost",
        "length_of_stay_cost",
        "follow_up_program_cost",
        "total_care_cost",
    ]
    for col in financial_cols:
        financial[col] = pd.to_numeric(financial[col], errors="coerce")
        financial[f"{col}_missing_flag"] = financial[col].isna().astype(int)
        financial[f"{col}_negative_flag"] = financial[col].lt(0).fillna(False).astype(int)
        financial[f"{col}_nonnegative"] = financial[col].where(financial[col].ge(0))

    financial["total_care_cost_recomputed_excluding_penalty"] = (
        financial["readmission_cost_nonnegative"]
        + financial["length_of_stay_cost_nonnegative"]
        + financial["follow_up_program_cost_nonnegative"]
    )
    financial["total_care_cost_variance_from_recomputed"] = (
        financial["total_care_cost_nonnegative"]
        - financial["total_care_cost_recomputed_excluding_penalty"]
    ).round(2)
    financial["net_reimbursement_gap"] = (
        financial["total_care_cost_nonnegative"]
        - financial["reimbursement_amount_nonnegative"]
    ).round(2)

    issue_cols = [
        col
        for col in financial.columns
        if col.endswith("_missing_flag") or col.endswith("_negative_flag")
    ]
    financial["financial_data_quality_issue_count"] = financial[issue_cols].sum(axis=1)
    return financial


def clean_care() -> pd.DataFrame:
    care = normalize_columns(read_csv(RAW_FILES["care"]))
    require_unique_patient_id(care, "care")
    care["patient_id"] = care["patient_id"].astype("int64")

    binary_cols = [
        "care_coordinator_assigned",
        "follow_up_completed",
        "medication_review_completed",
        "home_health_referral",
        "transportation_assistance_provided",
    ]
    numeric_cols = binary_cols + [
        "follow_up_days_after_discharge",
        "post_discharge_calls",
    ]
    for col in numeric_cols:
        care[col] = pd.to_numeric(care[col], errors="coerce")

    validate_binary_values(care, binary_cols, "care")

    care["follow_up_days_after_discharge_missing_flag"] = (
        care["follow_up_days_after_discharge"].isna().astype(int)
    )
    care["post_discharge_calls_missing_flag"] = (
        care["post_discharge_calls"].isna().astype(int)
    )

    care = add_group_median_imputation(
        care,
        value_col="follow_up_days_after_discharge",
        group_col="follow_up_completed",
        output_col="follow_up_days_after_discharge_imputed",
    )
    care = add_group_median_imputation(
        care,
        value_col="post_discharge_calls",
        group_col="follow_up_completed",
        output_col="post_discharge_calls_imputed",
    )

    care["post_discharge_calls_imputed"] = care[
        "post_discharge_calls_imputed"
    ].round().clip(lower=0)
    care["any_post_discharge_call_flag"] = (
        care["post_discharge_calls_imputed"].fillna(0).gt(0).astype(int)
    )
    intervention_cols = binary_cols + ["any_post_discharge_call_flag"]
    care["intervention_count"] = care[intervention_cols].sum(axis=1)
    care["any_intervention_flag"] = care["intervention_count"].gt(0).astype(int)

    care["care_data_quality_issue_count"] = care[
        [
            "follow_up_days_after_discharge_missing_flag",
            "post_discharge_calls_missing_flag",
        ]
    ].sum(axis=1)
    return care


def summarize_missing(df: pd.DataFrame) -> dict[str, int]:
    missing = df.isna().sum()
    return {col: int(count) for col, count in missing.items() if count > 0}


def summarize_outputs(
    patient: pd.DataFrame,
    financial: pd.DataFrame,
    care: pd.DataFrame,
    master: pd.DataFrame,
) -> dict:
    return {
        "row_counts": {
            "patient_clean": int(len(patient)),
            "financial_clean": int(len(financial)),
            "care_clean": int(len(care)),
            "master_analysis": int(len(master)),
        },
        "unique_patient_ids": {
            "patient_clean": int(patient["patient_id"].nunique()),
            "financial_clean": int(financial["patient_id"].nunique()),
            "care_clean": int(care["patient_id"].nunique()),
            "master_analysis": int(master["patient_id"].nunique()),
        },
        "missing_after_cleaning": {
            "patient_clean": summarize_missing(patient),
            "financial_clean": summarize_missing(financial),
            "care_clean": summarize_missing(care),
            "master_analysis": summarize_missing(master),
        },
        "quality_flags": {
            "patient_rows_with_any_issue": int(
                patient["patient_data_quality_issue_count"].gt(0).sum()
            ),
            "financial_rows_with_any_issue": int(
                financial["financial_data_quality_issue_count"].gt(0).sum()
            ),
            "care_rows_with_any_issue": int(
                care["care_data_quality_issue_count"].gt(0).sum()
            ),
            "master_rows_with_any_issue": int(
                master["data_quality_issue_count"].gt(0).sum()
            ),
        },
        "target_distribution": {
            str(int(k)): int(v)
            for k, v in patient["readmitted_within_30_days"]
            .value_counts()
            .sort_index()
            .items()
        },
        "financial_negative_counts": {
            col: int(financial[f"{col}_negative_flag"].sum())
            for col in [
                "readmission_cost",
                "reimbursement_amount",
                "penalty_cost",
                "length_of_stay_cost",
                "follow_up_program_cost",
                "total_care_cost",
            ]
        },
    }


def write_cleaning_summary(summary: dict) -> None:
    lines = [
        "# Data Cleaning Summary",
        "",
        "## Outputs Created",
        "",
        "- `data/cleaned/patient_readmission_clean.csv`",
        "- `data/cleaned/financial_impact_clean.csv`",
        "- `data/cleaned/care_coordination_clean.csv`",
        "- `data/cleaned/field_dictionary_clean.csv`",
        "- `data/cleaned/dataset_dictionary_clean.csv`",
        "- `data/processed/nhn_patient_level_analysis.csv`",
        "- `data/processed/cleaning_summary.json`",
        "",
        "## Join Integrity",
        "",
        "All three source datasets contain 12,000 unique `PatientID` values, and the ID sets match across patient, financial, and care coordination files.",
        "",
        "## Cleaning Rules Applied",
        "",
        "- Raw CSV files were not modified.",
        "- Column names were standardized to snake_case in cleaned outputs.",
        "- Text fields were trimmed and blank strings were normalized to missing values.",
        "- Missing `insurance_type` and `follow_up_status` values were converted to `Unknown`, with missing flags retained.",
        "- Missing `length_of_stay_days` values were preserved and a diagnosis-median `length_of_stay_days_imputed` field was added.",
        "- Financial values below zero were flagged and excluded from companion `_nonnegative` fields.",
        "- Missing financial values were flagged. They were not silently replaced in the base cleaned financial fields.",
        "- Missing care coordination timing and call counts were flagged. Median-imputed companion fields were added for analysis.",
        "- A merged patient-level analysis table was created using `patient_id` as the join key.",
        "",
        "## Quality Flag Counts",
        "",
        f"- Patient rows with at least one issue: {summary['quality_flags']['patient_rows_with_any_issue']:,}",
        f"- Financial rows with at least one issue: {summary['quality_flags']['financial_rows_with_any_issue']:,}",
        f"- Care coordination rows with at least one issue: {summary['quality_flags']['care_rows_with_any_issue']:,}",
        f"- Master rows with at least one issue: {summary['quality_flags']['master_rows_with_any_issue']:,}",
        "",
        "## Target Distribution",
        "",
        f"- Not readmitted within 30 days: {summary['target_distribution'].get('0', 0):,}",
        f"- Readmitted within 30 days: {summary['target_distribution'].get('1', 0):,}",
        "",
        "## Financial Negative Value Counts",
        "",
    ]
    for col, count in summary["financial_negative_counts"].items():
        lines.append(f"- `{col}`: {count:,}")

    lines.extend(
        [
            "",
            "## Notes For Analysis",
            "",
            "- Use `nhn_patient_level_analysis.csv` for integrated EDA, risk segmentation, care coordination analysis, and executive dashboard preparation.",
            "- Use pre-discharge clinical and care coordination variables for readmission risk modeling. Financial fields should generally be treated as outcome and impact fields, not pre-discharge predictors.",
            "- Use the missing and negative flags in sensitivity checks, especially for financial impact and ROI estimates.",
            "- Treat the PDF requirements as project scope and presentation guidance. Actual findings must come from the cleaned CSV data.",
            "",
        ]
    )
    (ROOT / "DATA_CLEANING_SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_CLEAN.mkdir(parents=True, exist_ok=True)
    OUTPUT_PROCESSED.mkdir(parents=True, exist_ok=True)

    dictionaries = clean_data_dictionary()
    patient = clean_patient()
    financial = clean_financial()
    care = clean_care()

    patient_ids = set(patient["patient_id"])
    if patient_ids != set(financial["patient_id"]) or patient_ids != set(care["patient_id"]):
        raise ValueError("PatientID sets do not match across datasets")

    master = (
        patient.merge(care, on="patient_id", how="inner")
        .merge(financial, on="patient_id", how="inner")
        .copy()
    )
    master["data_quality_issue_count"] = (
        master["patient_data_quality_issue_count"]
        + master["care_data_quality_issue_count"]
        + master["financial_data_quality_issue_count"]
    )
    master["has_data_quality_issue_flag"] = (
        master["data_quality_issue_count"].gt(0).astype(int)
    )

    patient.to_csv(OUTPUT_CLEAN / "patient_readmission_clean.csv", index=False)
    financial.to_csv(OUTPUT_CLEAN / "financial_impact_clean.csv", index=False)
    care.to_csv(OUTPUT_CLEAN / "care_coordination_clean.csv", index=False)
    dictionaries["field_dictionary"].to_csv(
        OUTPUT_CLEAN / "field_dictionary_clean.csv", index=False
    )
    dictionaries["dataset_dictionary"].to_csv(
        OUTPUT_CLEAN / "dataset_dictionary_clean.csv", index=False
    )
    master.to_csv(OUTPUT_PROCESSED / "nhn_patient_level_analysis.csv", index=False)

    summary = summarize_outputs(patient, financial, care, master)
    (OUTPUT_PROCESSED / "cleaning_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    write_cleaning_summary(summary)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
