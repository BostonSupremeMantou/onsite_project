# Data Cleaning Summary

## Outputs Created

- `data/cleaned/patient_readmission_clean.csv`
- `data/cleaned/financial_impact_clean.csv`
- `data/cleaned/care_coordination_clean.csv`
- `data/cleaned/field_dictionary_clean.csv`
- `data/cleaned/dataset_dictionary_clean.csv`
- `data/processed/nhn_patient_level_analysis.csv`
- `data/processed/cleaning_summary.json`

## Join Integrity

All three source datasets contain 12,000 unique `PatientID` values, and the ID sets match across patient, financial, and care coordination files.

## Cleaning Rules Applied

- Raw CSV files were not modified.
- Column names were standardized to snake_case in cleaned outputs.
- Text fields were trimmed and blank strings were normalized to missing values.
- Missing `insurance_type` and `follow_up_status` values were converted to `Unknown`, with missing flags retained.
- Missing `length_of_stay_days` values were preserved and a diagnosis-median `length_of_stay_days_imputed` field was added.
- Financial values below zero were flagged and excluded from companion `_nonnegative` fields.
- Missing financial values were flagged. They were not silently replaced in the base cleaned financial fields.
- Missing care coordination timing and call counts were flagged. Median-imputed companion fields were added for analysis.
- A merged patient-level analysis table was created using `patient_id` as the join key.

## Quality Flag Counts

- Patient rows with at least one issue: 2,964
- Financial rows with at least one issue: 550
- Care coordination rows with at least one issue: 356
- Master rows with at least one issue: 3,620

## Target Distribution

- Not readmitted within 30 days: 6,816
- Readmitted within 30 days: 5,184

## Financial Negative Value Counts

- `readmission_cost`: 4
- `reimbursement_amount`: 4
- `penalty_cost`: 49
- `length_of_stay_cost`: 4
- `follow_up_program_cost`: 15
- `total_care_cost`: 0

## Notes For Analysis

- Use `nhn_patient_level_analysis.csv` for integrated EDA, risk segmentation, care coordination analysis, and executive dashboard preparation.
- Use pre-discharge clinical and care coordination variables for readmission risk modeling. Financial fields should generally be treated as outcome and impact fields, not pre-discharge predictors.
- Use the missing and negative flags in sensitivity checks, especially for financial impact and ROI estimates.
- Treat the PDF requirements as project scope and presentation guidance. Actual findings must come from the cleaned CSV data.
