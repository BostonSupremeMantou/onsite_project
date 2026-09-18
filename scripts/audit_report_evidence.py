from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "REPORT_EVIDENCE_AUDIT.md"

FINAL_REPORTS = [
    ROOT / "deliverables/01_project_charter/final/project_charter.md",
    ROOT / "deliverables/02_eda_report/final/eda_report.md",
    ROOT / "deliverables/03_model_evaluation_report/final/model_evaluation_report.md",
    ROOT / "deliverables/04_clinical_care_coordination_report/final/clinical_care_coordination_report.md",
    ROOT / "deliverables/05_financial_impact_roi_report/final/financial_impact_roi_report.md",
    ROOT / "deliverables/06_executive_dashboard/final/executive_dashboard_spec.md",
    ROOT / "deliverables/07_executive_board_presentation/final/executive_board_presentation_content.md",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def money(value: float) -> str:
    value = float(value)
    if abs(value) >= 1_000_000:
        amount = value / 1_000_000
        text = f"{amount:.2f}".rstrip("0").rstrip(".")
        if "." not in text:
            text = f"{amount:.1f}"
        return f"${text}M"
    if abs(value) >= 1_000:
        amount = value / 1_000
        text = f"{amount:.2f}".rstrip("0").rstrip(".")
        if "." not in text:
            text = f"{amount:.1f}"
        return f"${text}K"
    return f"${value:,.0f}"


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0])
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def report_checks() -> tuple[list[dict[str, object]], list[str]]:
    rows: list[dict[str, object]] = []
    external_refs: set[str] = set()
    for path in FINAL_REPORTS:
        text = path.read_text(encoding="utf-8")
        refs = set(re.findall(r"EXT-\d+", text))
        external_refs.update(refs)
        rows.append({
            "Report": path.relative_to(ROOT),
            "Evidence Notes": "Present" if "## Evidence Notes" in text else "Missing",
            "References Used": "Present" if "## References Used" in text else "Missing",
            "External References": ", ".join(sorted(refs)) or "None",
        })
    return rows, sorted(external_refs, key=lambda item: int(item.split("-")[1]))


def core_metrics() -> list[dict[str, object]]:
    master = read_csv(ROOT / "data/processed/nhn_patient_level_analysis.csv")
    model_metrics = read_csv(ROOT / "sections/05_predictive_modeling_results/data/model_metrics.csv")
    roi = read_csv(ROOT / "sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv")
    risk_deciles = read_csv(ROOT / "sections/05_predictive_modeling_results/data/risk_score_deciles.csv")

    readmitted = sum(int(float(row["readmitted_within_30_days"])) for row in master)
    total_cost = sum(float(row["total_care_cost_nonnegative"] or 0) for row in master)
    penalty = sum(float(row["penalty_cost_nonnegative"] or 0) for row in master)
    expanded = next(row for row in model_metrics if row["model"] == "Expanded clinical logistic model")
    expected = next(row for row in roi if row["scenario"] == "Expected")
    decile_10 = next(row for row in risk_deciles if row["risk_decile"] == "10")

    return [
        {
            "Metric": "Integrated patient records",
            "Recomputed Value": f"{len(master):,}",
            "Source": "data/processed/nhn_patient_level_analysis.csv",
        },
        {
            "Metric": "30-day readmitted patients",
            "Recomputed Value": f"{readmitted:,}",
            "Source": "data/processed/nhn_patient_level_analysis.csv",
        },
        {
            "Metric": "30-day readmission rate",
            "Recomputed Value": pct(readmitted / len(master)),
            "Source": "data/processed/nhn_patient_level_analysis.csv",
        },
        {
            "Metric": "Total care cost, nonnegative field",
            "Recomputed Value": money(total_cost),
            "Source": "data/processed/nhn_patient_level_analysis.csv",
        },
        {
            "Metric": "CMS penalty exposure, nonnegative field",
            "Recomputed Value": money(penalty),
            "Source": "data/processed/nhn_patient_level_analysis.csv",
        },
        {
            "Metric": "Expanded model ROC-AUC",
            "Recomputed Value": f"{float(expanded['roc_auc']):.2f}",
            "Source": "sections/05_predictive_modeling_results/data/model_metrics.csv",
        },
        {
            "Metric": "Expanded model recall",
            "Recomputed Value": pct(float(expanded["recall"])),
            "Source": "sections/05_predictive_modeling_results/data/model_metrics.csv",
        },
        {
            "Metric": "Risk decile 10 readmission rate",
            "Recomputed Value": pct(float(decile_10["readmission_rate"])),
            "Source": "sections/05_predictive_modeling_results/data/risk_score_deciles.csv",
        },
        {
            "Metric": "Expected scenario avoided readmissions",
            "Recomputed Value": f"{int(float(expected['avoided_readmissions'])):,}",
            "Source": "sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv",
        },
        {
            "Metric": "Expected scenario net savings",
            "Recomputed Value": money(float(expected["net_savings"])),
            "Source": "sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv",
        },
    ]


def main() -> None:
    checks, refs = report_checks()
    metrics = core_metrics()
    content = f"""# Report Evidence Audit

This audit checks whether the final written deliverables are tied to project data and substantive references.

## Final Report Citation Coverage

{table(checks)}

## External Reference Coverage

- Distinct external references used across final reports: {len(refs)}
- External IDs used: {", ".join(refs)}
- Minimum required by project steering: 6
- Status: {"Pass" if len(refs) >= 6 else "Needs more references"}

## Recomputed Core Metrics

{table(metrics)}

## Writing Controls

- Numerical claims should be traceable to `data/processed/nhn_patient_level_analysis.csv` or section-level CSV outputs.
- Care coordination intervention comparisons remain descriptive and should not be written as causal claims.
- ROI should be labeled as scenario analysis, not guaranteed savings.
- Model results should be described as planning and prioritization evidence until validated for clinical production.
"""
    REPORT_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
