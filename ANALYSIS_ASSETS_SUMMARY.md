# Analysis Assets Summary

Generated section-level data analysis, visualization, and presentation assets for the NHN healthcare consulting project.

## Primary Dataset

- `data/processed/nhn_patient_level_analysis.csv`

## Key Outputs

- Section-level CSV summary tables in each `sections/*/data/` folder.
- PPT-ready SVG visuals in each `sections/*/images/` folder.
- Section finding notes and presentation talking points in each `sections/*/notes/` folder.
- Tableau or Power BI dashboard-ready files in `sections/08_executive_dashboard_walkthrough/data/`.
- Tableau or Power BI build guidance in `sections/08_executive_dashboard_walkthrough/notes/tableau_powerbi_build_guide.md`.

## Current Analytical Baseline

- Patients analyzed: 12,000
- Readmission rate: 43.2%
- Expanded clinical model ROC-AUC: 0.74
- Expected scenario net savings: $8.8M

## Tableau Or Power BI Status

The project requires a Tableau or Power BI dashboard. Native Tableau or Power BI files were not generated in this repository, but the required dashboard-ready CSVs, KPI definitions, recommended pages, measures, and visual layout are prepared in section 08.

## Important Caveats

- Care coordination intervention comparisons are observed associations and should not be presented as causal effects.
- ROI scenarios use preliminary implementation cost assumptions and should be validated before final presentation.
- The predictive model is a planning baseline and should be validated before production clinical use.
