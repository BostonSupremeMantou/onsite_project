# Exploratory Data Analysis Report

## Executive Summary

The cleaned integrated dataset contains 12,000 matched patient records across the patient readmission, financial impact, and care coordination datasets. The analytical sample readmission rate is 43.2%. The strongest descriptive readmission patterns appear in chronic condition burden, prior admissions, age, emergency admission type, skilled nursing discharge, and missing follow-up status.

## Data Sources

| Dataset | Role |
| --- | --- |
| Patient Readmission Dataset | Clinical and utilization variables plus readmission outcome |
| Financial Impact Dataset | Readmission cost, reimbursement, penalty, and total care cost fields |
| Care Coordination Dataset | Post-discharge support and intervention fields |

All three datasets contain 12,000 unique `patient_id` values and join completely.

## Data Quality Assessment

| dataset | issue | affected_rows | affected_rate |
| --- | --- | --- | --- |
| Patient | Missing follow-up status | 2,587 | 21.6% |
| Patient | Missing insurance type | 240 | 2.0% |
| Patient | Missing length of stay | 240 | 2.0% |
| Financial | Missing penalty cost | 240 | 2.0% |
| Financial | Missing follow-up program cost | 240 | 2.0% |
| Care Coordination | Missing follow-up days | 180 | 1.5% |
| Care Coordination | Missing post-discharge calls | 180 | 1.5% |
| Financial | Negative penalty cost | 49 | 0.4% |

The largest quality issue is missing follow-up status. Financial fields also include missing and negative values. The cleaning workflow preserves original values, adds quality flags, and creates analysis-ready companion fields.

## Overall Readmission Pattern

- Patients analyzed: 12,000
- Readmitted within 30 days: 5,184
- Readmission rate: 43.2%

## Segment Findings

| segment_type | segment | patient_count | readmission_rate | avg_total_care_cost |
| --- | --- | --- | --- | --- |
| Chronic condition bucket | 5+ | 1,317 | 62.3% | $25.3K |
| Follow-up status | Unknown | 2,587 | 60.3% | $25.3K |
| Prior admissions bucket | 3+ | 3,225 | 57.0% | $25.2K |
| Discharge disposition | Skilled Nursing | 1,803 | 54.4% | $25.0K |
| Age group | 85+ | 949 | 54.3% | $25.4K |
| Admission type | Emergency | 7,095 | 50.9% | $25.3K |
| ED visits bucket | 2 | 3,139 | 44.5% | $25.4K |
| Primary diagnosis | Heart Failure | 2,422 | 44.2% | $25.1K |

## Recommended Visuals

- `sections/02_business_problem/images/historical_readmission_trend.svg`
- `sections/03_data_overview/images/missing_values_summary.svg`
- `sections/04_clinical_analysis/images/readmission_by_age_group.svg`
- `sections/04_clinical_analysis/images/readmission_by_chronic_condition_bucket.svg`
- `sections/04_clinical_analysis/images/readmission_by_prior_admissions.svg`
- `sections/04_clinical_analysis/images/readmission_by_discharge_disposition.svg`

## Key Findings

1. Readmission risk increases materially with chronic condition burden.
2. Prior admissions show a clear relationship with readmission risk.
3. Older age groups carry higher observed readmission rates.
4. Emergency admissions have higher readmission rates than urgent or elective admissions.
5. Unknown follow-up status has the highest observed readmission rate among follow-up categories.
6. Financial data can support ROI planning, but final estimates should use quality flags and sensitivity checks.

## Areas For Further Investigation

- Validate whether missing follow-up status reflects actual lack of follow-up or documentation gaps.
- Compare interventions within high-risk deciles to determine whether care coordination reaches the right patients.
- Validate ROI assumptions with actual implementation costs.
- Review model threshold selection with clinical operations and care coordination capacity.
