from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "sections"
DELIVERABLES = ROOT / "deliverables"


def pct(value: float, digits: int = 1) -> str:
    return f"{value * 100:.{digits}f}%"


def money(value: float, digits: int = 1) -> str:
    value = float(value)
    sign = "-" if value < 0 else ""
    value = abs(value)
    def compact(amount: float) -> str:
        text = f"{amount:.2f}"
        if text.endswith("00"):
            return f"{amount:.1f}"
        return text.rstrip("0").rstrip(".")

    if value >= 1_000_000:
        return f"{sign}${compact(value / 1_000_000)}M"
    if value >= 1_000:
        return f"{sign}${compact(value / 1_000)}K"
    return f"{sign}${value:,.0f}"


def integer(value: float | int) -> str:
    return f"{int(round(float(value))):,}"


def table_md(df: pd.DataFrame, columns: list[str] | None = None, formats: dict[str, str] | None = None) -> str:
    work = df.copy()
    if columns:
        work = work[columns]
    formats = formats or {}
    for col, kind in formats.items():
        if col not in work.columns:
            continue
        if kind == "pct":
            work[col] = work[col].map(lambda x: pct(float(x)) if pd.notna(x) else "n.a.")
        elif kind == "money":
            work[col] = work[col].map(lambda x: money(float(x)) if pd.notna(x) else "n.a.")
        elif kind == "int":
            work[col] = work[col].map(lambda x: integer(x) if pd.notna(x) else "n.a.")
        elif kind == "score":
            work[col] = work[col].map(lambda x: f"{float(x):.2f}" if pd.notna(x) else "n.a.")
    headers = [str(col) for col in work.columns]
    rows = [[str(value) for value in row] for row in work.to_numpy()]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


REFERENCE_DETAILS = {
    "INT-1": "Option 1 Healthcare Consulting Packet.pdf.",
    "INT-2": "Option 1 Final Presentation Requirements.pdf.",
    "INT-3": "NHN Patient Readmission Dataset.csv and data/cleaned/patient_readmission_clean.csv.",
    "INT-4": "NHN Financial Impact Dataset.csv and data/cleaned/financial_impact_clean.csv.",
    "INT-5": "NHN Care Coordination Dataset.csv and data/cleaned/care_coordination_clean.csv.",
    "INT-6": "data/processed/nhn_patient_level_analysis.csv.",
    "EXT-1": "Centers for Medicare & Medicaid Services. Hospital Readmissions Reduction Program. https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions-reduction-program",
    "EXT-2": "CMS Data. Hospital Readmissions Reduction Program. https://data.cms.gov/provider-data/topics/hospitals/hospital-readmissions-reduction-program",
    "EXT-3": "Elixhauser A, Steiner C. Readmissions to U.S. Hospitals by Diagnosis, 2010. HCUP Statistical Brief #153. AHRQ, 2013. https://hcup-us.ahrq.gov/reports/statbriefs/sb153.jsp",
    "EXT-4": "Jencks SF, Williams MV, Coleman EA. Rehospitalizations among patients in the Medicare fee-for-service program. N Engl J Med. 2009;360(14):1418-1428. doi:10.1056/NEJMsa0803563",
    "EXT-5": "Coleman EA, Parry C, Chalmers S, Min SJ. The care transitions intervention: results of a randomized controlled trial. Arch Intern Med. 2006;166(17):1822-1828. doi:10.1001/archinte.166.17.1822",
    "EXT-6": "Jack BW, Chetty VK, Anthony D, et al. A reengineered hospital discharge program to decrease rehospitalization: a randomized trial. Ann Intern Med. 2009;150(3):178-187. doi:10.7326/0003-4819-150-3-200902030-00007",
    "EXT-7": "Collins GS, Reitsma JB, Altman DG, Moons KGM. Transparent Reporting of a multivariable prediction model for Individual Prognosis or Diagnosis (TRIPOD): the TRIPOD statement. Ann Intern Med. 2015;162(1):55-63. doi:10.7326/M14-0697",
    "EXT-8": "TRIPOD Statement. TRIPOD+AI and TRIPOD 2015 resources. https://www.tripod-statement.org/",
}


def references_section(ids: list[str]) -> str:
    lines = ["## References Used", "", "Full reference governance is maintained in `REFERENCES.md` and `EVIDENCE_STANDARDS.md`.", ""]
    for ref_id in ids:
        lines.append(f"- [{ref_id}] {REFERENCE_DETAILS[ref_id]}")
    return "\n".join(lines)


def load_assets() -> dict[str, pd.DataFrame]:
    return {
        "master": pd.read_csv(ROOT / "data" / "processed" / "nhn_patient_level_analysis.csv"),
        "business_metrics": pd.read_csv(SECTIONS / "02_business_problem" / "data" / "business_problem_metrics.csv"),
        "segments": pd.read_csv(SECTIONS / "04_clinical_analysis" / "data" / "clinical_readmission_segments.csv"),
        "quality": pd.read_csv(SECTIONS / "03_data_overview" / "data" / "data_quality_summary.csv"),
        "model_metrics": pd.read_csv(SECTIONS / "05_predictive_modeling_results" / "data" / "model_metrics.csv"),
        "feature_importance": pd.read_csv(SECTIONS / "05_predictive_modeling_results" / "data" / "model_feature_importance.csv"),
        "confusion": pd.read_csv(SECTIONS / "05_predictive_modeling_results" / "data" / "model_confusion_matrix.csv"),
        "risk_deciles": pd.read_csv(SECTIONS / "05_predictive_modeling_results" / "data" / "risk_score_deciles.csv"),
        "interventions": pd.read_csv(SECTIONS / "06_care_coordination_analysis" / "data" / "intervention_effectiveness_summary.csv"),
        "intervention_count": pd.read_csv(SECTIONS / "06_care_coordination_analysis" / "data" / "intervention_count_summary.csv"),
        "follow_up_timing": pd.read_csv(SECTIONS / "06_care_coordination_analysis" / "data" / "follow_up_timing_summary.csv"),
        "financial_baseline": pd.read_csv(SECTIONS / "07_financial_impact_analysis" / "data" / "financial_baseline_summary.csv"),
        "cost_components": pd.read_csv(SECTIONS / "07_financial_impact_analysis" / "data" / "financial_cost_components.csv"),
        "roi": pd.read_csv(SECTIONS / "10_financial_impact_and_roi_analysis" / "data" / "roi_scenarios.csv"),
        "recommendations": pd.read_csv(SECTIONS / "09_strategic_recommendations" / "data" / "recommendation_evidence_matrix.csv"),
        "roadmap": pd.read_csv(SECTIONS / "11_implementation_roadmap" / "data" / "implementation_roadmap.csv"),
        "success_metrics": pd.read_csv(SECTIONS / "11_implementation_roadmap" / "data" / "success_metrics.csv"),
    }


def top_segment(segments: pd.DataFrame, segment_type: str) -> pd.Series:
    return segments[segments["segment_type"].eq(segment_type)].sort_values("readmission_rate", ascending=False).iloc[0]


def generate_section_briefs(data: dict[str, pd.DataFrame]) -> None:
    segments = data["segments"]
    model = data["model_metrics"].query("model == 'Expanded clinical logistic model'").iloc[0]
    roi_expected = data["roi"].query("scenario == 'Expected'").iloc[0]
    briefs = {
        "01_executive_summary": {
            "title": "Executive Summary",
            "message": f"NHN has a {pct(data['master']['readmitted_within_30_days'].mean())} readmission rate in the analytical sample, and the expected ROI scenario estimates {money(roi_expected['net_savings'])} in net savings before cost validation.",
            "visuals": ["images/executive_kpi_cards.svg"],
            "data": ["data/executive_kpis.csv"],
        },
        "02_business_problem": {
            "title": "Business Problem",
            "message": "Historical readmissions rose from 14.2% in 2022 to 18.4% in 2025, while the current sample shows elevated risk among emergency admissions and patients without documented follow-up status.",
            "visuals": ["images/historical_readmission_trend.svg", "images/readmission_by_admission_type.svg", "images/readmission_by_follow_up_status.svg"],
            "data": ["data/business_problem_metrics.csv", "data/readmission_by_business_driver.csv"],
        },
        "03_data_overview": {
            "title": "Data Overview",
            "message": "All three source datasets join cleanly on patient_id, with 12,000 matched patients. Missing follow-up documentation and financial field quality flags remain important limitations.",
            "visuals": ["images/data_flow.svg", "images/missing_values_summary.svg"],
            "data": ["data/source_dataset_profile.csv", "data/data_quality_summary.csv"],
        },
        "04_clinical_analysis": {
            "title": "Clinical Analysis",
            "message": f"Observed readmission risk rises with age, chronic condition burden, and prior admissions. The highest chronic condition bucket has a {pct(top_segment(segments, 'Chronic condition bucket')['readmission_rate'])} readmission rate.",
            "visuals": ["images/readmission_by_age_group.svg", "images/readmission_by_chronic_condition_bucket.svg", "images/readmission_by_prior_admissions.svg"],
            "data": ["data/clinical_readmission_segments.csv"],
        },
        "05_predictive_modeling_results": {
            "title": "Predictive Modeling Results",
            "message": f"The expanded clinical logistic model performs better than the baseline model, with ROC-AUC {model['roc_auc']:.2f}, accuracy {pct(model['accuracy'])}, and recall {pct(model['recall'])}.",
            "visuals": ["images/model_metrics_comparison.svg", "images/feature_importance.svg", "images/risk_decile_readmission_rate.svg"],
            "data": ["data/model_metrics.csv", "data/model_feature_importance.csv", "data/risk_score_deciles.csv"],
        },
        "06_care_coordination_analysis": {
            "title": "Care Coordination Analysis",
            "message": "Care coordination activity should be interpreted as observed association, not causal impact. The next decision is whether support reaches the highest-risk patients early enough.",
            "visuals": ["images/readmission_by_intervention.svg", "images/readmission_by_intervention_count.svg", "images/readmission_by_follow_up_timing.svg"],
            "data": ["data/intervention_effectiveness_summary.csv", "data/intervention_count_summary.csv"],
        },
        "07_financial_impact_analysis": {
            "title": "Financial Impact Analysis",
            "message": f"The cleaned financial dataset shows {money(data['master']['total_care_cost_nonnegative'].sum())} in total care cost and {money(data['master']['penalty_cost_nonnegative'].sum())} in nonnegative CMS penalty exposure.",
            "visuals": ["images/financial_cost_components.svg", "images/total_cost_by_readmission_outcome.svg"],
            "data": ["data/financial_baseline_summary.csv", "data/financial_cost_components.csv"],
        },
        "08_executive_dashboard_walkthrough": {
            "title": "Executive Dashboard Walkthrough",
            "message": "The dashboard should give leaders one integrated view of readmission risk, clinical drivers, cost exposure, care coordination performance, and recommendation status.",
            "visuals": ["images/dashboard_wireframe.svg"],
            "data": ["data/dashboard_ready_extract.csv", "data/dashboard_kpis.csv", "data/dashboard_measure_definitions.csv"],
        },
        "09_strategic_recommendations": {
            "title": "Strategic Recommendations",
            "message": "The highest-priority actions are risk scoring, enhanced discharge review, follow-up documentation improvement, targeted care coordination, and executive dashboard reporting.",
            "visuals": ["images/recommendation_priority_matrix.svg"],
            "data": ["data/recommendation_evidence_matrix.csv"],
        },
        "10_financial_impact_and_roi_analysis": {
            "title": "Financial Impact And ROI Analysis",
            "message": f"The expected scenario assumes a 10.0% readmission reduction, {integer(roi_expected['avoided_readmissions'])} avoided readmissions, and {money(roi_expected['net_savings'])} in estimated net savings.",
            "visuals": ["images/net_savings_scenarios.svg", "images/roi_scenarios.svg"],
            "data": ["data/roi_scenarios.csv"],
        },
        "11_implementation_roadmap": {
            "title": "Implementation Roadmap",
            "message": "The roadmap starts with KPI governance, risk scoring pilots, and follow-up documentation, then expands care coordination and dashboard reporting over 12 months.",
            "visuals": ["images/implementation_timeline.svg", "images/risk_matrix.svg"],
            "data": ["data/implementation_roadmap.csv", "data/success_metrics.csv"],
        },
    }
    for folder, brief in briefs.items():
        content = f"""# {brief['title']} Section Brief

## Slide Purpose

Prepare the content, visuals, and talking points needed for the `{folder}` portion of the Board presentation.

## Key Message

{brief['message']}

## Recommended Visuals

{chr(10).join(f"- `{item}`" for item in brief['visuals'])}

## Supporting Data

{chr(10).join(f"- `{item}`" for item in brief['data'])}

## Presenter Notes

- Keep the message executive-level.
- Use the linked visuals as slide-ready evidence.
- Avoid overclaiming causality where the analysis only shows observed association.
- Preserve the data limitations from `DATA_CLEANING_SUMMARY.md`.
"""
        write(SECTIONS / folder / "notes" / "section_brief.md", content)


def generate_project_charter(data: dict[str, pd.DataFrame]) -> None:
    master = data["master"]
    content = f"""# Project Charter

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

- Matched patient records: {integer(len(master))}
- Analytical sample readmission rate: {pct(master['readmitted_within_30_days'].mean())}
- Total care cost in cleaned financial data: {money(master['total_care_cost_nonnegative'].sum())}
- Nonnegative CMS penalty exposure: {money(master['penalty_cost_nonnegative'].sum())}

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

{references_section(['INT-1', 'INT-2', 'INT-6', 'EXT-1', 'EXT-2', 'EXT-3', 'EXT-4'])}
"""
    write(DELIVERABLES / "01_project_charter" / "final" / "project_charter.md", content)


def generate_eda_report(data: dict[str, pd.DataFrame]) -> None:
    master = data["master"]
    quality = data["quality"].head(8)
    segments = data["segments"]
    top_by_type = (
        segments.sort_values("readmission_rate", ascending=False)
        .groupby("segment_type", as_index=False)
        .first()
        .sort_values("readmission_rate", ascending=False)
    )
    content = f"""# Exploratory Data Analysis Report

## Executive Summary

The cleaned integrated dataset contains {integer(len(master))} matched patient records across the patient readmission, financial impact, and care coordination datasets. The analytical sample readmission rate is {pct(master['readmitted_within_30_days'].mean())}. The strongest descriptive readmission patterns appear in chronic condition burden, prior admissions, age, emergency admission type, skilled nursing discharge, and missing follow-up status.

## Data Sources

| Dataset | Role |
| --- | --- |
| Patient Readmission Dataset | Clinical and utilization variables plus readmission outcome |
| Financial Impact Dataset | Readmission cost, reimbursement, penalty, and total care cost fields |
| Care Coordination Dataset | Post-discharge support and intervention fields |

All three datasets contain {integer(len(master))} unique `patient_id` values and join completely.

## Data Quality Assessment

{table_md(quality, ['dataset', 'issue', 'affected_rows', 'affected_rate'], {'affected_rows': 'int', 'affected_rate': 'pct'})}

The largest quality issue is missing follow-up status. Financial fields also include missing and negative values. The cleaning workflow preserves original values, adds quality flags, and creates analysis-ready companion fields.

## Overall Readmission Pattern

- Patients analyzed: {integer(len(master))}
- Readmitted within 30 days: {integer(master['readmitted_within_30_days'].sum())}
- Readmission rate: {pct(master['readmitted_within_30_days'].mean())}

## Segment Findings

{table_md(top_by_type, ['segment_type', 'segment', 'patient_count', 'readmission_rate', 'avg_total_care_cost'], {'patient_count': 'int', 'readmission_rate': 'pct', 'avg_total_care_cost': 'money'})}

## Recommended Visuals

- `sections/02_business_problem/images/historical_readmission_trend.svg`
- `sections/03_data_overview/images/missing_values_summary.svg`
- `sections/04_clinical_analysis/images/readmission_by_age_group.svg`
- `sections/04_clinical_analysis/images/readmission_by_chronic_condition_bucket.svg`
- `sections/04_clinical_analysis/images/readmission_by_prior_admissions.svg`
- `sections/04_clinical_analysis/images/readmission_by_discharge_disposition.svg`

## Key Findings

1. Readmission risk increases materially with chronic condition burden.
2. Prior admissions show a clear relationship with readmission risk.
3. Older age groups carry higher observed readmission rates.
4. Emergency admissions have higher readmission rates than urgent or elective admissions.
5. Unknown follow-up status has the highest observed readmission rate among follow-up categories.
6. Financial data can support ROI planning, but final estimates should use quality flags and sensitivity checks.

## Areas For Further Investigation

- Validate whether missing follow-up status reflects actual lack of follow-up or documentation gaps.
- Compare interventions within high-risk deciles to determine whether care coordination reaches the right patients.
- Validate ROI assumptions with actual implementation costs.
- Review model threshold selection with clinical operations and care coordination capacity.

## Evidence Notes

- Record counts, readmission rates, data-quality rates, and segment tables are calculated from the cleaned and integrated NHN data [INT-3], [INT-4], [INT-5], [INT-6].
- The 30-day all-cause framing aligns with AHRQ HCUP readmission definitions and national readmission context [EXT-3].
- Segment relationships are descriptive. They should guide prioritization, not causal claims [EXT-4].

{references_section(['INT-3', 'INT-4', 'INT-5', 'INT-6', 'EXT-3', 'EXT-4'])}
"""
    write(DELIVERABLES / "02_eda_report" / "final" / "eda_report.md", content)


def generate_model_report(data: dict[str, pd.DataFrame]) -> None:
    metrics = data["model_metrics"]
    importance = data["feature_importance"].head(12)
    confusion = data["confusion"]
    risk = data["risk_deciles"]
    best = metrics.query("model == 'Expanded clinical logistic model'").iloc[0]
    content = f"""# Model Evaluation Report

## Modeling Objective

Identify patients at higher risk of 30-day readmission before discharge so NHN can prioritize discharge planning, care coordination, and follow-up resources.

## Target Variable

`readmitted_within_30_days`

- 1 = patient was readmitted within 30 days.
- 0 = patient was not readmitted within 30 days.

## Feature Set

The preliminary models use clinical and operational fields that are available before or around discharge. Financial outcomes were excluded from prediction because they represent downstream impact rather than pre-discharge risk.

## Models Compared

{table_md(metrics, ['model', 'accuracy', 'precision', 'recall', 'f1_score', 'roc_auc', 'predicted_positive_rate', 'test_records'], {'accuracy': 'pct', 'precision': 'pct', 'recall': 'pct', 'f1_score': 'pct', 'roc_auc': 'score', 'predicted_positive_rate': 'pct', 'test_records': 'int'})}

## Selected Model

The expanded clinical logistic model is the current preferred planning model because it outperforms the numeric baseline and remains explainable for clinical leadership.

- Accuracy: {pct(best['accuracy'])}
- Precision: {pct(best['precision'])}
- Recall: {pct(best['recall'])}
- F1 score: {pct(best['f1_score'])}
- ROC-AUC: {best['roc_auc']:.2f}

## Confusion Matrix

{table_md(confusion, ['actual', 'predicted', 'count'], {'count': 'int'})}

## Feature Importance

{table_md(importance, ['feature', 'coefficient', 'absolute_coefficient'], {'coefficient': 'score', 'absolute_coefficient': 'score'})}

## Risk Decile Validation

{table_md(risk, ['risk_decile', 'patient_count', 'average_risk_score', 'readmission_rate'], {'patient_count': 'int', 'average_risk_score': 'score', 'readmission_rate': 'pct'})}

The decile table shows that the model separates lower-risk and higher-risk patients well enough for planning and prioritization.

## Limitations

- This is a preliminary model built from the supplied project dataset.
- The model requires validation before clinical production use.
- The 0.50 threshold may not be the best operational threshold. NHN should choose a threshold based on clinical capacity, acceptable false positives, and the cost of missing high-risk patients.
- The current model does not include facility-level, time-based, medication, lab, or social determinant variables that could improve performance.

## Operational Recommendation

Use the model initially for risk stratification, discharge planning prioritization, and dashboard reporting. NHN should pilot the score with care coordination teams before using it for automated decisions.

## Evidence Notes

- Model metrics, confusion matrix counts, feature coefficients, and risk decile validation are generated from the supplied project dataset and section modeling outputs [INT-6].
- Model results are planning evidence. TRIPOD guidance supports transparent reporting, validation caveats, and careful interpretation before production use [EXT-7], [EXT-8].
- The selected workflow should combine model score, clinical rules, and care team review instead of using one score as the sole decision engine [EXT-7].

{references_section(['INT-6', 'EXT-7', 'EXT-8'])}
"""
    write(DELIVERABLES / "03_model_evaluation_report" / "final" / "model_evaluation_report.md", content)


def generate_clinical_care_report(data: dict[str, pd.DataFrame]) -> None:
    segments = data["segments"]
    interventions = data["interventions"]
    intervention_count = data["intervention_count"]
    timing = data["follow_up_timing"]
    selected_segments = segments[segments["segment_type"].isin(["Age group", "Chronic condition bucket", "Prior admissions bucket", "Discharge disposition", "Admission type", "Follow-up status"])]
    content = f"""# Clinical And Care Coordination Analysis Report

## Executive Summary

The clinical analysis identifies higher readmission risk among older patients, patients with more chronic conditions, patients with repeated prior admissions, emergency admissions, skilled nursing discharges, and patients with unknown follow-up status. Care coordination activity requires cautious interpretation because high-risk patients may receive more support.

## High-Risk Clinical Segments

{table_md(selected_segments.sort_values('readmission_rate', ascending=False).head(15), ['segment_type', 'segment', 'patient_count', 'readmission_rate', 'avg_total_care_cost'], {'patient_count': 'int', 'readmission_rate': 'pct', 'avg_total_care_cost': 'money'})}

## Care Coordination Intervention Summary

{table_md(interventions, ['intervention', 'patients_with_intervention', 'readmission_rate_with_intervention', 'readmission_rate_without_intervention', 'observed_difference_pp'], {'patients_with_intervention': 'int', 'readmission_rate_with_intervention': 'pct', 'readmission_rate_without_intervention': 'pct', 'observed_difference_pp': 'pct'})}

## Intervention Count Summary

{table_md(intervention_count, ['intervention_count', 'patient_count', 'readmission_rate'], {'patient_count': 'int', 'readmission_rate': 'pct'})}

## Follow-Up Timing Summary

{table_md(timing, ['follow_up_timing_bucket', 'patient_count', 'readmission_rate'], {'patient_count': 'int', 'readmission_rate': 'pct'})}

## Interpretation

The most useful care coordination insight is not that one intervention clearly causes lower readmissions. The dataset suggests that NHN should evaluate whether interventions are assigned consistently to the patients with the greatest predicted risk. Several raw intervention groups have similar or higher readmission rates, which likely reflects patient selection and baseline risk.

## Recommendations

1. Prioritize enhanced discharge planning for patients with high chronic condition burden or repeated prior admissions.
2. Use the risk score to trigger care coordination review before discharge.
3. Treat unknown follow-up status as an operational defect and close documentation gaps.
4. Evaluate intervention effectiveness inside risk bands, especially the top three risk deciles.
5. Track follow-up completion, medication review, home health referral, transportation assistance, and post-discharge calls in the executive dashboard.

## Required Caveat

The current care coordination analysis shows observed association. It does not prove that an intervention caused or prevented readmission.

## Evidence Notes

- Clinical segment rates, intervention comparisons, intervention counts, and follow-up timing rates are calculated from the integrated NHN patient-level analysis and care coordination data [INT-3], [INT-5], [INT-6].
- Care transition and discharge redesign recommendations are supported by randomized evidence for structured transition support and reengineered discharge workflows [EXT-5], [EXT-6].
- The current intervention comparisons remain observational. Selection bias is a material limitation, so the report recommends redesigning targeting and timing rather than claiming causal effects.

{references_section(['INT-3', 'INT-5', 'INT-6', 'EXT-5', 'EXT-6', 'EXT-7'])}
"""
    write(DELIVERABLES / "04_clinical_care_coordination_report" / "final" / "clinical_care_coordination_report.md", content)


def generate_financial_report(data: dict[str, pd.DataFrame]) -> None:
    baseline = data["financial_baseline"]
    components = data["cost_components"]
    roi = data["roi"]
    expected = roi.query("scenario == 'Expected'").iloc[0]
    content = f"""# Financial Impact And ROI Analysis Report

## Executive Summary

NHN's financial opportunity comes from reducing avoidable readmission costs and CMS penalty exposure. The expected scenario estimates {integer(expected['avoided_readmissions'])} avoided readmissions, {money(expected['gross_savings'])} in gross savings, {money(expected['net_savings'])} in net savings, and ROI of {expected['roi']:.2f}x before final implementation cost validation.

## Financial Baseline By Readmission Outcome

{table_md(baseline, ['readmission_label', 'patient_count', 'avg_total_care_cost', 'avg_readmission_cost', 'avg_penalty_cost', 'avg_net_reimbursement_gap', 'total_care_cost', 'total_penalty_cost'], {'patient_count': 'int', 'avg_total_care_cost': 'money', 'avg_readmission_cost': 'money', 'avg_penalty_cost': 'money', 'avg_net_reimbursement_gap': 'money', 'total_care_cost': 'money', 'total_penalty_cost': 'money'})}

## Cost Components

{table_md(components, ['component', 'amount'], {'amount': 'money'})}

## ROI Scenarios

{table_md(roi, ['scenario', 'readmission_reduction_rate', 'implementation_cost_assumption', 'avoided_readmissions', 'gross_savings', 'net_savings', 'roi'], {'readmission_reduction_rate': 'pct', 'implementation_cost_assumption': 'money', 'avoided_readmissions': 'int', 'gross_savings': 'money', 'net_savings': 'money', 'roi': 'score'})}

## Scenario Assumptions

- Conservative: 5.0% readmission reduction and $1.0M implementation cost.
- Expected: 10.0% readmission reduction and $1.75M implementation cost.
- Optimistic: 15.0% readmission reduction and $2.5M implementation cost.
- Average avoided value per readmission uses readmission cost plus nonnegative penalty cost among readmitted patients.

## Interpretation

The expected scenario suggests that reducing avoidable readmissions can create meaningful financial value. The Board should treat these figures as planning estimates until implementation costs, intervention capacity, and avoidable-readmission assumptions are validated.

## Limitations

- Financial fields include missing and negative values, so the analysis uses nonnegative companion fields.
- Scenario implementation costs are placeholders.
- The model does not yet distinguish avoidable from unavoidable readmissions.
- ROI should be refreshed after dashboard implementation and operational pilot results.

## Evidence Notes

- Financial baseline, cost components, and ROI scenario values are calculated from the cleaned financial data and integrated patient-level analysis table [INT-4], [INT-6].
- CMS HRRP references provide policy context for why penalty exposure matters. They do not validate NHN-specific savings estimates [EXT-1], [EXT-2].
- Readmission-cost framing is supported by peer-reviewed Medicare readmission literature, while ROI remains a project scenario estimate [EXT-4].

{references_section(['INT-4', 'INT-6', 'EXT-1', 'EXT-2', 'EXT-4'])}
"""
    write(DELIVERABLES / "05_financial_impact_roi_report" / "final" / "financial_impact_roi_report.md", content)


def generate_dashboard_spec(data: dict[str, pd.DataFrame]) -> None:
    content = f"""# Executive Dashboard Specification

## Dashboard Tool

Use Tableau first for the required executive dashboard. This repository includes the dashboard-ready data, KPI definitions, and page specifications needed to build the native Tableau dashboard file.

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

## Evidence Notes

- Dashboard data files are derived from the integrated patient-level analysis table and section-level summaries [INT-6].
- The dashboard is required by the final presentation guide and should be built in Tableau first based on team preference [INT-2].
- Model and care coordination views should preserve validation and association caveats [EXT-5], [EXT-6], [EXT-7].

{references_section(['INT-2', 'INT-6', 'EXT-1', 'EXT-3', 'EXT-5', 'EXT-6', 'EXT-7'])}
"""
    write(DELIVERABLES / "06_executive_dashboard" / "final" / "executive_dashboard_spec.md", content)


def generate_board_presentation_content(data: dict[str, pd.DataFrame]) -> None:
    master = data["master"]
    model = data["model_metrics"].query("model == 'Expanded clinical logistic model'").iloc[0]
    expected = data["roi"].query("scenario == 'Expected'").iloc[0]
    recommendations = data["recommendations"]
    roadmap = data["roadmap"]
    content = f"""# Executive Board Presentation Content

## Slide 1: Title

National Hospital Network Readmission Reduction Strategy

Subtitle: Clinical analytics, financial impact, care coordination, and 12-month implementation plan

## Slide 2: Executive Summary

- NHN's analytical sample readmission rate is {pct(master['readmitted_within_30_days'].mean())}.
- The highest-risk groups include older patients, patients with more chronic conditions, patients with repeated prior admissions, emergency admissions, and skilled nursing discharges.
- The expanded clinical model reached ROC-AUC {model['roc_auc']:.2f}.
- The expected financial scenario estimates {money(expected['net_savings'])} in net savings before implementation cost validation.

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

- Total care cost in the cleaned dataset is {money(master['total_care_cost_nonnegative'].sum())}.
- Nonnegative CMS penalty exposure is {money(master['penalty_cost_nonnegative'].sum())}.
- Financial estimates should use quality flags and scenario sensitivity.

## Slide 10: Dashboard Walkthrough

- Executive KPI Summary.
- Clinical Analytics.
- Financial Analytics.
- Care Coordination Analytics.
- Executive Recommendation Center.

## Slide 11: Strategic Recommendations

{chr(10).join(f"- {row.recommendation}: {row.evidence}" for row in recommendations.itertuples())}

## Slide 12: Financial Impact And ROI

| Scenario | Readmission Reduction | Avoided Readmissions | Net Savings | ROI |
| --- | --- | --- | --- | --- |
{chr(10).join(f"| {row.scenario} | {pct(row.readmission_reduction_rate)} | {integer(row.avoided_readmissions)} | {money(row.net_savings)} | {row.roi:.2f}x |" for row in data['roi'].itertuples())}

## Slide 13: Implementation Roadmap

{chr(10).join(f"- {row.phase}: {row.initiative}" for row in roadmap.itertuples())}

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

{references_section(['INT-1', 'INT-2', 'INT-3', 'INT-4', 'INT-5', 'INT-6', 'EXT-1', 'EXT-2', 'EXT-3', 'EXT-4', 'EXT-5', 'EXT-6', 'EXT-7', 'EXT-8'])}
"""
    write(DELIVERABLES / "07_executive_board_presentation" / "final" / "executive_board_presentation_content.md", content)


def update_tracker() -> None:
    content = """# Deliverables Tracker

| Deliverable | Folder | Primary Output | Current Status |
| --- | --- | --- | --- |
| 1. Project Charter | `01_project_charter` | Charter document | Final Markdown created |
| 2. EDA Report | `02_eda_report` | EDA report with at least five visuals | Final Markdown created |
| 3. Model Evaluation Report | `03_model_evaluation_report` | Model comparison and interpretation report | Final Markdown created |
| 4. Clinical And Care Coordination Report | `04_clinical_care_coordination_report` | Clinical and intervention analysis report | Final Markdown created |
| 5. Financial Impact And ROI Report | `05_financial_impact_roi_report` | Financial baseline and ROI scenario report | Final Markdown created |
| 6. Executive Dashboard | `06_executive_dashboard` | Tableau dashboard | Tableau-first build package and validation workbook created; native Tableau workbook still needed |
| 7. Executive Board Presentation | `07_executive_board_presentation` | Final executive presentation | Final PPTX and preview images created |

## Recommended Workflow

1. Review each final Markdown file for instructor or team preferences.
2. Build the native Tableau dashboard from the dashboard-ready data.
3. Convert the Board presentation content into the final deck.
4. Put submission-ready files in each `final/` folder.
"""
    write(DELIVERABLES / "deliverables_tracker.md", content)


def main() -> None:
    data = load_assets()
    generate_section_briefs(data)
    generate_project_charter(data)
    generate_eda_report(data)
    generate_model_report(data)
    generate_clinical_care_report(data)
    generate_financial_report(data)
    generate_dashboard_spec(data)
    generate_board_presentation_content(data)
    update_tracker()
    print("Generated final deliverable markdown files and section briefs.")


if __name__ == "__main__":
    main()
