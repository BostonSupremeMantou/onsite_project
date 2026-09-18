# NHN Healthcare Consulting Checklist

## Current Status

- [x] Source PDFs reviewed and summarized in `PROJECT_SUMMARY.md`.
- [x] Data dictionary reviewed.
- [x] Raw CSV files preserved without modification.
- [x] Cleaning script created at `scripts/clean_nhn_data.py`.
- [x] Cleaned CSV outputs created under `data/cleaned/`.
- [x] Integrated patient-level analysis table created at `data/processed/nhn_patient_level_analysis.csv`.
- [x] Data cleaning notes created in `DATA_CLEANING_SUMMARY.md`.
- [x] Preliminary exploratory data analysis assets generated.
- [x] Preliminary predictive models completed and compared.
- [x] Preliminary care coordination effectiveness analysis assets generated.
- [x] Preliminary financial impact and ROI scenario assets generated.
- [x] Tableau or Power BI dashboard-ready data and build guide created.
- [x] Tableau-first dashboard build package workbook created.
- [x] Deliverable workspace folders and templates created.
- [ ] Native Tableau or Power BI dashboard completed.
- [x] Final Board presentation completed.

## Data Cleaning Checklist

- [x] Standardize column names to snake_case.
- [x] Validate `PatientID` uniqueness in patient, financial, and care coordination datasets.
- [x] Validate that all three datasets contain the same 12,000 `PatientID` values.
- [x] Normalize text fields by trimming whitespace and converting blank strings to missing values.
- [x] Flag missing `insurance_type`, `follow_up_status`, and `length_of_stay_days`.
- [x] Fill missing categorical fields with `Unknown` for analysis while preserving missing flags.
- [x] Add diagnosis-median imputed `length_of_stay_days_imputed`.
- [x] Flag missing financial values.
- [x] Flag negative financial values and create `_nonnegative` companion fields.
- [x] Recompute total care cost excluding penalty using nonnegative cost components.
- [x] Add `net_reimbursement_gap` for financial analysis.
- [x] Flag missing care coordination timing and call-count fields.
- [x] Add median-imputed care coordination timing and call-count companion fields.
- [x] Add patient segmentation fields for age, chronic conditions, prior admissions, and ED visits.
- [x] Add intervention count and intervention flag fields.
- [x] Create master analysis file by joining patient, financial, and care datasets.
- [ ] Review whether imputation choices should be changed before final modeling.
- [ ] Decide whether financial records with negative source values should be excluded from ROI scenarios or handled through sensitivity analysis.

## Initial Data Quality Findings

- All three core datasets have 12,000 rows.
- All three core datasets have 12,000 unique patient IDs.
- Patient IDs fully match across patient, financial, and care coordination datasets.
- Patient dataset issues:
  - 240 missing `length_of_stay_days` values.
  - 240 missing `insurance_type` values.
  - 2,587 missing `follow_up_status` values.
- Financial dataset issues:
  - 240 missing `penalty_cost` values.
  - 240 missing `follow_up_program_cost` values.
  - Negative values appear in several financial fields and should be handled carefully in ROI analysis.
- Care coordination dataset issues:
  - 180 missing `follow_up_days_after_discharge` values.
  - 180 missing `post_discharge_calls` values.
- Target distribution:
  - 6,816 patients were not readmitted within 30 days.
  - 5,184 patients were readmitted within 30 days.
  - Readmission rate in the dataset is 43.2%.

## Final Board Presentation Section Checklist

### 1. Executive Summary

Needed content:

- Business problem in one paragraph.
- Most important clinical, operational, and financial findings.
- Three highest-priority recommendations.
- Expected clinical impact.
- Estimated financial value.
- Expected organizational impact.

Data and evidence needed:

- Overall readmission rate.
- Highest-risk patient segments.
- Most effective care coordination interventions.
- Current cost and penalty exposure.
- Conservative, expected, and optimistic ROI scenarios.

Status:

- [x] Project problem defined from PDFs.
- [x] Preliminary findings generated from EDA, modeling, intervention analysis, and ROI analysis.
- [ ] Final executive summary needs to be updated after the Tableau or Power BI dashboard is built.

### 2. Business Problem

Needed content:

- Historical readmission trend from the PDF: 14.2% in 2022, 15.8% in 2023, 16.9% in 2024, and 18.4% in 2025.
- Clinical implications of avoidable readmissions.
- Operational impact on inpatient capacity, staff, care coordinators, and patient flow.
- Financial impact, including the PDF estimate of more than $42 million in annual readmission-related cost.
- Executive concerns and working theories.

Data and evidence needed:

- Dataset-level current readmission rate.
- Readmission rate by diagnosis, admission type, discharge disposition, chronic condition burden, prior admissions, and follow-up status.
- Cost exposure from financial dataset.

Status:

- [x] PDF context captured.
- [x] Current dataset readmission rate identified.
- [x] Detailed business problem visuals generated.

### 3. Data Overview

Needed content:

- Description of the three datasets.
- Explanation of `patient_id` as the join key.
- Data preparation process.
- Data quality issues and limitations.
- Missing value and negative financial value handling.

Data and evidence needed:

- Row counts and unique patient counts.
- Missing value table.
- Join integrity summary.
- Cleaning rules from `DATA_CLEANING_SUMMARY.md`.

Status:

- [x] Data dictionary reviewed.
- [x] Cleaning outputs created.
- [x] Join integrity validated.
- [x] Data overview tables and visuals generated.

### 4. Clinical Analysis

Needed content:

- Patient demographics.
- Diagnosis categories.
- Chronic disease burden.
- Prior admissions.
- Length of stay.
- ED utilization.
- Discharge disposition.
- Readmission patterns.
- High-risk patient profiles.

Data and evidence needed:

- Readmission rate by age group.
- Readmission rate by diagnosis.
- Readmission rate by chronic condition bucket.
- Readmission rate by prior admission bucket.
- Readmission rate by ED visit bucket.
- Readmission rate by discharge disposition.
- Length of stay distributions.

Status:

- [x] Segmentation fields added in cleaned data.
- [x] Clinical EDA visuals generated.
- [x] Preliminary clinical interpretation drafted.

### 5. Predictive Modeling Results

Needed content:

- Baseline model selection and results.
- Advanced model selection and results.
- Model comparison.
- Final model choice.
- Feature importance.
- Clinical interpretation.
- Model limitations.
- How leadership should use the model operationally.

Data and evidence needed:

- Modeling dataset with pre-discharge variables.
- Train/test split or cross-validation design.
- Accuracy, precision, recall, F1 score, ROC-AUC, and confusion matrix.
- Feature importance or coefficient interpretation.
- High-risk threshold recommendation.

Status:

- [x] Analysis-ready master dataset created.
- [x] Preliminary modeling feature set defined.
- [x] Baseline model generated.
- [x] Expanded clinical model generated.
- [x] Model evaluation generated.
- [ ] Final model threshold needs to be selected for operational use.

### 6. Care Coordination Analysis

Needed content:

- Care coordinator assignment effectiveness.
- Follow-up completion effect.
- Medication review effect.
- Home health referral effect.
- Transportation assistance effect.
- Post-discharge call effect.
- Which interventions should be expanded or redesigned.

Data and evidence needed:

- Readmission rate by each intervention.
- Intervention combinations and intervention count.
- Follow-up timing relationship with readmission.
- Segment-specific intervention effectiveness for high-risk groups.

Status:

- [x] Care coordination fields cleaned.
- [x] Intervention count fields created.
- [x] Preliminary care coordination effectiveness analysis generated.
- [x] Quantitative recommendation evidence drafted.
- [ ] Causal interpretation caveat needs to remain in final presentation.

### 7. Financial Impact Analysis

Needed content:

- Current readmission costs.
- CMS penalty exposure.
- Total care costs.
- Resource utilization impact.
- Expected financial savings.

Data and evidence needed:

- Total care cost by readmission outcome.
- Penalty cost summary.
- Net reimbursement gap.
- Cost by diagnosis, risk segment, discharge disposition, and intervention status.
- Cost difference between readmitted and non-readmitted patients.

Status:

- [x] Financial fields cleaned and quality flags created.
- [x] Nonnegative companion fields created for questionable financial values.
- [x] Preliminary financial EDA generated.
- [x] Preliminary scenario assumptions generated.
- [ ] Scenario assumptions need final review before Board presentation.

### 8. Executive Dashboard Walkthrough

Needed content:

- Executive KPI Summary.
- Clinical Analytics view.
- Financial Analytics view.
- Care Coordination Analytics view.
- Executive Recommendation Center.

Dashboard KPIs needed:

- Readmission rate.
- Patient risk score.
- Total care cost.
- CMS penalties.
- ROI.
- High-risk patient count.
- Intervention completion rates.
- Expected savings by scenario.

Status:

- [x] Clean integrated data table created.
- [x] Dashboard-ready extract created.
- [x] Dashboard KPI definitions created.
- [x] Dashboard wireframe created.
- [x] Tableau or Power BI build guide created.
- [x] Tableau-first dashboard build package workbook created.
- [ ] Native Tableau or Power BI build needed.
- [ ] Dashboard screenshots needed after native dashboard build.
- [x] Dashboard walkthrough script drafted.

### 9. Strategic Recommendations

Needed content:

- Patient risk identification recommendation.
- Care coordination recommendation.
- Discharge planning recommendation.
- Medication management recommendation.
- Follow-up care recommendation.
- Resource allocation recommendation.
- Executive reporting recommendation.

Evidence needed:

- Link each recommendation to a data finding.
- Estimate clinical value.
- Estimate financial value.
- Describe implementation feasibility.

Status:

- [x] Preliminary recommendations derived from EDA, modeling, care coordination, and financial analysis.
- [ ] Final recommendation language should be reviewed after dashboard build.

### 10. Financial Impact And ROI Analysis

Needed content:

- Reduced readmission costs.
- Reduced CMS penalties.
- Reduced total care costs.
- Improved resource utilization.
- ROI.
- Expected financial return.
- Payback period if implementation costs are available or assumed.

Scenario content needed:

- Conservative scenario.
- Expected scenario.
- Optimistic scenario.
- Key assumptions behind each scenario.

Status:

- [x] Cleaned financial data available.
- [x] Preliminary scenario model generated.
- [x] Placeholder implementation cost assumptions created.
- [x] ROI outputs generated.
- [ ] Implementation cost assumptions need validation before final presentation.

### 11. Implementation Roadmap

Needed content:

- Immediate actions: 0-3 months.
- Short-term actions: 3-6 months.
- Long-term actions: 6-12 months.
- Required resources.
- Organizational challenges.
- Potential risks.
- Success measures.

Likely roadmap themes:

- Risk scoring and discharge planning workflow.
- Care coordination targeting for high-risk patients.
- Follow-up completion improvement.
- Medication review process improvement.
- Dashboard and executive reporting cadence.
- Financial monitoring and ROI tracking.

Status:

- [x] Preliminary roadmap generated.
- [ ] Roadmap needs final review after recommendations are finalized.

## Deliverables Checklist

### Deliverable 1: Project Charter

- [ ] Business problem statement.
- [ ] Project objectives.
- [ ] Stakeholders.
- [ ] Scope of work.
- [ ] Initial business hypotheses.
- [ ] Success metrics.
- [ ] Anticipated risks.
- [ ] Team roles and responsibilities.

### Deliverable 2: EDA Report

- [ ] Data quality assessment.
- [ ] Missing value analysis.
- [ ] Duplicate record check.
- [ ] Outlier detection.
- [ ] Five professional visualizations.
- [ ] Clinical findings.
- [ ] Financial findings.
- [ ] Care coordination findings.
- [ ] Initial evidence-backed hypotheses.

### Deliverable 3: Model Evaluation Report

- [ ] Baseline model.
- [ ] Advanced model.
- [ ] Performance metrics.
- [ ] Confusion matrix.
- [ ] ROC-AUC.
- [ ] Feature importance.
- [ ] Model limitations.
- [ ] Executive interpretation.

### Deliverable 4: Clinical And Care Coordination Report

- [ ] High-risk patient populations.
- [ ] Readmission trends.
- [ ] Diagnosis category analysis.
- [ ] Chronic disease burden analysis.
- [ ] Care coordinator effectiveness.
- [ ] Follow-up completion analysis.
- [ ] Medication review analysis.
- [ ] Home health referral analysis.
- [ ] Transportation assistance analysis.
- [ ] Intervention recommendations.

### Deliverable 5: Financial Impact And ROI Report

- [ ] Current financial baseline.
- [ ] Readmission cost reduction opportunity.
- [ ] CMS penalty reduction opportunity.
- [ ] Total care cost opportunity.
- [ ] Implementation cost assumptions.
- [ ] Conservative scenario.
- [ ] Expected scenario.
- [ ] Optimistic scenario.
- [ ] ROI and payback period.

### Deliverable 6: Executive Dashboard

- [ ] Executive KPI Summary.
- [ ] Clinical Analytics.
- [ ] Financial Analytics.
- [ ] Care Coordination Analytics.
- [ ] Executive Recommendation Center.

### Deliverable 7: Executive Board Presentation

- [x] Executive summary.
- [x] Business problem.
- [x] Data overview.
- [x] Key findings.
- [x] Predictive modeling results.
- [x] Clinical analysis.
- [x] Financial analysis.
- [x] Care coordination analysis.
- [x] Dashboard walkthrough.
- [x] Strategic recommendations.
- [x] Implementation roadmap.
- [x] Expected clinical impact.
- [x] Expected financial value.
- [x] ROI.

## Immediate Next Analysis Tasks

- [ ] Build EDA summary tables from `data/processed/nhn_patient_level_analysis.csv`.
- [ ] Create visuals for readmission rate by patient segment.
- [ ] Create visuals for readmission rate by care coordination intervention.
- [ ] Create financial baseline summary using nonnegative financial fields.
- [ ] Define the modeling feature set.
- [ ] Train baseline logistic regression model.
- [ ] Train advanced tree-based model.
- [ ] Select model threshold with recall, precision, and operational capacity in mind.
- [ ] Build ROI scenarios.
- [ ] Draft Board presentation storyline from data-backed findings.
