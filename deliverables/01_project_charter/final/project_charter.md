# Project Charter

## Business Problem Statement

National Hospital Network faces rising 30-day hospital readmissions that create clinical, operational, and financial pressure. The engagement packet shows readmission rates increasing from 14.2% in 2022 to 18.4% in 2025, and leadership estimates annual readmission-related costs exceed $42 million.

## Consulting Objective

The consulting team will integrate patient readmission, financial impact, and care coordination data to identify readmission drivers, build predictive risk models, evaluate current support programs, estimate financial value, and recommend a practical 12-month improvement plan.

## Stakeholders

- Executive sponsor: Chief Medical Officer.
- Board audience: National Hospital Network Board of Directors.
- Operating stakeholders: clinical operations, care coordination, discharge planning, finance, quality improvement, and analytics teams.
- End users: executive leaders, clinical managers, care coordinators, and BI/dashboard users.

## Scope Of Work

- Analyze patient-level clinical and utilization patterns.
- Assess data quality, missing values, and integration limitations.
- Build readmission risk models using pre-discharge clinical and operational fields.
- Evaluate observed care coordination activity and follow-up patterns.
- Quantify financial exposure and build ROI scenarios.
- Prepare executive dashboard inputs and Board presentation materials.

## Initial Business Hypotheses

1. Patients with more chronic conditions, prior admissions, and longer stays carry higher readmission risk.
2. Emergency admissions and skilled nursing discharges require more focused discharge planning.
3. Missing follow-up documentation may hide operational gaps.
4. Care coordination resources may not align consistently with predicted patient risk.
5. Reducing avoidable readmissions can produce measurable savings through lower readmission costs and reduced CMS penalty exposure.

## Success Metrics

- Lower 30-day readmission rate.
- Higher follow-up completion and documentation quality.
- Better intervention targeting for high-risk patients.
- Lower CMS penalty exposure.
- Positive ROI from prioritized interventions.
- Published executive dashboard with clinical, financial, and care coordination views.

## Current Analytical Baseline

- Matched patient records: 12,000
- Analytical sample readmission rate: 43.2%
- Total care cost in cleaned financial data: $303.13M
- Nonnegative CMS penalty exposure: $21.25M

## Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Missing follow-up documentation affects interpretation | Retain missing flags and include limitations in every analytical report |
| Financial fields include missing or negative values | Use nonnegative companion fields and sensitivity analysis |
| Intervention comparisons may reflect patient selection | Present care coordination findings as observed associations, not causal effects |
| Model may not be ready for clinical production | Use it as a planning baseline and require validation before deployment |
| Native Tableau build depends on local software access | Provide dashboard-ready CSVs, KPI definitions, and build guide |

## Team Roles

| Role | Responsibilities |
| --- | --- |
| Project lead | Scope, timeline, final recommendations, executive story |
| Data analyst | Data cleaning, EDA, summary tables, visual assets |
| Modeling lead | Feature set, model comparison, risk score interpretation |
| Financial analyst | Cost baseline, ROI scenarios, financial caveats |
| Dashboard lead | Tableau build, KPI definitions, dashboard QA |
| Presentation lead | Board deck, speaker notes, final delivery |

## Evidence Notes

- Engagement scope and deliverable requirements come from the client packet and final presentation requirements [INT-1], [INT-2].
- Current analytical baseline values are calculated from the integrated patient-level analysis table [INT-6].
- CMS penalty context is included as regulatory framing, not as a substitute for project financial calculations [EXT-1], [EXT-2].

## References Used

Full reference governance is maintained in `REFERENCES.md` and `EVIDENCE_STANDARDS.md`.

- [INT-1] Option 1 Healthcare Consulting Packet.pdf.
- [INT-2] Option 1 Final Presentation Requirements.pdf.
- [INT-6] data/processed/nhn_patient_level_analysis.csv.
- [EXT-1] Centers for Medicare & Medicaid Services. Hospital Readmissions Reduction Program. https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions-reduction-program
- [EXT-2] CMS Data. Hospital Readmissions Reduction Program. https://data.cms.gov/provider-data/topics/hospitals/hospital-readmissions-reduction-program
- [EXT-3] Elixhauser A, Steiner C. Readmissions to U.S. Hospitals by Diagnosis, 2010. HCUP Statistical Brief #153. AHRQ, 2013. https://hcup-us.ahrq.gov/reports/statbriefs/sb153.jsp
- [EXT-4] Jencks SF, Williams MV, Coleman EA. Rehospitalizations among patients in the Medicare fee-for-service program. N Engl J Med. 2009;360(14):1418-1428. doi:10.1056/NEJMsa0803563
