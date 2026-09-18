# Report Evidence Audit

This audit checks whether the final written deliverables are tied to project data and substantive references.

## Final Report Citation Coverage

| Report | Evidence Notes | References Used | External References |
| --- | --- | --- | --- |
| deliverables/01_project_charter/final/project_charter.md | Present | Present | EXT-1, EXT-2, EXT-3, EXT-4 |
| deliverables/02_eda_report/final/eda_report.md | Present | Present | EXT-3, EXT-4 |
| deliverables/03_model_evaluation_report/final/model_evaluation_report.md | Present | Present | EXT-7, EXT-8 |
| deliverables/04_clinical_care_coordination_report/final/clinical_care_coordination_report.md | Present | Present | EXT-5, EXT-6, EXT-7 |
| deliverables/05_financial_impact_roi_report/final/financial_impact_roi_report.md | Present | Present | EXT-1, EXT-2, EXT-4 |
| deliverables/06_executive_dashboard/final/executive_dashboard_spec.md | Present | Present | EXT-1, EXT-3, EXT-5, EXT-6, EXT-7 |
| deliverables/07_executive_board_presentation/final/executive_board_presentation_content.md | Present | Present | EXT-1, EXT-2, EXT-3, EXT-4, EXT-5, EXT-6, EXT-7, EXT-8 |

## External Reference Coverage

- Distinct external references used across final reports: 8
- External IDs used: EXT-1, EXT-2, EXT-3, EXT-4, EXT-5, EXT-6, EXT-7, EXT-8
- Minimum required by project steering: 6
- Status: Pass

## Recomputed Core Metrics

| Metric | Recomputed Value | Source |
| --- | --- | --- |
| Integrated patient records | 12,000 | data/processed/nhn_patient_level_analysis.csv |
| 30-day readmitted patients | 5,184 | data/processed/nhn_patient_level_analysis.csv |
| 30-day readmission rate | 43.2% | data/processed/nhn_patient_level_analysis.csv |
| Total care cost, nonnegative field | $303.13M | data/processed/nhn_patient_level_analysis.csv |
| CMS penalty exposure, nonnegative field | $21.25M | data/processed/nhn_patient_level_analysis.csv |
| Expanded model ROC-AUC | 0.74 | sections/05_predictive_modeling_results/data/model_metrics.csv |
| Expanded model recall | 55.3% | sections/05_predictive_modeling_results/data/model_metrics.csv |
| Risk decile 10 readmission rate | 82.3% | sections/05_predictive_modeling_results/data/risk_score_deciles.csv |
| Expected scenario avoided readmissions | 518 | sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv |
| Expected scenario net savings | $8.81M | sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv |

## Writing Controls

- Numerical claims should be traceable to `data/processed/nhn_patient_level_analysis.csv` or section-level CSV outputs.
- Care coordination intervention comparisons remain descriptive and should not be written as causal claims.
- ROI should be labeled as scenario analysis, not guaranteed savings.
- Model results should be described as planning and prioritization evidence until validated for clinical production.
