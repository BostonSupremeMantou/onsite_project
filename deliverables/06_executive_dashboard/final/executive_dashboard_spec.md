# Executive Dashboard Specification

## Dashboard Tool

Use Tableau or Power BI for the required executive dashboard. This repository includes the dashboard-ready data, KPI definitions, and page specifications needed to build the native dashboard file.

## Required Data Files

- `sections/08_executive_dashboard_walkthrough/data/dashboard_ready_extract.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_measure_definitions.csv`
- `sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv`

## Page 1: Executive KPI Summary

KPI cards:

- Readmission Rate
- High-Risk Patients
- Total Care Cost
- CMS Penalties
- Expected ROI
- Average Risk Score

Recommended visuals:

- KPI card row.
- Readmission by risk decile.
- Recommendation summary table.

## Page 2: Clinical Analytics

Recommended visuals:

- Readmission rate by age group.
- Readmission rate by diagnosis.
- Readmission rate by chronic condition bucket.
- Readmission rate by prior admissions bucket.
- Readmission rate by discharge disposition.

## Page 3: Financial Analytics

Recommended visuals:

- Total care cost by readmission outcome.
- Cost component totals.
- Net reimbursement gap by discharge disposition.
- ROI scenario chart.

## Page 4: Care Coordination Analytics

Recommended visuals:

- Readmission rate by intervention.
- Intervention count distribution.
- Follow-up timing readmission rate.
- Intervention completion KPI cards.

## Page 5: Executive Recommendation Center

Recommended visuals:

- Recommendation priority matrix.
- Implementation roadmap.
- Success metrics table.

## Suggested Calculated Measures

| Measure | Definition |
| --- | --- |
| Readmission Rate | `SUM(readmitted_within_30_days) / COUNT(patient_id)` |
| High-Risk Patients | Count of patients with `risk_decile` equal to 8, 9, or 10 |
| Total Care Cost | `SUM(total_care_cost_nonnegative)` |
| CMS Penalties | `SUM(penalty_cost_nonnegative)` |
| Average Risk Score | `AVG(preliminary_readmission_risk_score)` |
| Intervention Completion Rate | Average of the selected binary intervention field |

## Recommended Filters

- Primary diagnosis.
- Age group.
- Admission type.
- Discharge disposition.
- Insurance type.
- Risk decile.
- Readmission outcome.
- Data quality issue flag.

## Validation Checklist

- Confirm record count equals 12,000.
- Confirm readmission rate equals 43.2%.
- Confirm high-risk filters use risk deciles 8 through 10.
- Confirm financial charts use nonnegative financial fields.
- Confirm care coordination pages include the selection-bias caveat in dashboard notes or presentation narration.
