# Executive Board Presentation Content

## Slide 1: Title

National Hospital Network Readmission Reduction Strategy

Subtitle: Clinical analytics, financial impact, care coordination, and 12-month implementation plan

## Slide 2: Executive Summary

- NHN's analytical sample readmission rate is 43.2%.
- The highest-risk groups include older patients, patients with more chronic conditions, patients with repeated prior admissions, emergency admissions, and skilled nursing discharges.
- The expanded clinical model reached ROC-AUC 0.74.
- The recommendation uses separate clinical, financial, capacity, care coordination, and data quality lenses rather than one single emphasis.
- The expected financial scenario estimates $8.8M in net savings before implementation cost validation.

## Slide 3: Business Problem

- Historical readmissions rose from 14.2% in 2022 to 18.4% in 2025.
- Leadership estimates annual readmission-related costs exceed $42 million.
- Rising readmissions affect patient outcomes, inpatient capacity, care coordination workload, and CMS penalty exposure.

## Slide 4: Data Overview

- Three datasets were integrated through `patient_id`.
- The merged analysis table contains 12,000 matched patients.
- Main limitations are missing follow-up status and financial field quality issues.

## Slide 5: Clinical Analysis

- Risk increases with age, chronic condition burden, prior admissions, and skilled nursing discharge.
- Emergency admissions have higher readmission rates than urgent or elective admissions.
- Unknown follow-up status carries the highest observed readmission rate among follow-up categories.

## Slide 6: Predictive Modeling Results

- The baseline model uses numeric clinical variables.
- The expanded model adds categorical clinical and discharge variables.
- The expanded model performs better and remains explainable for leadership.
- NHN should use a staged model and clinical-rule workflow rather than one model as the sole decision engine.
- Risk scoring should support broad high-risk coverage, especially deciles 8-10 and clinically elevated segments.
- Largest drivers include emergency admission, skilled nursing discharge, prior admissions, chronic conditions, length of stay, and age.

## Slide 7: Care Coordination Analysis

- Intervention comparisons show observed association, not causal impact.
- Selection bias makes raw intervention comparisons difficult to interpret.
- NHN should redesign targeting and timing so interventions reach high-risk patients earlier and more consistently.
- Intervention completion should be tracked as part of the dashboard.

## Slide 8: Financial Impact Analysis

- Total care cost in the cleaned dataset is $303.1M.
- Nonnegative CMS penalty exposure is $21.2M.
- Financial estimates should use quality flags and scenario sensitivity.

## Slide 9: Dashboard Walkthrough

- Executive KPI Summary for presentation-level status.
- Clinical Analytics.
- Financial Analytics.
- Care Coordination Analytics.
- Executive Recommendation Center.

## Slide 10: Strategic Recommendations

- Deploy a staged readmission risk workflow: Expanded clinical model ROC-AUC is 0.74 and risk deciles separate observed readmission rates, but model output should be combined with clinical rules and review.
- Prioritize emergency admissions and skilled nursing discharges for enhanced discharge review: Emergency admissions and skilled nursing discharges show elevated readmission rates.
- Close follow-up documentation and completion gaps: Unknown follow-up status has the highest observed readmission rate and 2,587 records lack follow-up status.
- Target care coordination resources to high-risk chronic disease and prior-admission groups: Patients with 5+ chronic conditions and 3+ prior admissions show materially higher readmission rates.
- Launch an executive readmission dashboard: The project requires integrated clinical, financial, and operational reporting for executive decisions.

## Slide 11: Financial Impact And ROI

| Scenario | Readmission Reduction | Avoided Readmissions | Net Savings | ROI |
| --- | --- | --- | --- | --- |
| Conservative | 5.0% | 259 | $4.3M | 4.28x |
| Expected | 10.0% | 518 | $8.8M | 5.03x |
| Optimistic | 15.0% | 778 | $13.4M | 5.34x |

## Slide 12: Implementation Roadmap

- 0-3 months: Approve dashboard KPIs, risk model governance, and readmission reduction targets.
- 0-3 months: Pilot broad high-risk coverage using deciles 8-10, emergency admissions, skilled nursing discharges, chronic disease burden, and prior admissions.
- 0-3 months: Fix follow-up status documentation workflow and missing-value monitoring.
- 3-6 months: Expand targeted care coordination for high-risk chronic disease and prior-admission groups.
- 3-6 months: Build Tableau or Power BI dashboard using the prepared dashboard extract.
- 6-12 months: Track ROI, readmission reduction, CMS penalty exposure, and intervention performance monthly.
- 6-12 months: Refresh and validate the risk model with new outcomes and operational feedback.

## Slide 13: Success Measures

- Readmission rate.
- High-risk patient intervention completion.
- CMS penalty exposure.
- Net savings.
- Unknown follow-up status rate.
- Model ROC-AUC and recall.

## Slide 14: Board Decision Points

- Approve a broad high-risk readmission reduction pilot.
- Approve staged model governance across scoring, clinical rules, and care team review.
- Approve dashboard development in Tableau.
- Approve follow-up documentation improvements.
- Validate implementation cost assumptions for ROI tracking.

## Slide 15: Appendix

- Data quality limitations.
- Model metric details.
- ROI assumptions.
- Care coordination caveat.
