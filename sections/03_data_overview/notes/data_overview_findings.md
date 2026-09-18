# Data Overview Findings

## Data Sources

The analysis integrates patient readmission, financial impact, and care coordination data using `patient_id`.

## Data Quality Summary

- All three datasets contain 12,000 unique patient IDs after cleaning.
- Patient IDs match across all datasets.
- The largest data quality issue is missing follow-up status, affecting 2,587 records.
- Financial fields include missing and negative values, so nonnegative companion fields and quality flags were created.

## Recommended Slide Message

The data is usable for executive analytics because the join key is complete and unique across datasets, but the Board should understand that missing follow-up documentation and questionable financial values create limitations for precise ROI estimates.
