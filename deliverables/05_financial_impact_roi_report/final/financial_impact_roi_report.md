# Financial Impact And ROI Analysis Report

## Executive Summary

NHN's financial opportunity comes from reducing avoidable readmission costs and CMS penalty exposure. The expected scenario estimates 518 avoided readmissions, $10.56M in gross savings, $8.81M in net savings, and ROI of 5.03x before final implementation cost validation.

## Financial Baseline By Readmission Outcome

| readmission_label | patient_count | avg_total_care_cost | avg_readmission_cost | avg_penalty_cost | avg_net_reimbursement_gap | total_care_cost | total_penalty_cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Not readmitted | 6,816 | $25.25K | $18.58K | $1.82K | $11.33K | $172.11M | $12.11M |
| Readmitted | 5,184 | $25.27K | $18.63K | $1.81K | $11.33K | $131.01M | $9.14M |

## Cost Components

| component | amount |
| --- | --- |
| Follow-up program cost | $5.3M |
| CMS penalty cost | $21.25M |
| Length-of-stay cost | $74.6M |
| Readmission cost | $223.12M |

## ROI Scenarios

| scenario | readmission_reduction_rate | implementation_cost_assumption | avoided_readmissions | gross_savings | net_savings | roi |
| --- | --- | --- | --- | --- | --- | --- |
| Conservative | 5.0% | $1.0M | 259 | $5.28M | $4.28M | 4.28 |
| Expected | 10.0% | $1.75M | 518 | $10.56M | $8.81M | 5.03 |
| Optimistic | 15.0% | $2.5M | 778 | $15.86M | $13.36M | 5.34 |

## Scenario Assumptions

- Conservative: 5.0% readmission reduction and $1.0M implementation cost.
- Expected: 10.0% readmission reduction and $1.75M implementation cost.
- Optimistic: 15.0% readmission reduction and $2.5M implementation cost.
- Average avoided value per readmission uses readmission cost plus nonnegative penalty cost among readmitted patients.

## Interpretation

The expected scenario suggests that reducing avoidable readmissions can create meaningful financial value. The Board should treat these figures as planning estimates until implementation costs, intervention capacity, and avoidable-readmission assumptions are validated.

## Limitations

- Financial fields include missing and negative values, so the analysis uses nonnegative companion fields.
- Scenario implementation costs are placeholders.
- The model does not yet distinguish avoidable from unavoidable readmissions.
- ROI should be refreshed after dashboard implementation and operational pilot results.

## Evidence Notes

- Financial baseline, cost components, and ROI scenario values are calculated from the cleaned financial data and integrated patient-level analysis table [INT-4], [INT-6].
- CMS HRRP references provide policy context for why penalty exposure matters. They do not validate NHN-specific savings estimates [EXT-1], [EXT-2].
- Readmission-cost framing is supported by peer-reviewed Medicare readmission literature, while ROI remains a project scenario estimate [EXT-4].

## References Used

Full reference governance is maintained in `REFERENCES.md` and `EVIDENCE_STANDARDS.md`.

- [INT-4] NHN Financial Impact Dataset.csv and data/cleaned/financial_impact_clean.csv.
- [INT-6] data/processed/nhn_patient_level_analysis.csv.
- [EXT-1] Centers for Medicare & Medicaid Services. Hospital Readmissions Reduction Program. https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions-reduction-program
- [EXT-2] CMS Data. Hospital Readmissions Reduction Program. https://data.cms.gov/provider-data/topics/hospitals/hospital-readmissions-reduction-program
- [EXT-4] Jencks SF, Williams MV, Coleman EA. Rehospitalizations among patients in the Medicare fee-for-service program. N Engl J Med. 2009;360(14):1418-1428. doi:10.1056/NEJMsa0803563
