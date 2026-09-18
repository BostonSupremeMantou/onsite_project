from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"
SECTIONS = ROOT / "sections"


def read_csv(rel_path: str) -> list[dict[str, str]]:
    with (ROOT / rel_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_asset(source_rel: str, destination: Path) -> str:
    source = ROOT / source_rel
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() == destination.resolve():
        return destination.name
    shutil.copy2(source, destination)
    return destination.name


def money(value: float) -> str:
    value = float(value)
    def compact(amount: float) -> str:
        text = f"{amount:.2f}"
        if text.endswith("00"):
            return f"{amount:.1f}"
        return text.rstrip("0").rstrip(".")

    if abs(value) >= 1_000_000:
        return f"${compact(value / 1_000_000)}M"
    if abs(value) >= 1_000:
        return f"${compact(value / 1_000)}K"
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{float(value) * 100:.1f}%"


def table_md(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def manifest_markdown(title: str, rows: list[dict[str, object]]) -> str:
    return f"""# {title}

This file lists the supporting assets placed in this deliverable folder and where they came from.

{table_md(rows)}
"""


def copy_data(deliverable: Path, items: list[tuple[str, str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_rel, purpose, destination_name in items:
        copied_name = copy_asset(source_rel, deliverable / "data" / destination_name)
        rows.append({
            "Destination": f"data/{copied_name}",
            "Purpose": purpose,
            "Source": source_rel,
        })
    write_text(deliverable / "data" / "data_manifest.md", manifest_markdown("Data Manifest", rows))
    return rows


def copy_images(deliverable: Path, items: list[tuple[str, str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_rel, use, destination_name in items:
        copied_name = copy_asset(source_rel, deliverable / "images" / destination_name)
        rows.append({
            "Image": f"images/{copied_name}",
            "Recommended Use": use,
            "Source": source_rel,
        })
    write_text(deliverable / "images" / "figure_index.md", manifest_markdown("Figure Index", rows))
    return rows


def write_review_notes(deliverable: Path, title: str, bullets: list[str], caveats: list[str]) -> None:
    write_text(deliverable / "notes" / "review_notes.md", f"""# {title} Review Notes

## How To Use This Folder

{chr(10).join(f"- {item}" for item in bullets)}

## Caveats To Preserve

{chr(10).join(f"- {item}" for item in caveats)}
""")


def write_draft_outline(deliverable: Path, title: str, sections: list[str]) -> None:
    write_text(deliverable / "drafts" / "submission_outline.md", f"""# {title} Submission Outline

Use this outline when converting the deliverable into a final submitted document, dashboard page, or presentation section.

{chr(10).join(f"## {item}{chr(10)}" for item in sections)}
""")


def populate_project_charter() -> None:
    deliverable = DELIVERABLES / "01_project_charter"
    copy_data(deliverable, [
        ("sections/01_executive_summary/data/executive_kpis.csv", "Executive baseline metrics.", "executive_kpis.csv"),
        ("sections/02_business_problem/data/business_problem_metrics.csv", "Historical readmission and business context.", "business_problem_metrics.csv"),
        ("sections/03_data_overview/data/source_dataset_profile.csv", "Source dataset inventory.", "source_dataset_profile.csv"),
        ("sections/03_data_overview/data/data_quality_summary.csv", "Known data quality issues for project risk planning.", "data_quality_summary.csv"),
    ])
    copy_images(deliverable, [
        ("sections/01_executive_summary/images/executive_kpi_cards.svg", "Opening KPI summary.", "executive_kpi_cards.svg"),
        ("sections/02_business_problem/images/historical_readmission_trend.svg", "Business problem evidence.", "historical_readmission_trend.svg"),
        ("sections/03_data_overview/images/data_flow.svg", "Data integration overview.", "data_flow.svg"),
    ])
    write_csv(deliverable / "analysis" / "project_scope_matrix.csv", [
        {"Workstream": "Clinical analysis", "In Scope": "Readmission patterns by patient segment", "Out Of Scope": "Clinical protocol design"},
        {"Workstream": "Predictive modeling", "In Scope": "Pre-discharge risk scoring and staged workflow", "Out Of Scope": "Production clinical decision support deployment"},
        {"Workstream": "Care coordination", "In Scope": "Observed intervention patterns and redesign opportunities", "Out Of Scope": "Causal intervention trial"},
        {"Workstream": "Financial impact", "In Scope": "Cost exposure and ROI scenarios", "Out Of Scope": "Final budget approval"},
        {"Workstream": "Dashboard", "In Scope": "Tableau-first build package and validation targets", "Out Of Scope": "Native Tableau Desktop build in this repository"},
    ])
    write_csv(deliverable / "analysis" / "stakeholder_matrix.csv", [
        {"Stakeholder": "Board of Directors", "Interest": "Clinical outcomes, financial value, organizational risk", "Deliverable Need": "Executive presentation and decision framing"},
        {"Stakeholder": "Chief Medical Officer", "Interest": "Quality, patient safety, clinical governance", "Deliverable Need": "Risk workflow and clinical caveats"},
        {"Stakeholder": "Care Coordination Leadership", "Interest": "Targeting, timing, completion, workload", "Deliverable Need": "Care coordination redesign evidence"},
        {"Stakeholder": "Finance Leadership", "Interest": "Cost exposure, penalties, ROI", "Deliverable Need": "Financial impact report and scenario assumptions"},
        {"Stakeholder": "Analytics and BI Team", "Interest": "Data model, dashboard, reproducibility", "Deliverable Need": "Clean extract, measures, validation checks"},
    ])
    write_text(deliverable / "analysis" / "charter_evidence_summary.md", """# Charter Evidence Summary

## Core Evidence

- Historical readmissions increased from 14.2% in 2022 to 18.4% in 2025.
- The integrated analytical sample contains 12,000 matched patient records.
- The analytical sample readmission rate is 43.2%.
- Total care cost in the cleaned data is $303.1M.
- Nonnegative CMS penalty exposure is $21.2M.

## Steering Decisions Reflected

- Treat readmission as a multi-lens problem rather than a single clinical or financial emphasis.
- Use broad high-risk coverage for risk deciles 8-10 and clinically elevated segments.
- Use Tableau as the primary dashboard implementation path.
""")
    write_review_notes(deliverable, "Project Charter", [
        "Use `final/project_charter.md` as the submission-ready charter.",
        "Use `analysis/project_scope_matrix.csv` to defend scope choices.",
        "Use `analysis/stakeholder_matrix.csv` to explain who needs each output.",
    ], [
        "Dashboard package is complete, but a native Tableau workbook still needs Tableau Desktop.",
        "ROI estimates are planning scenarios and require finance validation before budget commitment.",
    ])
    write_draft_outline(deliverable, "Project Charter", [
        "Business Problem Statement",
        "Engagement Objectives",
        "Stakeholders",
        "Scope And Out-Of-Scope Items",
        "Initial Hypotheses",
        "Success Metrics",
        "Risks And Mitigations",
        "Team Roles",
    ])


def populate_eda_report() -> None:
    deliverable = DELIVERABLES / "02_eda_report"
    copy_data(deliverable, [
        ("sections/03_data_overview/data/source_dataset_profile.csv", "Dataset inventory and join integrity.", "source_dataset_profile.csv"),
        ("sections/03_data_overview/data/data_quality_summary.csv", "Missing values and quality flags.", "data_quality_summary.csv"),
        ("sections/02_business_problem/data/readmission_by_business_driver.csv", "Readmission by key business drivers.", "readmission_by_business_driver.csv"),
        ("sections/04_clinical_analysis/data/clinical_readmission_segments.csv", "Clinical segment rates.", "clinical_readmission_segments.csv"),
        ("sections/06_care_coordination_analysis/data/intervention_effectiveness_summary.csv", "Observed intervention comparisons.", "intervention_effectiveness_summary.csv"),
        ("sections/07_financial_impact_analysis/data/financial_baseline_summary.csv", "Financial baseline by readmission outcome.", "financial_baseline_summary.csv"),
    ])
    copy_images(deliverable, [
        ("sections/03_data_overview/images/missing_values_summary.svg", "Data quality visual.", "missing_values_summary.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_age_group.svg", "Clinical segment visual.", "readmission_by_age_group.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_chronic_condition_bucket.svg", "Clinical segment visual.", "readmission_by_chronic_condition_bucket.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_prior_admissions.svg", "Clinical segment visual.", "readmission_by_prior_admissions.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_discharge_disposition.svg", "Clinical segment visual.", "readmission_by_discharge_disposition.svg"),
        ("sections/02_business_problem/images/readmission_by_follow_up_status.svg", "Follow-up documentation visual.", "readmission_by_follow_up_status.svg"),
    ])
    segments = read_csv("sections/04_clinical_analysis/data/clinical_readmission_segments.csv")
    top = sorted(segments, key=lambda row: float(row["readmission_rate"]), reverse=True)[:10]
    write_csv(deliverable / "analysis" / "top_readmission_segments.csv", [
        {
            "Segment Type": row["segment_type"],
            "Segment": row["segment"],
            "Patients": int(row["patient_count"]),
            "Readmission Rate": pct(row["readmission_rate"]),
            "Average Total Care Cost": money(row["avg_total_care_cost"]),
        }
        for row in top
    ])
    write_csv(deliverable / "analysis" / "eda_findings_matrix.csv", [
        {"Finding": "Unknown follow-up status carries elevated readmission risk.", "Evidence": "2,587 records lack follow-up status and the segment readmission rate is high.", "Use": "Main caveat and care coordination question"},
        {"Finding": "Chronic condition burden has a strong relationship with readmission.", "Evidence": "5+ chronic condition bucket is the highest clinical segment.", "Use": "Clinical Analytics page"},
        {"Finding": "Prior admissions identify high-risk patients.", "Evidence": "3+ prior admissions segment has materially elevated readmission rate.", "Use": "Risk workflow and clinical rules"},
        {"Finding": "Emergency admissions and skilled nursing discharges need focused review.", "Evidence": "Both segments show elevated observed readmission rates.", "Use": "Discharge review recommendation"},
        {"Finding": "Financial fields support ROI planning but need quality flags.", "Evidence": "Missing and negative financial values exist in source data.", "Use": "Financial caveat"},
    ])
    write_review_notes(deliverable, "EDA Report", [
        "Use `final/eda_report.md` for the written EDA deliverable.",
        "Use `analysis/top_readmission_segments.csv` to select chart callouts.",
        "Use `images/figure_index.md` to pick slide-ready visuals.",
    ], [
        "Do not interpret observed segment relationships as causal.",
        "Keep missing follow-up status and financial data quality in the main report.",
    ])
    write_draft_outline(deliverable, "EDA Report", [
        "Data Sources And Join Integrity",
        "Data Quality Assessment",
        "Overall Readmission Pattern",
        "Clinical Segment Findings",
        "Care Coordination Findings",
        "Financial EDA Findings",
        "Visual Appendix",
        "Next Questions",
    ])


def populate_model_report() -> None:
    deliverable = DELIVERABLES / "03_model_evaluation_report"
    copy_data(deliverable, [
        ("sections/05_predictive_modeling_results/data/model_metrics.csv", "Model performance comparison.", "model_metrics.csv"),
        ("sections/05_predictive_modeling_results/data/model_confusion_matrix.csv", "Expanded model confusion matrix.", "model_confusion_matrix.csv"),
        ("sections/05_predictive_modeling_results/data/model_feature_importance.csv", "Expanded model coefficient ranking.", "model_feature_importance.csv"),
        ("sections/05_predictive_modeling_results/data/risk_score_deciles.csv", "Risk decile calibration table.", "risk_score_deciles.csv"),
    ])
    copy_images(deliverable, [
        ("sections/05_predictive_modeling_results/images/model_metrics_comparison.svg", "Model comparison visual.", "model_metrics_comparison.svg"),
        ("sections/05_predictive_modeling_results/images/confusion_matrix_expanded_clinical.svg", "Confusion matrix visual.", "confusion_matrix_expanded_clinical.svg"),
        ("sections/05_predictive_modeling_results/images/feature_importance.svg", "Top driver visual.", "feature_importance.svg"),
        ("sections/05_predictive_modeling_results/images/risk_decile_readmission_rate.svg", "Risk stratification visual.", "risk_decile_readmission_rate.svg"),
    ])
    metrics = read_csv("sections/05_predictive_modeling_results/data/model_metrics.csv")
    write_csv(deliverable / "analysis" / "model_comparison_summary.csv", [
        {
            "Model": row["model"],
            "Accuracy": pct(row["accuracy"]),
            "Precision": pct(row["precision"]),
            "Recall": pct(row["recall"]),
            "F1 Score": pct(row["f1_score"]),
            "ROC AUC": f"{float(row['roc_auc']):.2f}",
            "Recommended Use": "Benchmark" if "Baseline" in row["model"] else "Primary explainable risk input",
        }
        for row in metrics
    ])
    write_csv(deliverable / "analysis" / "staged_model_workflow.csv", [
        {"Stage": "1. Broad risk screen", "Input": "Risk deciles 8-10 and clinical rules", "Purpose": "Maximize high-risk coverage"},
        {"Stage": "2. Model score", "Input": "Expanded clinical logistic model", "Purpose": "Provide explainable pre-discharge risk estimate"},
        {"Stage": "3. Clinical review", "Input": "Care team judgment and patient context", "Purpose": "Avoid single-model decision risk"},
        {"Stage": "4. Intervention assignment", "Input": "Risk level, discharge plan, follow-up needs", "Purpose": "Target support earlier and more consistently"},
        {"Stage": "5. Monthly validation", "Input": "Recall, precision, intervention workload, outcomes", "Purpose": "Balance missed risk and incorrect assignment"},
    ])
    write_text(deliverable / "analysis" / "threshold_guidance.md", """# Threshold Guidance

The selected operational approach is broad coverage rather than a decile-10-only pilot. Use risk deciles 8-10 as the default high-risk group, then add clinical rules for emergency admissions, skilled nursing discharges, high chronic condition burden, and repeated prior admissions.

The model should not be the sole decision engine. It should be one layer in a staged workflow that combines model scores, clinical rules, care team review, intervention assignment, and monthly validation.
""")
    write_review_notes(deliverable, "Model Evaluation Report", [
        "Use `analysis/model_comparison_summary.csv` for the model comparison table.",
        "Use `analysis/staged_model_workflow.csv` to explain why healthcare risk decisions should not depend on one model.",
        "Use risk decile visuals for operational interpretation.",
    ], [
        "Model results require validation before clinical production use.",
        "Thresholds should be reviewed with care coordination capacity and clinical governance.",
    ])
    write_draft_outline(deliverable, "Model Evaluation Report", [
        "Modeling Objective",
        "Target Variable",
        "Feature Set",
        "Model Comparison",
        "Confusion Matrix",
        "Feature Importance",
        "Risk Decile Interpretation",
        "Staged Operational Workflow",
        "Limitations",
    ])


def populate_clinical_care_report() -> None:
    deliverable = DELIVERABLES / "04_clinical_care_coordination_report"
    copy_data(deliverable, [
        ("sections/04_clinical_analysis/data/clinical_readmission_segments.csv", "Clinical high-risk segment analysis.", "clinical_readmission_segments.csv"),
        ("sections/06_care_coordination_analysis/data/intervention_effectiveness_summary.csv", "Observed intervention comparisons.", "intervention_effectiveness_summary.csv"),
        ("sections/06_care_coordination_analysis/data/intervention_count_summary.csv", "Intervention count relationship.", "intervention_count_summary.csv"),
        ("sections/06_care_coordination_analysis/data/follow_up_timing_summary.csv", "Follow-up timing summary.", "follow_up_timing_summary.csv"),
        ("sections/05_predictive_modeling_results/data/risk_score_deciles.csv", "High-risk decile support.", "risk_score_deciles.csv"),
    ])
    copy_images(deliverable, [
        ("sections/04_clinical_analysis/images/readmission_by_diagnosis.svg", "Diagnosis visual.", "readmission_by_diagnosis.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_chronic_condition_bucket.svg", "Chronic burden visual.", "readmission_by_chronic_condition_bucket.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_prior_admissions.svg", "Prior admissions visual.", "readmission_by_prior_admissions.svg"),
        ("sections/04_clinical_analysis/images/readmission_by_discharge_disposition.svg", "Discharge disposition visual.", "readmission_by_discharge_disposition.svg"),
        ("sections/06_care_coordination_analysis/images/readmission_by_intervention.svg", "Intervention comparison visual.", "readmission_by_intervention.svg"),
        ("sections/06_care_coordination_analysis/images/readmission_by_intervention_count.svg", "Intervention count visual.", "readmission_by_intervention_count.svg"),
        ("sections/06_care_coordination_analysis/images/readmission_by_follow_up_timing.svg", "Follow-up timing visual.", "readmission_by_follow_up_timing.svg"),
    ])
    segments = read_csv("sections/04_clinical_analysis/data/clinical_readmission_segments.csv")
    profile = sorted(segments, key=lambda row: float(row["readmission_rate"]), reverse=True)[:12]
    write_csv(deliverable / "analysis" / "high_risk_profile_matrix.csv", [
        {
            "Segment Type": row["segment_type"],
            "Segment": row["segment"],
            "Patients": int(row["patient_count"]),
            "Readmission Rate": pct(row["readmission_rate"]),
            "Action Implication": "Prioritize for high-risk workflow review",
        }
        for row in profile
    ])
    write_csv(deliverable / "analysis" / "care_redesign_evidence_matrix.csv", [
        {"Evidence": "Observed intervention differences are associations, not causal effects.", "Implication": "Do not claim current interventions reduce readmissions causally.", "Action": "Redesign targeting and timing before expansion claims."},
        {"Evidence": "High-risk patients may receive more interventions because they are already sicker.", "Implication": "Selection bias can make intervention groups look worse.", "Action": "Evaluate within risk deciles or staged cohorts."},
        {"Evidence": "Unknown follow-up status is material.", "Implication": "Documentation gaps can hide operational failures.", "Action": "Make follow-up status completion a dashboard KPI."},
        {"Evidence": "Risk deciles 8-10 identify broad high-risk coverage.", "Implication": "Narrow decile-10-only pilots may miss meaningful risk.", "Action": "Cover deciles 8-10 plus clinical rules."},
    ])
    write_review_notes(deliverable, "Clinical And Care Coordination Report", [
        "Use `analysis/high_risk_profile_matrix.csv` for clinical priority segments.",
        "Use `analysis/care_redesign_evidence_matrix.csv` to explain the stronger care coordination conclusion.",
        "Use care coordination visuals with the selection-bias caveat visible.",
    ], [
        "Intervention comparisons are observed associations, not causal impact estimates.",
        "The recommended conclusion is redesign of targeting and timing, not proof that any one current intervention works or fails.",
    ])
    write_draft_outline(deliverable, "Clinical And Care Coordination Report", [
        "High-Risk Patient Profiles",
        "Diagnosis And Chronic Burden",
        "Prior Admissions And ED Utilization",
        "Discharge Disposition",
        "Care Coordination Findings",
        "Selection Bias Caveat",
        "Targeting And Timing Redesign",
        "Recommended Operating Workflow",
    ])


def populate_financial_report() -> None:
    deliverable = DELIVERABLES / "05_financial_impact_roi_report"
    copy_data(deliverable, [
        ("sections/07_financial_impact_analysis/data/financial_baseline_summary.csv", "Financial baseline by readmission outcome.", "financial_baseline_summary.csv"),
        ("sections/07_financial_impact_analysis/data/financial_by_segment.csv", "Financial summary by clinical and operational segment.", "financial_by_segment.csv"),
        ("sections/07_financial_impact_analysis/data/financial_cost_components.csv", "Cost component totals.", "financial_cost_components.csv"),
        ("sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv", "Conservative, expected, and optimistic ROI scenarios.", "roi_scenarios.csv"),
        ("sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv", "Executive KPI reconciliation.", "dashboard_kpis.csv"),
    ])
    copy_images(deliverable, [
        ("sections/07_financial_impact_analysis/images/financial_cost_components.svg", "Cost component visual.", "financial_cost_components.svg"),
        ("sections/07_financial_impact_analysis/images/total_cost_by_readmission_outcome.svg", "Readmission outcome cost visual.", "total_cost_by_readmission_outcome.svg"),
        ("sections/07_financial_impact_analysis/images/net_reimbursement_gap_by_discharge_disposition.svg", "Reimbursement gap visual.", "net_reimbursement_gap_by_discharge_disposition.svg"),
        ("sections/10_financial_impact_and_roi_analysis/images/net_savings_scenarios.svg", "Net savings scenario visual.", "net_savings_scenarios.svg"),
        ("sections/10_financial_impact_and_roi_analysis/images/roi_scenarios.svg", "ROI scenario visual.", "roi_scenarios.svg"),
    ])
    roi = read_csv("sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv")
    write_csv(deliverable / "analysis" / "roi_summary_matrix.csv", [
        {
            "Scenario": row["scenario"],
            "Readmission Reduction": pct(row["readmission_reduction_rate"]),
            "Implementation Cost": money(row["implementation_cost_assumption"]),
            "Avoided Readmissions": int(row["avoided_readmissions"]),
            "Gross Savings": money(row["gross_savings"]),
            "Net Savings": money(row["net_savings"]),
            "ROI": f"{float(row['roi']):.2f}x",
        }
        for row in roi
    ])
    write_text(deliverable / "analysis" / "financial_assumptions.md", """# Financial Assumptions

## Retained Implementation Cost Assumptions

- Conservative: $1.0M.
- Expected: $1.75M.
- Optimistic: $2.5M.

## Interpretation

These assumptions are retained as planning scenarios. They should not be presented as approved budgets. Finance should validate actual staffing, technology, BI, workflow redesign, and change management costs before budget commitment.

## Data Quality Handling

Financial analyses use nonnegative companion fields where appropriate because the source data contains missing and negative values. The report should preserve this caveat in the main narrative.
""")
    write_review_notes(deliverable, "Financial Impact And ROI Report", [
        "Use `analysis/roi_summary_matrix.csv` for executive ROI tables.",
        "Use `analysis/financial_assumptions.md` for the assumptions caveat.",
        "Use the cost component and ROI visuals for presentation backup.",
    ], [
        "ROI is a planning scenario, not a budget guarantee.",
        "Financial data quality flags remain material and should stay visible.",
    ])
    write_draft_outline(deliverable, "Financial Impact And ROI Report", [
        "Current Financial Baseline",
        "Cost Components",
        "CMS Penalty Exposure",
        "Segment-Level Financial Exposure",
        "ROI Scenario Assumptions",
        "Conservative Scenario",
        "Expected Scenario",
        "Optimistic Scenario",
        "Financial Caveats",
    ])


def populate_dashboard() -> None:
    deliverable = DELIVERABLES / "06_executive_dashboard"
    copy_data(deliverable, [
        ("sections/08_executive_dashboard_walkthrough/data/dashboard_ready_extract.csv", "Primary Tableau data source.", "dashboard_ready_extract.csv"),
        ("sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv", "Dashboard KPI reconciliation.", "dashboard_kpis.csv"),
        ("sections/08_executive_dashboard_walkthrough/data/dashboard_measure_definitions.csv", "Calculated measure definitions.", "dashboard_measure_definitions.csv"),
        ("sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv", "ROI scenario data source.", "roi_scenarios.csv"),
        ("sections/09_strategic_recommendations/data/recommendation_evidence_matrix.csv", "Recommendation Center data source.", "recommendation_evidence_matrix.csv"),
        ("sections/11_implementation_roadmap/data/implementation_roadmap.csv", "Roadmap data source.", "implementation_roadmap.csv"),
        ("sections/11_implementation_roadmap/data/success_metrics.csv", "Success metrics data source.", "success_metrics.csv"),
    ])
    copy_images(deliverable, [
        ("sections/08_executive_dashboard_walkthrough/images/dashboard_wireframe.svg", "Dashboard layout reference.", "dashboard_wireframe.svg"),
        ("deliverables/06_executive_dashboard/images/dashboard_package_preview/dashboard_summary.png", "Workbook preview for dashboard summary.", "dashboard_summary_preview.png"),
        ("deliverables/06_executive_dashboard/images/dashboard_package_preview/dashboard_pages.png", "Workbook preview for page specification.", "dashboard_pages_preview.png"),
        ("deliverables/06_executive_dashboard/images/dashboard_package_preview/measure_definitions.png", "Workbook preview for measure definitions.", "measure_definitions_preview.png"),
        ("deliverables/06_executive_dashboard/images/dashboard_package_preview/validation_checks.png", "Workbook preview for validation checks.", "validation_checks_preview.png"),
    ])
    write_csv(deliverable / "analysis" / "tableau_build_status.csv", [
        {"Component": "Dashboard-ready extract", "Status": "Complete", "Location": "data/dashboard_ready_extract.csv"},
        {"Component": "KPI definitions", "Status": "Complete", "Location": "data/dashboard_measure_definitions.csv"},
        {"Component": "Build workbook", "Status": "Complete", "Location": "final/nhn_dashboard_build_package.xlsx"},
        {"Component": "Tableau build guide", "Status": "Complete", "Location": "final/tableau_dashboard_build_guide.md"},
        {"Component": "Native Tableau workbook", "Status": "Not complete in repository", "Location": "Requires Tableau Desktop"},
        {"Component": "Native dashboard screenshots", "Status": "Not complete in repository", "Location": "Requires Tableau Desktop export"},
    ])
    write_text(deliverable / "analysis" / "dashboard_page_plan.md", """# Dashboard Page Plan

## Tool Direction

Use Tableau first. Power BI remains a backup path.

## Audience

The dashboard is designed for presentation and executive review, not dense daily operational management.

## Pages

1. Executive KPI Summary.
2. Clinical Analytics.
3. Financial Analytics.
4. Care Coordination Analytics.
5. Executive Recommendation Center.

## Required Visible Caveats

- Unknown follow-up status is material.
- Financial fields contain missing and negative source values.
- Intervention comparisons are observed associations, not causal estimates.
- Model output should be one layer in a staged risk workflow.
""")
    write_review_notes(deliverable, "Executive Dashboard", [
        "Use `final/nhn_dashboard_build_package.xlsx` as the Tableau build workbook.",
        "Use `final/tableau_dashboard_build_guide.md` as the step-by-step native dashboard guide.",
        "Use `analysis/tableau_build_status.csv` to track what is ready and what still requires Tableau Desktop.",
    ], [
        "A native Tableau `.twb` or `.twbx` is not generated in this repository.",
        "Dashboard screenshots from Tableau Desktop are still needed if the final submission requires native dashboard proof.",
    ])
    write_draft_outline(deliverable, "Executive Dashboard", [
        "Tableau Data Connection",
        "Calculated Fields",
        "Executive KPI Summary",
        "Clinical Analytics",
        "Financial Analytics",
        "Care Coordination Analytics",
        "Executive Recommendation Center",
        "Validation Checks",
        "Screenshot Export",
    ])


def populate_presentation() -> None:
    deliverable = DELIVERABLES / "07_executive_board_presentation"
    copy_data(deliverable, [
        ("sections/01_executive_summary/data/executive_kpis.csv", "Opening KPI source.", "executive_kpis.csv"),
        ("sections/05_predictive_modeling_results/data/model_metrics.csv", "Model performance slide source.", "model_metrics.csv"),
        ("sections/05_predictive_modeling_results/data/risk_score_deciles.csv", "Risk decile slide source.", "risk_score_deciles.csv"),
        ("sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv", "ROI slide source.", "roi_scenarios.csv"),
        ("sections/09_strategic_recommendations/data/recommendation_evidence_matrix.csv", "Recommendation slide source.", "recommendation_evidence_matrix.csv"),
        ("sections/11_implementation_roadmap/data/implementation_roadmap.csv", "Roadmap slide source.", "implementation_roadmap.csv"),
        ("sections/11_implementation_roadmap/data/success_metrics.csv", "Governance slide source.", "success_metrics.csv"),
    ])
    image_items: list[tuple[str, str, str]] = [
        ("deliverables/07_executive_board_presentation/images/healthcare_analytics_background.png", "Cover backup image.", "healthcare_analytics_background.png"),
        ("deliverables/07_executive_board_presentation/final/preview_overview/contact_sheet.png", "Full deck visual QA contact sheet.", "board_presentation_contact_sheet.png"),
    ]
    for idx in range(1, 16):
        image_items.append((
            f"deliverables/07_executive_board_presentation/final/preview/slide-{idx}.png",
            f"Slide {idx} preview.",
            f"slide_{idx:02d}_preview.png",
        ))
    copy_images(deliverable, image_items)
    write_csv(deliverable / "analysis" / "slide_evidence_map.csv", [
        {"Slide": 1, "Topic": "Title", "Primary Evidence": "Project scope and NHN readmission context", "Source File": "final/executive_board_presentation_content.md"},
        {"Slide": 2, "Topic": "Executive Summary", "Primary Evidence": "KPI baseline, steering decisions, expected ROI", "Source File": "data/executive_kpis.csv"},
        {"Slide": 3, "Topic": "Business Problem", "Primary Evidence": "Historical readmission trend and $42M cost exposure", "Source File": "sections/02_business_problem/data/business_problem_metrics.csv"},
        {"Slide": 4, "Topic": "Data Overview", "Primary Evidence": "12,000 matched patients and data quality issues", "Source File": "sections/03_data_overview/data/data_quality_summary.csv"},
        {"Slide": 5, "Topic": "Clinical Analysis", "Primary Evidence": "High-risk clinical segments", "Source File": "sections/04_clinical_analysis/data/clinical_readmission_segments.csv"},
        {"Slide": 6, "Topic": "Predictive Modeling", "Primary Evidence": "Model metrics and staged workflow", "Source File": "data/model_metrics.csv"},
        {"Slide": 7, "Topic": "Risk Stratification", "Primary Evidence": "Readmission by risk decile", "Source File": "data/risk_score_deciles.csv"},
        {"Slide": 8, "Topic": "Care Coordination", "Primary Evidence": "Observed intervention associations and redesign conclusion", "Source File": "sections/06_care_coordination_analysis/data/intervention_effectiveness_summary.csv"},
        {"Slide": 9, "Topic": "Financial Impact", "Primary Evidence": "Cost components and penalty exposure", "Source File": "sections/07_financial_impact_analysis/data/financial_cost_components.csv"},
        {"Slide": 10, "Topic": "Dashboard Walkthrough", "Primary Evidence": "Tableau-first build package", "Source File": "deliverables/06_executive_dashboard/final/tableau_dashboard_build_guide.md"},
        {"Slide": 11, "Topic": "Recommendations", "Primary Evidence": "Recommendation evidence matrix", "Source File": "data/recommendation_evidence_matrix.csv"},
        {"Slide": 12, "Topic": "ROI", "Primary Evidence": "Scenario model", "Source File": "data/roi_scenarios.csv"},
        {"Slide": 13, "Topic": "Implementation", "Primary Evidence": "12-month roadmap", "Source File": "data/implementation_roadmap.csv"},
        {"Slide": 14, "Topic": "Governance", "Primary Evidence": "Success metrics", "Source File": "data/success_metrics.csv"},
        {"Slide": 15, "Topic": "Decision Points", "Primary Evidence": "Steering decisions and recommendations", "Source File": "PROJECT_STEERING_DECISIONS.md"},
    ])
    write_text(deliverable / "notes" / "speaker_notes_by_slide.md", """# Speaker Notes By Slide

## Slide 1
Frame the project as a data science consulting engagement for NHN's readmission challenge.

## Slide 2
State that the analysis uses multiple lenses: clinical quality, financial and capacity impact, care coordination, data quality, and implementation feasibility.

## Slide 3
Explain why rising readmissions matter before introducing technical analysis.

## Slide 4
Emphasize that the source datasets join cleanly, while follow-up and financial data quality caveats are material.

## Slide 5
Describe high-risk patient profiles and connect them to discharge planning.

## Slide 6
Position the model as one layer in a staged workflow, not as a single decision engine.

## Slide 7
Use deciles 8-10 plus clinical rules for broad high-risk coverage.

## Slide 8
State the selection-bias caveat first, then make the operational recommendation to redesign targeting and timing.

## Slide 9
Present financial exposure as planning evidence, with financial data quality caveats.

## Slide 10
Explain that Tableau is the primary build path and that the workbook package supports native dashboard construction.

## Slide 11
Cover all recommendations together rather than selecting only one main strategy.

## Slide 12
Retain the current implementation cost assumptions and describe ROI as planning scenarios.

## Slide 13
Walk through implementation in stages from governance to model refresh.

## Slide 14
Define how success will be measured after launch.

## Slide 15
Close with decision points that support broad coverage, staged governance, Tableau dashboard development, documentation improvement, and ROI validation.
""")
    write_review_notes(deliverable, "Executive Board Presentation", [
        "Use `final/nhn_readmission_board_presentation.pptx` as the final deck.",
        "Use `images/board_presentation_contact_sheet.png` for quick visual QA.",
        "Use `analysis/slide_evidence_map.csv` to trace each slide to source evidence.",
    ], [
        "Keep data caveats in the main presentation narrative.",
        "Keep the narrative presentation-oriented rather than an overly narrow approval pitch.",
    ])
    write_draft_outline(deliverable, "Executive Board Presentation", [
        "Opening And Context",
        "Executive Summary",
        "Business Problem",
        "Data Overview",
        "Clinical Findings",
        "Modeling And Risk Workflow",
        "Care Coordination Redesign",
        "Financial Impact And ROI",
        "Dashboard Walkthrough",
        "Recommendations",
        "Roadmap And Governance",
        "Decision Points",
    ])


POPULATORS = {
    "01_project_charter": populate_project_charter,
    "02_eda_report": populate_eda_report,
    "03_model_evaluation_report": populate_model_report,
    "04_clinical_care_coordination_report": populate_clinical_care_report,
    "05_financial_impact_roi_report": populate_financial_report,
    "06_executive_dashboard": populate_dashboard,
    "07_executive_board_presentation": populate_presentation,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate supporting assets for deliverable folders.")
    parser.add_argument("deliverables", nargs="+", choices=[*POPULATORS.keys(), "all"])
    args = parser.parse_args()

    targets = list(POPULATORS) if "all" in args.deliverables else args.deliverables
    for target in targets:
        POPULATORS[target]()
        print(f"Populated {target}")


if __name__ == "__main__":
    main()
