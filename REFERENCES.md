# Project Reference Library

This library defines the references that should be used across the NHN healthcare consulting reports, dashboard notes, and Board presentation. Use internal project data for analytical claims and external references for domain framing, regulatory context, care-transition evidence, and model-reporting standards.

## Internal Project References

| ID | Reference | Use In Reports | Why It Is Substantive |
| --- | --- | --- | --- |
| INT-1 | `Option 1 Healthcare Consulting Packet.pdf` | Engagement scope, client objectives, deliverable list, historical readmission trend, Board audience, NHN context | This is the client packet that defines the consulting engagement and the project problem statement. |
| INT-2 | `Option 1 Final Presentation Requirements.pdf` | Required presentation sections, dashboard requirement, expected financial and operational discussion | This is the assignment requirement document and should anchor the final deliverable structure. |
| INT-3 | `NHN Patient Readmission Dataset.csv` and `data/cleaned/patient_readmission_clean.csv` | Patient demographics, clinical risk segments, readmission outcome, missing follow-up status | These files are the primary source for clinical and readmission analysis. |
| INT-4 | `NHN Financial Impact Dataset.csv` and `data/cleaned/financial_impact_clean.csv` | Cost, reimbursement, CMS penalty, total care cost, ROI inputs | These files are the primary source for financial baseline and ROI calculations. |
| INT-5 | `NHN Care Coordination Dataset.csv` and `data/cleaned/care_coordination_clean.csv` | Follow-up timing, post-discharge calls, care coordinator assignment, medication review, home health referral, transportation assistance | These files are the primary source for care coordination analysis. |
| INT-6 | `data/processed/nhn_patient_level_analysis.csv` | Integrated EDA, risk segmentation, modeling, dashboard extract, section-level summaries | This is the joined analytical table used to calculate report metrics. |

## External References

| ID | Reference | Use In Reports | Why It Is Substantive |
| --- | --- | --- | --- |
| EXT-1 | Centers for Medicare & Medicaid Services. Hospital Readmissions Reduction Program (HRRP). `https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions-reduction-program` | CMS penalty exposure, value-based reimbursement context, why readmission reduction is financially material | CMS is the official source for HRRP policy and payment adjustment context. |
| EXT-2 | CMS Data. Hospital Readmissions Reduction Program. `https://data.cms.gov/provider-data/topics/hospitals/hospital-readmissions-reduction-program` | Public reporting and HRRP program context | CMS Data is an official program-data source for hospital readmission penalties and public reporting. |
| EXT-3 | Elixhauser A, Steiner C. *Readmissions to U.S. Hospitals by Diagnosis, 2010*. HCUP Statistical Brief #153. AHRQ, 2013. `https://hcup-us.ahrq.gov/reports/statbriefs/sb153.jsp` | 30-day all-cause readmission definition, diagnosis-specific readmission context, national readmission benchmark framing | AHRQ HCUP provides national hospital readmission statistics and explicitly defines 30-day all-cause readmissions. |
| EXT-4 | Jencks SF, Williams MV, Coleman EA. "Rehospitalizations among patients in the Medicare fee-for-service program." *New England Journal of Medicine*. 2009;360(14):1418-1428. DOI: `10.1056/NEJMsa0803563`; PMID: `19339721`. `https://pubmed.ncbi.nlm.nih.gov/19339721/` | Why readmissions are a clinical quality and cost issue; avoidable vs unavoidable readmission caveat | Highly cited peer-reviewed study on Medicare rehospitalizations and cost implications. |
| EXT-5 | Coleman EA, Parry C, Chalmers S, Min SJ. "The care transitions intervention: results of a randomized controlled trial." *Archives of Internal Medicine*. 2006;166(17):1822-1828. DOI: `10.1001/archinte.166.17.1822`; PMID: `17000937`. `https://pubmed.ncbi.nlm.nih.gov/17000937/` | Care transition redesign, coaching, cross-site communication, readmission reduction evidence | Randomized controlled trial showing lower rehospitalization rates with structured transition support. |
| EXT-6 | Jack BW, Chetty VK, Anthony D, et al. "A reengineered hospital discharge program to decrease rehospitalization: a randomized trial." *Annals of Internal Medicine*. 2009;150(3):178-187. DOI: `10.7326/0003-4819-150-3-200902030-00007`; PMID: `19189907`. `https://pubmed.ncbi.nlm.nih.gov/19189907/` | Discharge planning, medication reconciliation, follow-up appointment workflow, Project RED support | Randomized trial of a redesigned discharge program that reduced post-discharge hospital utilization. |
| EXT-7 | Collins GS, Reitsma JB, Altman DG, Moons KGM. "Transparent Reporting of a multivariable prediction model for Individual Prognosis or Diagnosis (TRIPOD): the TRIPOD statement." *Annals of Internal Medicine*. 2015;162(1):55-63. DOI: `10.7326/M14-0697`; PMID: `25560714`. `https://pubmed.ncbi.nlm.nih.gov/25560714/` | Model limitations, transparent reporting, validation caveats, threshold governance | Consensus reporting guideline for clinical prediction model studies. |
| EXT-8 | TRIPOD Statement. TRIPOD+AI and TRIPOD 2015 resources. `https://www.tripod-statement.org/` | Model governance and reporting transparency, especially when discussing predictive analytics with executives | Maintained reporting-guideline resource for prediction model transparency. |

## Citation Rule

Use bracketed IDs in deliverables, for example `[INT-6]`, `[EXT-1]`, or `[EXT-7]`. At least six distinct external references should appear across the final written report package. Every numerical project claim should also point to an internal evidence source, not only an external reference.
