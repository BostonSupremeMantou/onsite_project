# Tableau Or Power BI Build Guide

## Requirement

The project requires an executive dashboard using Tableau or Power BI. This repository now includes dashboard-ready CSV files, but it does not contain a native Tableau workbook (`.twb` or `.twbx`) or Power BI report (`.pbix`).

## Recommended Data Files

- `sections/08_executive_dashboard_walkthrough/data/dashboard_ready_extract.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_measure_definitions.csv`
- `sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv`

## Recommended Dashboard Pages

### Executive KPI Summary

Use KPI cards for:

- Readmission Rate.
- High-Risk Patients.
- Total Care Cost.
- CMS Penalties.
- Expected ROI.

### Clinical Analytics

Recommended visuals:

- Readmission rate by age group.
- Readmission rate by diagnosis.
- Readmission rate by chronic condition bucket.
- Readmission rate by prior admissions bucket.
- Risk decile readmission rate.

### Financial Analytics

Recommended visuals:

- Total care cost by readmission outcome.
- Cost component totals.
- Net reimbursement gap by discharge disposition.
- ROI scenarios.

### Care Coordination Analytics

Recommended visuals:

- Readmission rate by intervention.
- Intervention completion rates.
- Readmission rate by intervention count.
- Follow-up timing analysis.

### Executive Recommendation Center

Recommended visuals:

- Recommendation priority matrix.
- Implementation roadmap.
- Success metrics table.

## Suggested Calculated Measures

- Readmission Rate: `SUM(readmitted_within_30_days) / COUNT(patient_id)`
- Total Care Cost: `SUM(total_care_cost_nonnegative)`
- CMS Penalties: `SUM(penalty_cost_nonnegative)`
- High-Risk Patients: `COUNT(patient_id)` filtered to `risk_decile` in 8, 9, or 10
- Average Risk Score: `AVG(preliminary_readmission_risk_score)`
- Intervention Completion Rate: average of selected binary intervention fields

## Suggested Filters

- Primary diagnosis.
- Age group.
- Admission type.
- Discharge disposition.
- Insurance type.
- Risk decile.
- Readmission outcome.
- Data quality issue flag.

## Practical Recommendation

Use Tableau or Power BI for the final submitted dashboard. Use the SVG visuals in each section folder as backup presentation assets or as quick slide visuals if the live dashboard is not ready.
