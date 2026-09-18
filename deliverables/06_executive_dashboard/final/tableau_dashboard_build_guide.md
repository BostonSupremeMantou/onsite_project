# Tableau Dashboard Build Guide

## Recommended Tool

Use Tableau as the primary dashboard tool. Power BI can use the same data model and measures as a backup implementation path.

## Primary Data Source

Connect Tableau to:

- `sections/08_executive_dashboard_walkthrough/data/dashboard_ready_extract.csv`

Optional supporting files:

- `sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_measure_definitions.csv`
- `sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv`
- `deliverables/06_executive_dashboard/final/nhn_dashboard_build_package.xlsx`

## Dashboard Purpose

This dashboard is designed for presentation use. It should help explain the full readmission problem across clinical quality, financial and capacity impact, care coordination targeting, and executive recommendations.

## Tableau Calculated Fields

Create these Tableau calculated fields:

| Field | Formula |
| --- | --- |
| Readmission Rate | `SUM([readmitted_within_30_days]) / COUNT([patient_id])` |
| High-Risk Patient | `IF [risk_decile] >= 8 THEN 1 ELSE 0 END` |
| High-Risk Patients | `SUM([High-Risk Patient])` |
| Total Care Cost | `SUM([total_care_cost_nonnegative])` |
| CMS Penalties | `SUM([penalty_cost_nonnegative])` |
| Average Risk Score | `AVG([preliminary_readmission_risk_score])` |
| Intervention Completion Count | `SUM([care_coordinator_assigned]) + SUM([follow_up_completed]) + SUM([medication_review_completed]) + SUM([home_health_referral]) + SUM([transportation_assistance_provided]) + SUM([any_post_discharge_call_flag])` |

## Page 1: Executive KPI Summary

Use this page for the opening dashboard view.

- KPI cards: readmission rate, high-risk patients, total care cost, CMS penalties, expected ROI.
- Bar chart: readmission rate by risk decile.
- Table: recommendation priority, action, and timeframe.
- Visible caveat: missing follow-up status and financial data quality issues are material.

## Page 2: Clinical Analytics

Use this page to show the clinical quality lens.

- Readmission rate by age group.
- Readmission rate by primary diagnosis.
- Readmission rate by chronic condition bucket.
- Readmission rate by prior admissions bucket.
- Readmission rate by discharge disposition.

## Page 3: Financial Analytics

Use this page to show financial and capacity impact.

- Total care cost by readmission outcome.
- CMS penalty exposure.
- Net reimbursement gap by discharge disposition.
- ROI scenario chart from `roi_scenarios.csv`.

## Page 4: Care Coordination Analytics

Use this page to support the stronger conclusion that NHN should redesign targeting and timing.

- Readmission rate by intervention.
- Intervention count distribution.
- Follow-up status and follow-up timing.
- High-risk patient coverage by intervention.
- Caveat: intervention results are observed associations, not causal estimates.

## Page 5: Executive Recommendation Center

Use this page to show all recommendations together.

- Recommendation priority matrix.
- Implementation roadmap.
- Success metrics.
- Data quality caveats.

## Modeling Guidance

Do not present one model as the sole decision engine. Use model output as one layer in a staged risk process:

1. Broad high-risk segmentation using risk deciles 8-10 and clinical rules.
2. Explainable model score for pre-discharge review.
3. Clinical review for final intervention assignment.
4. Monthly validation of recall, precision, and operational workload.

## Validation Targets

Before using screenshots in the final presentation, validate:

| Check | Expected |
| --- | --- |
| Record count | 12,000 |
| Readmission rate | 43.2% |
| Readmitted patients | 5,184 |
| High-risk patients | 3,600 |
| Total care cost | $303.1M |
| CMS penalty exposure | $21.2M |
| Unknown follow-up status | 2,587 |

## Screenshot Export

Export one screenshot per Tableau dashboard page and place them in:

- `deliverables/06_executive_dashboard/images/`

Use the same light executive template style as the Board presentation: restrained teal palette, gold divider line, clear labels, and no dense operational clutter.
