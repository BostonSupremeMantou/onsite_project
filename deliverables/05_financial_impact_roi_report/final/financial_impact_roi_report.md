# Financial Impact And ROI Analysis Report

## Executive Summary

NHN's financial opportunity comes from reducing avoidable readmission costs and CMS penalty exposure. The expected scenario estimates 518 avoided readmissions, $10.6M in gross savings, $8.8M in net savings, and ROI of 5.03x before final implementation cost validation.

## Financial Baseline By Readmission Outcome

| readmission_label | patient_count | avg_total_care_cost | avg_readmission_cost | avg_penalty_cost | avg_net_reimbursement_gap | total_care_cost | total_penalty_cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Not readmitted | 6,816 | $25.3K | $18.6K | $1.8K | $11.3K | $172.1M | $12.1M |
| Readmitted | 5,184 | $25.3K | $18.6K | $1.8K | $11.3K | $131.0M | $9.1M |

## Cost Components

| component | amount |
| --- | --- |
| Follow-up program cost | $5.3M |
| CMS penalty cost | $21.2M |
| Length-of-stay cost | $74.6M |
| Readmission cost | $223.1M |

## ROI Scenarios

| scenario | readmission_reduction_rate | implementation_cost_assumption | avoided_readmissions | gross_savings | net_savings | roi |
| --- | --- | --- | --- | --- | --- | --- |
| Conservative | 5.0% | $1.0M | 259 | $5.3M | $4.3M | 4.28 |
| Expected | 10.0% | $1.8M | 518 | $10.6M | $8.8M | 5.03 |
| Optimistic | 15.0% | $2.5M | 778 | $15.9M | $13.4M | 5.34 |

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
