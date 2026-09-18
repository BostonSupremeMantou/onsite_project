# NHN Healthcare Consulting Project Summary

## Source PDFs

- `Option 1 Healthcare Consulting Packet.pdf`
- `Option 1 Final Presentation Requirements.pdf`

## Executive Summary

National Hospital Network (NHN) is facing a sustained increase in 30-day hospital readmissions. The readmission rate rose from 14.2% in 2022 to 18.4% in 2025, and leadership estimates annual readmission-related costs exceed $42 million.

The consulting project is to integrate clinical, financial, and care coordination data to explain why readmissions are increasing, identify high-risk patients before discharge, evaluate which interventions work, estimate the financial value of reducing avoidable readmissions, build an executive dashboard, and recommend a practical 12-month action plan for the Board of Directors.

Important note: the PDFs define the project background, required analyses, deliverables, and presentation expectations. They do not contain the actual analytical findings. Real conclusions need to come from the CSV datasets.

## Core Board Question

The final presentation must answer one central executive question:

> How can NHN use clinical analytics, predictive modeling, financial analysis, and care coordination intelligence to reduce avoidable hospital readmissions, improve patient outcomes, optimize operational performance, and create measurable long-term organizational value?

Every analysis, visualization, model, dashboard, financial estimate, and recommendation should support this question.

## Client Background

NHN is described as one of the largest integrated healthcare systems in the United States.

Key facts:

- 42 hospitals
- More than 300 outpatient facilities
- Operations across 11 states
- 2.3 million patients annually
- 48,000 employees
- Integrated care coordination programs
- Enterprise Electronic Health Record system

NHN's strategic priorities include reducing avoidable readmissions, improving outcomes through predictive analytics and evidence-based decision making, improving resource utilization and patient flow, and strengthening population health initiatives.

## Business Problem

NHN has invested in quality improvement, discharge planning, care coordination, and patient follow-up services, but readmission rates continue to rise across multiple patient populations and service lines.

The problem is framed as clinical, operational, and financial:

- Clinical: avoidable readmissions may signal gaps in discharge planning, medication management, chronic disease management, or follow-up care.
- Operational: rising readmissions strain inpatient resources, staff capacity, patient flow, and care coordination teams.
- Financial: readmissions increase care costs, CMS reimbursement penalties, administrative costs, staffing needs, and reduce operational efficiency.
- Strategic: leadership currently lacks an integrated view across patient outcomes, financial impact, and care coordination activity.

## Working Theories To Test

The PDFs identify several executive hypotheses that the consulting team should investigate:

1. Discharge planning may not adequately prepare patients for recovery.
2. Care coordination programs may not be effectively targeted toward high-risk patients.
3. Chronic disease management may need improvement.
4. Financial resources may not be directed toward the highest-impact interventions.
5. Patient follow-up and community support may influence readmission risk.
6. Organizational decision-making lacks integrated clinical, financial, and operational analytics.

## Provided Datasets

| Dataset | Purpose | Key Content | Main Use |
| --- | --- | --- | --- |
| Patient Readmission Dataset | Primary clinical dataset | Patient ID, age, gender, insurance type, primary diagnosis, chronic conditions, prior admissions, length of stay, admission type, discharge disposition, ED visits, follow-up status, readmitted within 30 days | EDA, clinical analysis, patient risk stratification, predictive modeling |
| Financial Impact Dataset | Financial consequence dataset | Readmission cost, reimbursement amount, penalty cost, length-of-stay cost, follow-up program cost, total care cost | Cost analysis, CMS penalty analysis, ROI estimation, scenario modeling |
| Care Coordination Dataset | Operational intervention dataset | Care coordinator assignment, follow-up completion, follow-up days after discharge, medication review, home health referral, transportation assistance, post-discharge calls | Intervention effectiveness, care coordination performance, operational improvement |

The datasets should be treated as complementary views of the same organizational problem rather than separate analyses. The expected story should connect clinical risk, financial impact, and care coordination effectiveness.

## Required Executive Questions

The engagement should provide evidence-based answers to these questions:

1. Which patients are most likely to be readmitted?
2. What factors contribute most significantly to readmission risk?
3. Can NHN accurately identify high-risk patients before discharge?
4. Which patient populations should receive additional care coordination and intervention?
5. Which care coordination interventions appear most effective?
6. What financial savings could be achieved by reducing avoidable readmissions?
7. What strategic initiatives should Executive Leadership prioritize during the next 12 months?

## Required Analysis Workstreams

### Exploratory Data Analysis

Required activities:

- Data quality assessment
- Missing value analysis
- Duplicate record identification
- Outlier detection
- Patient segmentation
- Readmission trend analysis
- Clinical diagnosis analysis
- Care coordination analysis
- Financial impact exploration
- Operational trend analysis

The EDA should summarize major trends, unexpected findings, data limitations, and initial business hypotheses.

### Clinical Analysis

The clinical workstream should evaluate:

- Patient demographics
- Primary diagnoses
- Chronic disease burden
- Length of stay
- Prior admissions
- Emergency department utilization
- Readmission patterns
- High-risk patient populations
- Opportunities for earlier intervention

### Predictive Modeling

The project requires predictive models that identify patients at high risk of readmission before discharge.

Expected modeling approach:

- Establish a baseline model, such as logistic regression or decision tree.
- Compare at least one advanced model, such as random forest, gradient boosting, or XGBoost.
- Evaluate models using accuracy, precision, recall, F1 score, ROC-AUC, and confusion matrix.
- Explain feature importance and business meaning.
- Select a final model based on both performance and clinical explainability.

The PDFs emphasize that leadership is not looking for the most technically sophisticated model. The selected model must be understandable, explainable, and appropriate for use in a clinical environment.

### Care Coordination Analysis

The care coordination workstream should evaluate:

- Care coordinator assignment
- Follow-up completion
- Medication review
- Home health referrals
- Transportation assistance
- Post-discharge communication

The goal is to identify which interventions reduce readmission risk, which should be expanded, which should be redesigned, and which provide the greatest clinical value.

### Financial Impact And ROI Analysis

The financial workstream should estimate:

- Current readmission costs
- CMS reimbursement penalties
- Total care costs
- Resource utilization impact
- Intervention costs
- Cost savings from reduced readmissions
- Expected financial return
- Return on Investment
- Payback period, where possible

Financial results should be presented under conservative, expected, and optimistic scenarios.

### Operational Analysis

The operational workstream should evaluate:

- Resource utilization
- Patient flow
- Care coordination efficiency
- Follow-up performance
- Clinical workflow effectiveness

The goal is to explain how operational improvements could reduce avoidable readmissions while minimizing disruption to care delivery.

## Required Deliverables

### Deliverable 1: Project Charter

Should include:

- Business problem statement
- Project objectives
- Stakeholders
- Scope of work
- Initial business hypotheses
- Success metrics
- Anticipated risks
- Team roles and responsibilities

### Deliverable 2: EDA Report

Should cover data quality, clinical analysis, financial analysis, care coordination analysis, and trend analysis.

Minimum requirements:

- Five professional visualizations
- Key findings
- Areas requiring further investigation
- Initial business hypotheses supported by evidence

### Deliverable 3: Model Evaluation Report

Should include:

- Baseline model
- Advanced model
- Rationale for model selection
- Performance metrics
- Feature importance
- Variable interpretation
- Model limitations
- Business implications

### Deliverable 4: Clinical And Care Coordination Analysis Report

Should include:

- High-risk patient populations
- Readmission trends
- Diagnosis categories
- Chronic disease burden
- Care coordinator effectiveness
- Follow-up completion
- Medication review
- Home health referrals
- Transportation assistance
- Post-discharge communication
- Recommendations for which interventions to expand or redesign

### Deliverable 5: Financial Impact And ROI Analysis Report

Should estimate:

- Reduced readmission costs
- Reduced CMS penalties
- Reduced total care costs
- Improved resource utilization
- Increased operational efficiency
- Implementation costs
- Expected financial benefits
- ROI
- Conservative, expected, and optimistic scenarios

### Deliverable 6: Executive Dashboard

The dashboard should be built in Tableau or Power BI and should support executive decision-making.

Required sections:

- Executive KPI Summary: readmission rate, patient risk score, total care cost, CMS penalties, ROI
- Clinical Analytics: patient risk profiles, diagnosis categories, chronic disease burden, readmission trends
- Financial Analytics: readmission costs, financial impact, CMS penalties, resource utilization
- Care Coordination Analytics: follow-up completion, care coordinator assignment, medication reviews, home health referrals, transportation assistance
- Executive Recommendation Center: priority recommendations, expected clinical improvements, expected financial value, estimated ROI, implementation priorities

### Deliverable 7: Executive Board Presentation

The presentation must translate technical findings into executive-level recommendations. It should convince leadership that the recommendations are practical, financially justified, clinically meaningful, and capable of improving patient outcomes.

## Final Presentation Required Structure

The Final Board Presentation Requirements Guide expects these sections:

1. Executive Summary
2. Business Problem
3. Data Overview
4. Clinical Analysis
5. Predictive Modeling Results
6. Care Coordination Analysis
7. Financial Impact Analysis
8. Executive Dashboard Walkthrough
9. Strategic Recommendations
10. Financial Impact And ROI Analysis
11. Implementation Roadmap

The implementation roadmap should include:

- Immediate actions: 0-3 months
- Short-term actions: 3-6 months
- Long-term actions: 6-12 months
- Required resources
- Organizational challenges
- Potential risks
- Success measures

## Recommendation Areas

Strategic recommendations should address:

- Patient risk identification
- Care coordination
- Discharge planning
- Medication management
- Follow-up care
- Resource allocation
- Financial management
- Executive reporting and dashboards

Recommendations must be:

- Data-driven
- Clinically appropriate
- Financially justified
- Operationally feasible
- Patient-centered
- Realistic to implement
- Aligned with NHN's strategic priorities

## Constraints

The PDFs emphasize several practical constraints:

- Budget: recommendations must have measurable business value and clear ROI.
- Staffing: NHN faces shortages among nurses, physicians, care coordinators, case managers, social workers, and primary care providers.
- Regulatory compliance: recommendations must account for HIPAA, CMS HRRP, Medicare Conditions of Participation, patient privacy, and healthcare quality reporting.
- Technology: recommendations should leverage existing EHR, care coordination, population health, reporting, and BI platforms where practical.
- Patient experience: recommendations should improve care without harming patient trust or experience.
- Operational disruption: implementation should minimize disruption to clinical workflows and provider workload.
- Data limitations: missing values, incomplete records, incomplete care coordination documentation, financial reporting inconsistencies, and variability across facilities must be documented.
- Timeline: recommended initiatives should be achievable within 12 months or include a phased plan.

## Success Metrics

Leadership will evaluate the project across five dimensions.

Clinical outcomes:

- Reduced readmission rate
- Improved patient outcomes
- Improved chronic disease management
- Improved follow-up
- Improved medication management
- Improved discharge planning
- Improved continuity of care

Financial outcomes:

- Reduced CMS penalties
- Reduced readmission costs
- Reduced total care costs
- Improved resource utilization
- Increased operational efficiency
- Positive ROI

Operational outcomes:

- Improved care coordination
- Better intervention effectiveness
- Improved patient flow
- Better allocation of clinical resources
- Improved executive decision-making through analytics

Analytics outcomes:

- Accurate predictive models
- Clearly interpreted model results
- Executive-ready dashboards
- Effective patient risk stratification
- Meaningful care coordination analysis
- Financial impact assessment
- Actionable business recommendations

Executive communication outcomes:

- Translate technical findings into business language
- Prioritize recommendations by patient and organizational value
- Defend recommendations with data evidence
- Balance analytical rigor with practical implementation
- Communicate clearly to non-technical stakeholders

## Practical Execution Plan

A strong project sequence would be:

1. Read the data dictionary and validate schemas across all CSV files.
2. Clean and profile each dataset: missing values, duplicates, outliers, categorical consistency, and numeric ranges.
3. Define the core target variable: `readmitted_within_30_days` or its equivalent in the dataset.
4. Build EDA visuals around readmission rate, diagnosis, age, chronic conditions, prior admissions, length of stay, follow-up status, care coordination, and costs.
5. Join or align datasets around patient or encounter identifiers where possible.
6. Develop baseline and advanced models for readmission risk.
7. Evaluate model performance with special attention to recall and precision, since missing high-risk patients may be clinically costly.
8. Interpret model drivers in business language for executives.
9. Compare intervention outcomes across follow-up, medication review, home health, transportation, and post-discharge communication.
10. Build conservative, expected, and optimistic financial scenarios for avoidable readmission reduction.
11. Convert analytical findings into a prioritized 12-month roadmap.
12. Build the executive dashboard and align its tabs to the required presentation sections.

## Suggested Board-Level Storyline

The final presentation should not read like a technical model report. It should tell a business story:

1. NHN's readmission trend is worsening and creates measurable patient, operational, and financial risk.
2. Integrated data analysis can reveal which patients are highest risk and why.
3. Predictive modeling can support earlier intervention before discharge.
4. Care coordination analysis can show which interventions create the greatest clinical value.
5. Financial analysis can estimate the value of reducing avoidable readmissions.
6. The dashboard gives leadership a repeatable way to monitor risk, costs, interventions, and ROI.
7. The recommendations should prioritize achievable, high-value initiatives that fit NHN's staffing, regulatory, technology, and operational constraints.

## Key Reminder

The Board does not want a deep technical walkthrough of algorithms. They want clear answers, quantified impact, and practical recommendations. The project should use data science as a decision-making tool, not as the main story.
