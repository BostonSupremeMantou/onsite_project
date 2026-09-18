# Executive Board Presentation Content

## Slide 1: Title

National Hospital Network Readmission Reduction Strategy

Subtitle: Clinical analytics, financial impact, care coordination, and 12-month implementation plan

## Slide 2: Executive Summary

- NHN's analytical sample readmission rate is 43.2%.
- The highest-risk groups include older patients, patients with more chronic conditions, patients with repeated prior admissions, emergency admissions, and skilled nursing discharges.
- The expanded clinical model reached ROC-AUC 0.74.
- The expected financial scenario estimates $8.81M in net savings before implementation cost validation.

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
- Largest drivers include emergency admission, skilled nursing discharge, prior admissions, chronic conditions, length of stay, and age.

## Slide 7: Risk Stratification

- Risk deciles turn model output into an operational queue.
- Deciles 8-10 should form the broad high-risk group.
- Clinical rules should add repeat admissions, high chronic burden, emergency admission, and skilled nursing discharge.

## Slide 8: Care Coordination Analysis

- Intervention comparisons show observed association, not causal impact.
- High-risk patients may receive more support, which can make raw intervention rates difficult to interpret.
- NHN should evaluate whether interventions reach the highest-risk patients early enough.

## Slide 9: Financial Impact Analysis

- Total care cost in the cleaned dataset is $303.13M.
- Nonnegative CMS penalty exposure is $21.25M.
- Financial estimates should use quality flags and scenario sensitivity.

## Slide 10: Dashboard Walkthrough

- Executive KPI Summary.
- Clinical Analytics.
- Financial Analytics.
- Care Coordination Analytics.
- Executive Recommendation Center.

## Slide 11: Strategic Recommendations

- Deploy a pre-discharge readmission risk score: Expanded clinical model ROC-AUC is 0.74 and risk deciles separate observed readmission rates.
- Prioritize emergency admissions and skilled nursing discharges for enhanced discharge review: Emergency admissions and skilled nursing discharges show elevated readmission rates.
- Close follow-up documentation and completion gaps: Unknown follow-up status has the highest observed readmission rate and 2,587 records lack follow-up status.
- Target care coordination resources to high-risk chronic disease and prior-admission groups: Patients with 5+ chronic conditions and 3+ prior admissions show materially higher readmission rates.
- Launch an executive readmission dashboard: The project requires integrated clinical, financial, and operational reporting for executive decisions.

## Slide 12: Financial Impact And ROI

| Scenario | Readmission Reduction | Avoided Readmissions | Net Savings | ROI |
| --- | --- | --- | --- | --- |
| Conservative | 5.0% | 259 | $4.28M | 4.28x |
| Expected | 10.0% | 518 | $8.81M | 5.03x |
| Optimistic | 15.0% | 778 | $13.36M | 5.34x |

## Slide 13: Implementation Roadmap

- 0-3 months: Approve dashboard KPIs, risk model governance, and readmission reduction targets.
- 0-3 months: Pilot pre-discharge risk scoring for emergency admissions and skilled nursing discharges.
- 0-3 months: Fix follow-up status documentation workflow and missing-value monitoring.
- 3-6 months: Expand targeted care coordination for high-risk chronic disease and prior-admission groups.
- 3-6 months: Build Tableau dashboard using the prepared dashboard extract.
- 6-12 months: Track ROI, readmission reduction, CMS penalty exposure, and intervention performance monthly.
- 6-12 months: Refresh and validate the risk model with new outcomes and operational feedback.

## Slide 14: Success Measures

- Readmission rate.
- High-risk patient intervention completion.
- CMS penalty exposure.
- Net savings.
- Unknown follow-up status rate.
- Model ROC-AUC and recall.

## Slide 15: Board Decision Points

- Approve a pilot for pre-discharge risk scoring.
- Approve dashboard development in Tableau.
- Approve follow-up documentation improvements.
- Validate implementation cost assumptions for ROI tracking.

## Slide 16: References And Evidence Controls

- Full citations are maintained in `REFERENCES.md`.
- Evidence rules are maintained in `EVIDENCE_STANDARDS.md`.
- Report evidence checks are summarized in `REPORT_EVIDENCE_AUDIT.md`.
- The deck should preserve data quality, association, ROI, and model validation caveats in the main narrative.

## Evidence Notes

- Slide-level numbers are calculated from the integrated NHN dataset, section-level output CSVs, and ROI scenario table [INT-3], [INT-4], [INT-5], [INT-6].
- The deck structure follows the final presentation requirements and should answer the Board's central question about reducing avoidable readmissions and creating organizational value [INT-2].
- External references support CMS context, readmission framing, care-transition rationale, discharge redesign rationale, and model-reporting caveats [EXT-1], [EXT-2], [EXT-3], [EXT-4], [EXT-5], [EXT-6], [EXT-7], [EXT-8].

## References Used

Full reference governance is maintained in `REFERENCES.md` and `EVIDENCE_STANDARDS.md`.

- [INT-1] Option 1 Healthcare Consulting Packet.pdf.
- [INT-2] Option 1 Final Presentation Requirements.pdf.
- [INT-3] NHN Patient Readmission Dataset.csv and data/cleaned/patient_readmission_clean.csv.
- [INT-4] NHN Financial Impact Dataset.csv and data/cleaned/financial_impact_clean.csv.
- [INT-5] NHN Care Coordination Dataset.csv and data/cleaned/care_coordination_clean.csv.
- [INT-6] data/processed/nhn_patient_level_analysis.csv.
- [EXT-1] Centers for Medicare & Medicaid Services. Hospital Readmissions Reduction Program. https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions-reduction-program
- [EXT-2] CMS Data. Hospital Readmissions Reduction Program. https://data.cms.gov/provider-data/topics/hospitals/hospital-readmissions-reduction-program
- [EXT-3] Elixhauser A, Steiner C. Readmissions to U.S. Hospitals by Diagnosis, 2010. HCUP Statistical Brief #153. AHRQ, 2013. https://hcup-us.ahrq.gov/reports/statbriefs/sb153.jsp
- [EXT-4] Jencks SF, Williams MV, Coleman EA. Rehospitalizations among patients in the Medicare fee-for-service program. N Engl J Med. 2009;360(14):1418-1428. doi:10.1056/NEJMsa0803563
- [EXT-5] Coleman EA, Parry C, Chalmers S, Min SJ. The care transitions intervention: results of a randomized controlled trial. Arch Intern Med. 2006;166(17):1822-1828. doi:10.1001/archinte.166.17.1822
- [EXT-6] Jack BW, Chetty VK, Anthony D, et al. A reengineered hospital discharge program to decrease rehospitalization: a randomized trial. Ann Intern Med. 2009;150(3):178-187. doi:10.7326/0003-4819-150-3-200902030-00007
- [EXT-7] Collins GS, Reitsma JB, Altman DG, Moons KGM. Transparent Reporting of a multivariable prediction model for Individual Prognosis or Diagnosis (TRIPOD): the TRIPOD statement. Ann Intern Med. 2015;162(1):55-63. doi:10.7326/M14-0697
- [EXT-8] TRIPOD Statement. TRIPOD+AI and TRIPOD 2015 resources. https://www.tripod-statement.org/
