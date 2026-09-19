# Team Presentation Script

Meds Counsulting LLC  
Saturday submission  
Total target time: 12-13 minutes, with 2-3 minutes left for transitions or questions.

## 1. Can He - Project Lead and Story

Slide 1: National Hospital Network project charter  
Target time: 1.5 minutes

Good morning everyone. We are Meds Counsulting LLC, and today we are presenting our readmission analytics project for National Hospital Network, or NHN.

NHN is a large integrated healthcare system with 42 hospitals, more than 300 outpatient sites, operations across 11 states, and about 2.3 million patients served each year. Because of that scale, even a small increase in readmissions can create a major clinical, operational, and financial challenge.

The business problem is that 30-day readmissions are rising despite investment in discharge planning, care coordination, and follow-up services. The readmission rate increased from 14.2 percent in 2022 to 18.4 percent in 2025, and leadership estimates more than 42 million dollars in annual cost exposure.

Our working hypothesis is that readmissions are rising because high-risk patients are not consistently matched to the right post-discharge support. We tested this through data analysis, predictive modeling, financial impact analysis, care coordination review, and ethical governance considerations.

I will now hand it over to Belal to walk through the initial data analysis.

## 2. Belal Glab - Data Preparation and EDA

Slide 2: Data analysis snapshot  
Target time: 1.5 minutes

Thank you, Can. For the data analysis, we started by checking the quality and structure of the dataset before moving into deeper modeling.

We analyzed 12,000 patients, and the overall 30-day readmission rate in the cleaned data is 43.2 percent. The first important data issue is missing follow-up status. Follow-up status is missing for 2,587 patients, or 21.6 percent of the dataset. This matters because follow-up status is directly connected to the care transition process.

We also checked outliers and quality flags. Length of stay has 191 outlier records, total care cost has 72 outlier records, and there are 49 records with negative penalty cost. These issues do not make the data unusable, but they do tell us that follow-up and financial fields need validation before final decisions.

The key takeaway from this slide is that the data is strong enough to support analysis, but we need to treat follow-up documentation and financial estimates carefully.

Next, Jingyi will explain what the data shows from a clinical risk perspective.

## 3. Jingyi Cao - Clinical Risk Analysis

Slide 2 and Slide 4: Clinical risk patterns and business insights  
Target time: 1.5 minutes

Building on the data review, the clinical risk patterns show that readmission risk is not evenly distributed across patients.

The highest-risk groups are clinically intuitive. Patients with five or more chronic conditions have a readmission rate of about 62.3 percent. Patients with unknown follow-up status have a readmission rate of about 60.3 percent. Patients with three or more prior admissions, skilled nursing discharges, and emergency admissions also show elevated readmission rates.

The correlation results support the same direction. Prior admissions and chronic conditions show the strongest positive relationship with readmission, followed by length of stay and age.

From a clinical perspective, this suggests that NHN should not treat all patients as one average group. The opportunity is to identify patients with higher risk before discharge and focus care coordination resources on those groups.

This also creates one unexpected finding: unknown follow-up status is not just a data issue. It may also signal a real care-transition visibility gap.

Now Santosh will explain the analytical approach and modeling logic.

## 4. Santosh Kumar Chantati - Predictive Modeling

Slide 3: Analytical approach  
Target time: 1.5 minutes

Thank you, Jingyi. Our analytical approach has three main parts: regression analysis, customer segmentation, and market basic analysis.

First, regression analysis helps us quantify which factors are associated with readmission. This is important because many risk factors overlap. For example, older patients may also have more chronic conditions, more prior admissions, or longer hospital stays. Regression helps us understand which variables still matter after accounting for that overlap.

Second, customer segmentation helps translate the model into action. In this healthcare context, segmentation means grouping patients by chronic burden, prior admissions, discharge setting, and follow-up status. That allows NHN to focus care coordination on the patients most likely to benefit.

Third, market basic analysis gives context. It helps compare patterns across discharge types, care settings, and financial scenarios.

The model performance evidence supports this approach. The expanded clinical model improves ROC-AUC to about 0.74, which gives NHN a stronger basis for risk-tier decisions.

Next, Jeevan will connect these insights to business value and ROI.

## 5. Jeevan-Kumar Mittapalli - Financial Impact and ROI

Slide 4 and Slide 5: Business value, cost, and expected benefits  
Target time: 1.5 minutes

Thank you, Santosh. From a business perspective, the main question is whether the analysis can lead to measurable value for NHN.

On Slide 4, the risk decile chart shows that the model meaningfully separates patients by readmission risk. Readmission rates increase from 11.8 percent in the lowest decile to 82.3 percent in the highest decile. This means the model can help NHN identify where intervention is most needed.

The ROI scenario then translates that clinical opportunity into business value. In the expected case, a 10 percent reduction in readmissions avoids about 518 readmissions. The estimated implementation cost is 1.75 million dollars, and the expected net savings are about 8.81 million dollars. That produces an estimated ROI of 5.03 times.

These numbers should be treated as planning estimates, not final budget commitments. Finance should validate the cost, penalty, and intervention assumptions before implementation.

Now Adarsh will explain how these recommendations can be implemented operationally.

## 6. Adarsh Pravinbhai Patel - Care Coordination Operations

Slide 5: Recommendations and implementation timeline  
Target time: 1.5 minutes

Thank you, Jeevan. The recommendations are organized into short-term actions and long-term strategy.

In the short term, NHN should pilot pre-discharge readmission risk scoring for emergency admissions and skilled nursing discharges. These groups show elevated risk, so they are a practical starting point. NHN should also close follow-up documentation and completion gaps because unknown follow-up status is both a data quality issue and a potential workflow issue.

The third short-term action is to approve dashboard KPIs and readmission reduction targets. This creates a shared definition of success before the pilot expands.

In the longer term, NHN should expand care coordination for high-risk chronic disease and repeat-admission groups. NHN should also track ROI, penalty exposure, intervention performance, and model performance monthly.

The timeline is staged: 0 to 3 months for pilot and workflow fixes, 3 to 6 months for expansion and dashboard rollout, and 6 to 12 months for ROI tracking and model refresh.

Finally, Sam will cover ethical considerations and responsible use.

## 7. Sam-Aquila Siddani - Dashboard, Recommendations, and Ethical Considerations

Slide 6: Ethical considerations  
Target time: 1.5 minutes

Thank you, Adarsh. The final slide focuses on ethical considerations because a readmission model affects patient care decisions.

The first issue is algorithmic bias. If historical data reflects unequal access to care or documentation gaps, the model may perform differently across patient groups. NHN should monitor performance by relevant groups such as age, diagnosis, discharge type, and insurance where appropriate.

The second issue is patient privacy. The analysis uses sensitive patient-level health, utilization, care coordination, and financial data. Access should follow the minimum necessary principle, with role-based controls.

The third issue is data governance. Missing follow-up values and financial anomalies need clear ownership, validation rules, refresh timing, and change logs.

The fourth issue is transparency. Clinicians need to understand why a patient is flagged as high risk. The model should show key drivers in plain language.

Finally, responsible AI means the model should support human judgment, not replace it. Care teams should keep final decision-making authority over outreach and discharge planning.

That concludes our presentation. Our recommendation is to start with a controlled pilot, validate the results, and scale only with strong governance in place.
