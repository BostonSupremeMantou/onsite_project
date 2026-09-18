from __future__ import annotations

import html
import json
import math
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MASTER_PATH = ROOT / "data" / "processed" / "nhn_patient_level_analysis.csv"
SECTIONS = ROOT / "sections"

BLUE = "#2563eb"
TEAL = "#0f766e"
GREEN = "#16a34a"
AMBER = "#d97706"
RED = "#dc2626"
SLATE = "#334155"
GRAY = "#64748b"
LIGHT_GRAY = "#e2e8f0"
PALE_BLUE = "#dbeafe"
PALE_TEAL = "#ccfbf1"
PALE_AMBER = "#fef3c7"
PALE_RED = "#fee2e2"


SECTION_DIRS = {
    "01": SECTIONS / "01_executive_summary",
    "02": SECTIONS / "02_business_problem",
    "03": SECTIONS / "03_data_overview",
    "04": SECTIONS / "04_clinical_analysis",
    "05": SECTIONS / "05_predictive_modeling_results",
    "06": SECTIONS / "06_care_coordination_analysis",
    "07": SECTIONS / "07_financial_impact_analysis",
    "08": SECTIONS / "08_executive_dashboard_walkthrough",
    "09": SECTIONS / "09_strategic_recommendations",
    "10": SECTIONS / "10_financial_impact_and_roi_analysis",
    "11": SECTIONS / "11_implementation_roadmap",
}


def ensure_dirs() -> None:
    for section in SECTION_DIRS.values():
        for child in ["analysis", "data", "images", "notes"]:
            (section / child).mkdir(parents=True, exist_ok=True)


def fmt_int(value: float | int) -> str:
    if pd.isna(value):
        return "n.a."
    return f"{int(round(float(value))):,}"


def fmt_pct(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return "n.a."
    return f"{float(value) * 100:.{digits}f}%"


def fmt_pp(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return "n.a."
    return f"{float(value) * 100:.{digits}f} pp"


def fmt_money(value: float, digits: int = 1) -> str:
    if pd.isna(value):
        return "n.a."
    value = float(value)
    sign = "-" if value < 0 else ""
    value = abs(value)
    if value >= 1_000_000:
        return f"{sign}${value / 1_000_000:.{digits}f}M"
    if value >= 1_000:
        return f"{sign}${value / 1_000:.{digits}f}K"
    return f"{sign}${value:,.0f}"


def clean_text(value: object) -> str:
    return html.escape(str(value))


def wrap_svg_text(text: str, max_chars: int = 42) -> list[str]:
    return textwrap.wrap(str(text), width=max_chars, break_long_words=False) or [""]


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>',
        '.title{font-family:Arial,Helvetica,sans-serif;font-size:30px;font-weight:700;fill:#0f172a}',
        '.subtitle{font-family:Arial,Helvetica,sans-serif;font-size:16px;fill:#475569}',
        '.label{font-family:Arial,Helvetica,sans-serif;font-size:15px;fill:#334155}',
        '.small{font-family:Arial,Helvetica,sans-serif;font-size:13px;fill:#64748b}',
        '.value{font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:700;fill:#0f172a}',
        '.kpi{font-family:Arial,Helvetica,sans-serif;font-size:34px;font-weight:700;fill:#0f172a}',
        '</style>',
    ]


def save_svg(path: Path, parts: list[str]) -> None:
    path.write_text("\n".join(parts + ["</svg>"]) + "\n", encoding="utf-8")


def add_title(parts: list[str], title: str, subtitle: str | None = None) -> None:
    parts.append(f'<text x="48" y="52" class="title">{clean_text(title)}</text>')
    if subtitle:
        parts.append(f'<text x="48" y="82" class="subtitle">{clean_text(subtitle)}</text>')


def format_value(value: float, value_kind: str) -> str:
    if value_kind == "percent":
        return fmt_pct(value)
    if value_kind == "money":
        return fmt_money(value)
    if value_kind == "count":
        return fmt_int(value)
    if value_kind == "score":
        return f"{value:.2f}"
    return f"{value:,.1f}"


def horizontal_bar_chart(
    df: pd.DataFrame,
    label_col: str,
    value_col: str,
    path: Path,
    title: str,
    subtitle: str,
    value_kind: str = "percent",
    max_value: float | None = None,
    color: str = BLUE,
    width: int = 1200,
    height: int | None = None,
) -> None:
    plot_df = df[[label_col, value_col]].dropna().copy()
    plot_df[value_col] = pd.to_numeric(plot_df[value_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[value_col])
    if height is None:
        height = max(420, 150 + len(plot_df) * 58)
    max_v = max_value or max(float(plot_df[value_col].max()), 0.01)
    left = 330
    right = width - 170
    top = 128
    bar_h = 28
    row_gap = 58
    parts = svg_header(width, height)
    add_title(parts, title, subtitle)
    parts.append(f'<line x1="{left}" y1="{top - 20}" x2="{right}" y2="{top - 20}" stroke="{LIGHT_GRAY}" stroke-width="1"/>')
    for idx, row in enumerate(plot_df.itertuples(index=False)):
        label = str(getattr(row, label_col))
        value = float(getattr(row, value_col))
        y = top + idx * row_gap
        bar_w = 0 if max_v == 0 else (right - left) * value / max_v
        parts.append(f'<text x="48" y="{y + 20}" class="label">{clean_text(label)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{right - left}" height="{bar_h}" rx="4" fill="#f1f5f9"/>')
        parts.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="{bar_h}" rx="4" fill="{color}"/>')
        parts.append(f'<text x="{right + 18}" y="{y + 20}" class="value">{format_value(value, value_kind)}</text>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Source: Cleaned NHN patient-level analysis dataset.</text>')
    save_svg(path, parts)


def vertical_bar_chart(
    df: pd.DataFrame,
    label_col: str,
    value_col: str,
    path: Path,
    title: str,
    subtitle: str,
    value_kind: str = "percent",
    color: str = BLUE,
    width: int = 1200,
    height: int = 720,
    max_value: float | None = None,
) -> None:
    plot_df = df[[label_col, value_col]].dropna().copy()
    plot_df[value_col] = pd.to_numeric(plot_df[value_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[value_col])
    left = 90
    right = width - 70
    top = 125
    bottom = height - 105
    max_v = max_value or max(float(plot_df[value_col].max()), 0.01)
    bar_area = right - left
    slot = bar_area / max(len(plot_df), 1)
    bar_w = min(80, slot * 0.58)
    parts = svg_header(width, height)
    add_title(parts, title, subtitle)
    parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{SLATE}" stroke-width="1.5"/>')
    for idx, row in enumerate(plot_df.itertuples(index=False)):
        label = str(getattr(row, label_col))
        value = float(getattr(row, value_col))
        x = left + idx * slot + (slot - bar_w) / 2
        bar_h = 0 if max_v == 0 else (bottom - top) * value / max_v
        y = bottom - bar_h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="5" fill="{color}"/>')
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{y - 10:.1f}" text-anchor="middle" class="value">{format_value(value, value_kind)}</text>')
        for line_idx, line in enumerate(wrap_svg_text(label, 14)):
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{bottom + 24 + line_idx * 16}" text-anchor="middle" class="small">{clean_text(line)}</text>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Source: Cleaned NHN patient-level analysis dataset.</text>')
    save_svg(path, parts)


def line_chart(
    df: pd.DataFrame,
    label_col: str,
    value_col: str,
    path: Path,
    title: str,
    subtitle: str,
    width: int = 1200,
    height: int = 680,
) -> None:
    plot_df = df[[label_col, value_col]].dropna().copy()
    plot_df[value_col] = pd.to_numeric(plot_df[value_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[value_col])
    left = 110
    right = width - 95
    top = 130
    bottom = height - 115
    min_v = max(0, float(plot_df[value_col].min()) - 0.02)
    max_v = float(plot_df[value_col].max()) + 0.02
    x_step = (right - left) / max(len(plot_df) - 1, 1)

    def xy(i: int, value: float) -> tuple[float, float]:
        x = left + i * x_step
        y = bottom - ((value - min_v) / (max_v - min_v)) * (bottom - top)
        return x, y

    points = [xy(i, float(v)) for i, v in enumerate(plot_df[value_col])]
    point_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    parts = svg_header(width, height)
    add_title(parts, title, subtitle)
    for tick in np.linspace(min_v, max_v, 5):
        y = bottom - ((tick - min_v) / (max_v - min_v)) * (bottom - top)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="#f1f5f9" stroke-width="1"/>')
        parts.append(f'<text x="{left - 14}" y="{y + 5:.1f}" text-anchor="end" class="small">{fmt_pct(tick)}</text>')
    parts.append(f'<polyline points="{point_str}" fill="none" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    for idx, row in enumerate(plot_df.itertuples(index=False)):
        label = str(getattr(row, label_col))
        value = float(getattr(row, value_col))
        x, y = points[idx]
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{TEAL}" stroke="#ffffff" stroke-width="3"/>')
        parts.append(f'<text x="{x:.1f}" y="{y - 16:.1f}" text-anchor="middle" class="value">{fmt_pct(value)}</text>')
        parts.append(f'<text x="{x:.1f}" y="{bottom + 32}" text-anchor="middle" class="label">{clean_text(label)}</text>')
    parts.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="{SLATE}" stroke-width="1.5"/>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Source: NHN engagement packet historical trend.</text>')
    save_svg(path, parts)


def kpi_cards(
    kpis: list[tuple[str, str, str]],
    path: Path,
    title: str,
    subtitle: str,
    width: int = 1200,
    height: int = 620,
) -> None:
    parts = svg_header(width, height)
    add_title(parts, title, subtitle)
    card_w = 340
    card_h = 130
    x0 = 48
    y0 = 128
    gap_x = 35
    gap_y = 34
    fills = [PALE_BLUE, PALE_TEAL, PALE_AMBER, PALE_RED, "#ecfccb", "#f1f5f9"]
    for idx, (label, value, note) in enumerate(kpis):
        row = idx // 3
        col = idx % 3
        x = x0 + col * (card_w + gap_x)
        y = y0 + row * (card_h + gap_y)
        parts.append(f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="10" fill="{fills[idx % len(fills)]}" stroke="#cbd5e1"/>')
        parts.append(f'<text x="{x + 22}" y="{y + 38}" class="label">{clean_text(label)}</text>')
        parts.append(f'<text x="{x + 22}" y="{y + 82}" class="kpi">{clean_text(value)}</text>')
        parts.append(f'<text x="{x + 22}" y="{y + 112}" class="small">{clean_text(note)}</text>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Source: Cleaned NHN analysis data and project packet.</text>')
    save_svg(path, parts)


def simple_flow_diagram(path: Path) -> None:
    width, height = 1200, 650
    parts = svg_header(width, height)
    add_title(parts, "Data Integration Flow", "Three source datasets connect through patient_id.")
    boxes = [
        (70, 155, 275, 120, "Patient Readmission", "Clinical risk and outcome fields"),
        (70, 340, 275, 120, "Care Coordination", "Post-discharge intervention fields"),
        (70, 525, 275, 120, "Financial Impact", "Cost, reimbursement, and penalty fields"),
        (470, 335, 290, 145, "Integrated Analysis Table", "12,000 patient records joined on patient_id"),
        (875, 335, 260, 145, "Section Assets", "Summary tables, charts, notes, and dashboard extracts"),
    ]
    for x, y, w, h, label, note in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>')
        parts.append(f'<text x="{x + 20}" y="{y + 42}" class="value">{clean_text(label)}</text>')
        for idx, line in enumerate(wrap_svg_text(note, 28)):
            parts.append(f'<text x="{x + 20}" y="{y + 72 + idx * 20}" class="small">{clean_text(line)}</text>')
    for y in [215, 400, 585]:
        parts.append(f'<path d="M350 {y} C410 {y}, 410 407, 468 407" fill="none" stroke="{BLUE}" stroke-width="3"/>')
        parts.append(f'<polygon points="468,407 456,400 456,414" fill="{BLUE}"/>')
    parts.append(f'<path d="M762 407 L872 407" fill="none" stroke="{TEAL}" stroke-width="3"/>')
    parts.append(f'<polygon points="872,407 860,400 860,414" fill="{TEAL}"/>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Source: NHN CSV files and cleaned patient-level analysis dataset.</text>')
    save_svg(path, parts)


def dashboard_wireframe(path: Path) -> None:
    width, height = 1300, 780
    parts = svg_header(width, height)
    add_title(parts, "Executive Dashboard Wireframe", "Recommended Tableau page layout.")
    panels = [
        (50, 120, 250, 110, "KPI Summary", "Readmission rate, high-risk count, total cost, penalties, ROI"),
        (325, 120, 420, 260, "Clinical Analytics", "Risk profiles, diagnosis, chronic burden, readmission patterns"),
        (770, 120, 480, 260, "Financial Analytics", "Cost exposure, penalties, reimbursement gap, ROI scenarios"),
        (50, 260, 250, 280, "Filters", "Diagnosis, age group, admission type, discharge disposition, risk decile"),
        (325, 410, 420, 270, "Care Coordination", "Follow-up, medication review, home health, transportation, calls"),
        (770, 410, 480, 270, "Recommendation Center", "Top priorities, expected impact, implementation phase"),
    ]
    colors = [PALE_BLUE, "#f8fafc", "#f8fafc", "#f1f5f9", "#f8fafc", PALE_TEAL]
    for idx, (x, y, w, h, label, note) in enumerate(panels):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{colors[idx]}" stroke="#94a3b8" stroke-width="1.5"/>')
        parts.append(f'<text x="{x + 22}" y="{y + 40}" class="value">{clean_text(label)}</text>')
        for line_idx, line in enumerate(wrap_svg_text(note, 42)):
            parts.append(f'<text x="{x + 22}" y="{y + 75 + line_idx * 21}" class="small">{clean_text(line)}</text>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Build using dashboard_ready_extract.csv, dashboard_kpis.csv, and roi_scenarios.csv.</text>')
    save_svg(path, parts)


def matrix_chart(df: pd.DataFrame, path: Path, title: str, subtitle: str) -> None:
    width, height = 1100, 780
    left, right, top, bottom = 120, 1000, 135, 665
    parts = svg_header(width, height)
    add_title(parts, title, subtitle)
    parts.append(f'<rect x="{left}" y="{top}" width="{right - left}" height="{bottom - top}" fill="#f8fafc" stroke="#cbd5e1"/>')
    for i in range(1, 5):
        x = left + i * (right - left) / 5
        y = top + i * (bottom - top) / 5
        parts.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="#e2e8f0"/>')
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="#e2e8f0"/>')
    parts.append(f'<text x="{(left + right) / 2}" y="{bottom + 55}" text-anchor="middle" class="label">Implementation effort</text>')
    parts.append(f'<text x="{left - 65}" y="{(top + bottom) / 2}" text-anchor="middle" class="label" transform="rotate(-90 {left - 65},{(top + bottom) / 2})">Expected impact</text>')
    colors = [BLUE, TEAL, AMBER, RED, GREEN]
    for idx, row in df.iterrows():
        impact = float(row["impact_score"])
        effort = float(row["effort_score"])
        x = left + (effort - 0.5) / 5 * (right - left)
        y = bottom - (impact - 0.5) / 5 * (bottom - top)
        label = str(row["short_label"])
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="{colors[idx % len(colors)]}" fill-opacity="0.88" stroke="#ffffff" stroke-width="3"/>')
        parts.append(f'<text x="{x + 24:.1f}" y="{y + 5:.1f}" class="small">{clean_text(label)}</text>')
    parts.append(f'<text x="48" y="{height - 28}" class="small">Scores are preliminary planning estimates based on observed impact, feasibility, and presentation requirements.</text>')
    save_svg(path, parts)


def timeline_chart(df: pd.DataFrame, path: Path) -> None:
    width, height = 1200, 680
    parts = svg_header(width, height)
    add_title(parts, "12-Month Implementation Roadmap", "Recommended sequence for turning analytics into operational action.")
    phases = [
        ("0-3 months", 75, 165, 300, PALE_BLUE),
        ("3-6 months", 450, 165, 300, PALE_TEAL),
        ("6-12 months", 825, 165, 300, PALE_AMBER),
    ]
    for phase, x, y, w, fill in phases:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="400" rx="12" fill="{fill}" stroke="#94a3b8"/>')
        parts.append(f'<text x="{x + 22}" y="{y + 42}" class="value">{clean_text(phase)}</text>')
        tasks = df[df["phase"].eq(phase)]["initiative"].tolist()
        yy = y + 82
        for task in tasks:
            for line in wrap_svg_text(task, 30):
                parts.append(f'<text x="{x + 22}" y="{yy}" class="small">{clean_text(line)}</text>')
                yy += 18
            yy += 10
    parts.append(f'<text x="48" y="{height - 28}" class="small">Source: Derived from NHN project findings and implementation constraints.</text>')
    save_svg(path, parts)


def risk_matrix_chart(path: Path) -> None:
    df = pd.DataFrame(
        [
            {"short_label": "Workflow adoption", "impact_score": 4.5, "effort_score": 3.5},
            {"short_label": "Data quality", "impact_score": 4.0, "effort_score": 2.5},
            {"short_label": "Staff capacity", "impact_score": 4.2, "effort_score": 4.0},
            {"short_label": "Model governance", "impact_score": 3.5, "effort_score": 3.0},
            {"short_label": "Dashboard upkeep", "impact_score": 3.0, "effort_score": 2.0},
        ]
    )
    matrix_chart(df, path, "Implementation Risk Matrix", "Higher impact risks need earlier mitigation planning.")


def segment_summary(df: pd.DataFrame, column: str, segment_type: str) -> pd.DataFrame:
    grouped = (
        df.groupby(column, dropna=False)
        .agg(
            patient_count=("patient_id", "count"),
            readmitted_count=("readmitted_within_30_days", "sum"),
            readmission_rate=("readmitted_within_30_days", "mean"),
            avg_total_care_cost=("total_care_cost_nonnegative", "mean"),
            avg_net_reimbursement_gap=("net_reimbursement_gap", "mean"),
        )
        .reset_index()
        .rename(columns={column: "segment"})
    )
    grouped.insert(0, "segment_type", segment_type)
    return grouped.sort_values(["segment_type", "readmission_rate"], ascending=[True, False])


def auc_score(y_true: np.ndarray, scores: np.ndarray) -> float:
    order = np.argsort(scores)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    positive = y_true == 1
    n_positive = int(positive.sum())
    n_negative = int(len(y_true) - n_positive)
    if n_positive == 0 or n_negative == 0:
        return float("nan")
    return float((ranks[positive].sum() - n_positive * (n_positive + 1) / 2) / (n_positive * n_negative))


def model_metrics(y_true: np.ndarray, scores: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    pred = scores >= threshold
    tp = int(((pred == 1) & (y_true == 1)).sum())
    tn = int(((pred == 0) & (y_true == 0)).sum())
    fp = int(((pred == 1) & (y_true == 0)).sum())
    fn = int(((pred == 0) & (y_true == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {
        "accuracy": (tp + tn) / len(y_true),
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": auc_score(y_true, scores),
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "predicted_positive_rate": float(pred.mean()),
    }


def fit_logistic_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    learning_rate: float = 0.05,
    epochs: int = 6000,
    l2: float = 0.1,
) -> np.ndarray:
    weights = np.zeros(X_train.shape[1])
    for _ in range(epochs):
        logits = np.clip(X_train @ weights, -30, 30)
        probs = 1 / (1 + np.exp(-logits))
        gradient = X_train.T @ (probs - y_train) / len(y_train)
        gradient[1:] += l2 * weights[1:] / len(y_train)
        weights -= learning_rate * gradient
    return weights


def build_design_matrix(df: pd.DataFrame, numeric_cols: list[str], categorical_cols: list[str]) -> tuple[pd.DataFrame, list[str]]:
    numeric = df[numeric_cols].astype(float).copy()
    if categorical_cols:
        categorical = pd.get_dummies(df[categorical_cols].astype(str), drop_first=True, dtype=float)
    else:
        categorical = pd.DataFrame(index=df.index)
    features = pd.concat([numeric, categorical], axis=1)
    return features, list(features.columns)


def train_logistic_model(
    df: pd.DataFrame,
    numeric_cols: list[str],
    categorical_cols: list[str],
    model_name: str,
) -> dict:
    features, feature_names = build_design_matrix(df, numeric_cols, categorical_cols)
    y = df["readmitted_within_30_days"].to_numpy(dtype=float)
    rng = np.random.default_rng(42)
    indices = np.arange(len(y))
    rng.shuffle(indices)
    split_at = int(len(indices) * 0.7)
    train_idx = indices[:split_at]
    test_idx = indices[split_at:]

    train_values = features.iloc[train_idx].to_numpy(dtype=float)
    test_values = features.iloc[test_idx].to_numpy(dtype=float)
    means = train_values.mean(axis=0)
    stds = train_values.std(axis=0)
    stds[stds == 0] = 1

    x_train = (train_values - means) / stds
    x_test = (test_values - means) / stds
    x_all = (features.to_numpy(dtype=float) - means) / stds
    x_train = np.column_stack([np.ones(len(x_train)), x_train])
    x_test = np.column_stack([np.ones(len(x_test)), x_test])
    x_all = np.column_stack([np.ones(len(x_all)), x_all])

    weights = fit_logistic_regression(x_train, y[train_idx])
    test_scores = 1 / (1 + np.exp(-np.clip(x_test @ weights, -30, 30)))
    all_scores = 1 / (1 + np.exp(-np.clip(x_all @ weights, -30, 30)))

    metrics = model_metrics(y[test_idx], test_scores)
    metrics["model"] = model_name
    metrics["test_records"] = len(test_idx)

    coefficients = pd.DataFrame(
        {
            "model": model_name,
            "feature": ["intercept"] + feature_names,
            "coefficient": weights,
        }
    )
    coefficients["absolute_coefficient"] = coefficients["coefficient"].abs()
    coefficients = coefficients.sort_values("absolute_coefficient", ascending=False)
    return {
        "metrics": metrics,
        "coefficients": coefficients,
        "all_scores": all_scores,
        "test_scores": test_scores,
        "test_actual": y[test_idx],
        "test_index": test_idx,
    }


def generate_assets() -> None:
    ensure_dirs()
    df = pd.read_csv(MASTER_PATH)
    total_patients = len(df)
    readmission_rate = df["readmitted_within_30_days"].mean()
    readmitted_count = int(df["readmitted_within_30_days"].sum())
    total_care_cost = df["total_care_cost_nonnegative"].sum()
    penalty_cost = df["penalty_cost_nonnegative"].sum()
    avg_gap = df["net_reimbursement_gap"].mean()

    historical = pd.DataFrame(
        {
            "year": ["2022", "2023", "2024", "2025"],
            "readmission_rate": [0.142, 0.158, 0.169, 0.184],
        }
    )
    historical.to_csv(SECTION_DIRS["02"] / "data" / "historical_readmission_trend.csv", index=False)
    line_chart(
        historical,
        "year",
        "readmission_rate",
        SECTION_DIRS["02"] / "images" / "historical_readmission_trend.svg",
        "Historical 30-Day Readmission Rate",
        "NHN engagement packet trend shows sustained annual increases.",
    )

    # Shared segment tables.
    segment_frames = [
        segment_summary(df, "primary_diagnosis", "Primary diagnosis"),
        segment_summary(df, "admission_type", "Admission type"),
        segment_summary(df, "discharge_disposition", "Discharge disposition"),
        segment_summary(df, "follow_up_status", "Follow-up status"),
        segment_summary(df, "age_group", "Age group"),
        segment_summary(df, "chronic_condition_bucket", "Chronic condition bucket"),
        segment_summary(df, "prior_admissions_bucket", "Prior admissions bucket"),
        segment_summary(df, "ed_visits_bucket", "ED visits bucket"),
    ]
    all_segments = pd.concat(segment_frames, ignore_index=True)
    all_segments.to_csv(SECTION_DIRS["04"] / "data" / "clinical_readmission_segments.csv", index=False)
    all_segments.to_csv(SECTION_DIRS["02"] / "data" / "readmission_by_business_driver.csv", index=False)

    business_metrics = pd.DataFrame(
        [
            {"metric": "Analytical dataset patients", "value": total_patients, "display_value": fmt_int(total_patients)},
            {"metric": "Readmitted within 30 days", "value": readmitted_count, "display_value": fmt_int(readmitted_count)},
            {"metric": "Analytical dataset readmission rate", "value": readmission_rate, "display_value": fmt_pct(readmission_rate)},
            {"metric": "Total care cost in cleaned dataset", "value": total_care_cost, "display_value": fmt_money(total_care_cost)},
            {"metric": "CMS penalty exposure in cleaned dataset", "value": penalty_cost, "display_value": fmt_money(penalty_cost)},
            {"metric": "Average net reimbursement gap", "value": avg_gap, "display_value": fmt_money(avg_gap)},
        ]
    )
    business_metrics.to_csv(SECTION_DIRS["02"] / "data" / "business_problem_metrics.csv", index=False)

    # Core clinical visuals.
    for section, segment_type, filename, title in [
        ("04", "Primary diagnosis", "readmission_by_diagnosis.svg", "Readmission Rate By Diagnosis"),
        ("04", "Age group", "readmission_by_age_group.svg", "Readmission Rate By Age Group"),
        ("04", "Chronic condition bucket", "readmission_by_chronic_condition_bucket.svg", "Readmission Rate By Chronic Condition Burden"),
        ("04", "Prior admissions bucket", "readmission_by_prior_admissions.svg", "Readmission Rate By Prior Admissions"),
        ("04", "ED visits bucket", "readmission_by_ed_visits.svg", "Readmission Rate By ED Utilization"),
        ("04", "Discharge disposition", "readmission_by_discharge_disposition.svg", "Readmission Rate By Discharge Disposition"),
    ]:
        chart_df = all_segments[all_segments["segment_type"].eq(segment_type)].sort_values("readmission_rate", ascending=True)
        horizontal_bar_chart(
            chart_df,
            "segment",
            "readmission_rate",
            SECTION_DIRS[section] / "images" / filename,
            title,
            "Rates calculated from the cleaned integrated patient-level table.",
            "percent",
            max_value=max(0.65, float(chart_df["readmission_rate"].max()) * 1.08),
            color=TEAL if "Age" not in segment_type else BLUE,
        )

    for segment_type, filename, title in [
        ("Admission type", "readmission_by_admission_type.svg", "Readmission Rate By Admission Type"),
        ("Follow-up status", "readmission_by_follow_up_status.svg", "Readmission Rate By Follow-Up Status"),
    ]:
        chart_df = all_segments[all_segments["segment_type"].eq(segment_type)].sort_values("readmission_rate", ascending=True)
        horizontal_bar_chart(
            chart_df,
            "segment",
            "readmission_rate",
            SECTION_DIRS["02"] / "images" / filename,
            title,
            "These are observed rates, not causal estimates.",
            "percent",
            max_value=max(0.65, float(chart_df["readmission_rate"].max()) * 1.08),
            color=BLUE,
        )

    # Data overview.
    source_profile = pd.DataFrame(
        [
            {
                "dataset": "Patient Readmission",
                "rows": len(df),
                "unique_patient_ids": df["patient_id"].nunique(),
                "key_fields": "Clinical risk, admission, discharge, and readmission outcome",
            },
            {
                "dataset": "Financial Impact",
                "rows": len(df),
                "unique_patient_ids": df["patient_id"].nunique(),
                "key_fields": "Readmission cost, reimbursement, penalties, length-of-stay cost, total care cost",
            },
            {
                "dataset": "Care Coordination",
                "rows": len(df),
                "unique_patient_ids": df["patient_id"].nunique(),
                "key_fields": "Care coordinator assignment, follow-up, medication review, home health, transportation, calls",
            },
        ]
    )
    source_profile.to_csv(SECTION_DIRS["03"] / "data" / "source_dataset_profile.csv", index=False)
    quality_rows = []
    issue_fields = [
        ("Patient", "insurance_type_missing_flag", "Missing insurance type"),
        ("Patient", "follow_up_status_missing_flag", "Missing follow-up status"),
        ("Patient", "length_of_stay_days_missing_flag", "Missing length of stay"),
        ("Financial", "penalty_cost_missing_flag", "Missing penalty cost"),
        ("Financial", "follow_up_program_cost_missing_flag", "Missing follow-up program cost"),
        ("Financial", "readmission_cost_negative_flag", "Negative readmission cost"),
        ("Financial", "reimbursement_amount_negative_flag", "Negative reimbursement amount"),
        ("Financial", "penalty_cost_negative_flag", "Negative penalty cost"),
        ("Financial", "length_of_stay_cost_negative_flag", "Negative length-of-stay cost"),
        ("Financial", "follow_up_program_cost_negative_flag", "Negative follow-up program cost"),
        ("Care Coordination", "follow_up_days_after_discharge_missing_flag", "Missing follow-up days"),
        ("Care Coordination", "post_discharge_calls_missing_flag", "Missing post-discharge calls"),
    ]
    for dataset, field, issue in issue_fields:
        count = int(df[field].sum())
        quality_rows.append(
            {
                "dataset": dataset,
                "issue": issue,
                "affected_rows": count,
                "affected_rate": count / total_patients,
            }
        )
    quality_summary = pd.DataFrame(quality_rows).sort_values("affected_rows", ascending=False)
    quality_summary.to_csv(SECTION_DIRS["03"] / "data" / "data_quality_summary.csv", index=False)
    horizontal_bar_chart(
        quality_summary.head(8).sort_values("affected_rows", ascending=True),
        "issue",
        "affected_rows",
        SECTION_DIRS["03"] / "images" / "missing_values_summary.svg",
        "Largest Data Quality Flags",
        "Flags preserve raw values while identifying records needing caution.",
        "count",
        color=AMBER,
    )
    simple_flow_diagram(SECTION_DIRS["03"] / "images" / "data_flow.svg")

    # Modeling.
    baseline = train_logistic_model(
        df,
        ["age", "chronic_conditions", "prior_admissions_12m", "length_of_stay_days_imputed", "ed_visits_12m"],
        [],
        "Baseline numeric clinical logistic model",
    )
    expanded = train_logistic_model(
        df,
        ["age", "chronic_conditions", "prior_admissions_12m", "length_of_stay_days_imputed", "ed_visits_12m"],
        ["gender", "insurance_type", "primary_diagnosis", "admission_type", "discharge_disposition"],
        "Expanded clinical logistic model",
    )
    metrics = pd.DataFrame([baseline["metrics"], expanded["metrics"]])
    metric_cols = ["model", "accuracy", "precision", "recall", "f1_score", "roc_auc", "true_positive", "true_negative", "false_positive", "false_negative", "predicted_positive_rate", "test_records"]
    metrics = metrics[metric_cols]
    metrics.to_csv(SECTION_DIRS["05"] / "data" / "model_metrics.csv", index=False)
    metrics_long = metrics.melt(
        id_vars="model",
        value_vars=["accuracy", "precision", "recall", "f1_score", "roc_auc"],
        var_name="metric",
        value_name="value",
    )
    metrics_long["label"] = metrics_long["model"].str.replace(" logistic model", "", regex=False) + " - " + metrics_long["metric"].str.replace("_", " ").str.title()
    horizontal_bar_chart(
        metrics_long.sort_values("value", ascending=True),
        "label",
        "value",
        SECTION_DIRS["05"] / "images" / "model_metrics_comparison.svg",
        "Model Performance Comparison",
        "Holdout-set metrics at a 0.50 classification threshold.",
        "percent",
        max_value=1.0,
        color=BLUE,
        height=760,
    )
    feature_importance = expanded["coefficients"].query("feature != 'intercept'").head(15).copy()
    feature_importance.to_csv(SECTION_DIRS["05"] / "data" / "model_feature_importance.csv", index=False)
    horizontal_bar_chart(
        feature_importance.sort_values("absolute_coefficient", ascending=True),
        "feature",
        "absolute_coefficient",
        SECTION_DIRS["05"] / "images" / "feature_importance.svg",
        "Expanded Model Feature Importance",
        "Importance uses absolute standardized logistic coefficients.",
        "score",
        color=TEAL,
        height=980,
    )
    expanded_pred = (expanded["test_scores"] >= 0.5).astype(int)
    y_test = expanded["test_actual"].astype(int)
    confusion = pd.DataFrame(
        [
            {"actual": "Not readmitted", "predicted": "Not readmitted", "count": int(((expanded_pred == 0) & (y_test == 0)).sum())},
            {"actual": "Not readmitted", "predicted": "Readmitted", "count": int(((expanded_pred == 1) & (y_test == 0)).sum())},
            {"actual": "Readmitted", "predicted": "Not readmitted", "count": int(((expanded_pred == 0) & (y_test == 1)).sum())},
            {"actual": "Readmitted", "predicted": "Readmitted", "count": int(((expanded_pred == 1) & (y_test == 1)).sum())},
        ]
    )
    confusion.to_csv(SECTION_DIRS["05"] / "data" / "model_confusion_matrix.csv", index=False)
    vertical_bar_chart(
        confusion.assign(label=confusion["actual"] + " / " + confusion["predicted"]),
        "label",
        "count",
        SECTION_DIRS["05"] / "images" / "confusion_matrix_expanded_clinical.svg",
        "Expanded Model Confusion Matrix",
        "Counts from the holdout test set.",
        "count",
        color=AMBER,
        height=760,
    )
    df["preliminary_readmission_risk_score"] = expanded["all_scores"]
    df["risk_decile"] = pd.qcut(df["preliminary_readmission_risk_score"], 10, labels=[str(i) for i in range(1, 11)])
    risk_deciles = (
        df.groupby("risk_decile", observed=True)
        .agg(
            patient_count=("patient_id", "count"),
            average_risk_score=("preliminary_readmission_risk_score", "mean"),
            readmission_rate=("readmitted_within_30_days", "mean"),
        )
        .reset_index()
    )
    risk_deciles.to_csv(SECTION_DIRS["05"] / "data" / "risk_score_deciles.csv", index=False)
    vertical_bar_chart(
        risk_deciles,
        "risk_decile",
        "readmission_rate",
        SECTION_DIRS["05"] / "images" / "risk_decile_readmission_rate.svg",
        "Observed Readmission Rate By Model Risk Decile",
        "Higher deciles should receive earlier review and targeted intervention.",
        "percent",
        color=TEAL,
        max_value=max(0.75, float(risk_deciles["readmission_rate"].max()) * 1.08),
    )

    # Care coordination.
    intervention_cols = [
        ("care_coordinator_assigned", "Care coordinator assigned"),
        ("follow_up_completed", "Follow-up completed"),
        ("medication_review_completed", "Medication review completed"),
        ("home_health_referral", "Home health referral"),
        ("transportation_assistance_provided", "Transportation assistance"),
        ("any_post_discharge_call_flag", "Any post-discharge call"),
    ]
    intervention_rows = []
    for col, label in intervention_cols:
        grouped = df.groupby(col)["readmitted_within_30_days"].agg(["count", "mean"]).rename(columns={"count": "patient_count", "mean": "readmission_rate"})
        yes_rate = float(grouped.loc[1, "readmission_rate"])
        no_rate = float(grouped.loc[0, "readmission_rate"])
        intervention_rows.append(
            {
                "intervention": label,
                "patients_with_intervention": int(grouped.loc[1, "patient_count"]),
                "patients_without_intervention": int(grouped.loc[0, "patient_count"]),
                "readmission_rate_with_intervention": yes_rate,
                "readmission_rate_without_intervention": no_rate,
                "observed_difference_pp": yes_rate - no_rate,
            }
        )
    interventions = pd.DataFrame(intervention_rows).sort_values("readmission_rate_with_intervention")
    interventions.to_csv(SECTION_DIRS["06"] / "data" / "intervention_effectiveness_summary.csv", index=False)
    horizontal_bar_chart(
        interventions.sort_values("readmission_rate_with_intervention", ascending=True),
        "intervention",
        "readmission_rate_with_intervention",
        SECTION_DIRS["06"] / "images" / "readmission_by_intervention.svg",
        "Readmission Rate Among Patients Receiving Each Intervention",
        "Observed rates are not causal because high-risk patients may be more likely to receive support.",
        "percent",
        max_value=0.52,
        color=BLUE,
    )
    intervention_count = (
        df.groupby("intervention_count")
        .agg(patient_count=("patient_id", "count"), readmission_rate=("readmitted_within_30_days", "mean"))
        .reset_index()
    )
    intervention_count.to_csv(SECTION_DIRS["06"] / "data" / "intervention_count_summary.csv", index=False)
    vertical_bar_chart(
        intervention_count,
        "intervention_count",
        "readmission_rate",
        SECTION_DIRS["06"] / "images" / "readmission_by_intervention_count.svg",
        "Readmission Rate By Intervention Count",
        "Intervention count reflects assigned support activities in the care coordination dataset.",
        "percent",
        color=TEAL,
        max_value=0.52,
    )
    df["follow_up_timing_bucket"] = pd.cut(
        df["follow_up_days_after_discharge_imputed"],
        bins=[0, 7, 14, 21, 30],
        labels=["1-7 days", "8-14 days", "15-21 days", "22-30 days"],
        include_lowest=True,
    ).astype(str)
    follow_up_timing = (
        df.groupby("follow_up_timing_bucket")
        .agg(patient_count=("patient_id", "count"), readmission_rate=("readmitted_within_30_days", "mean"))
        .reset_index()
    )
    follow_up_timing.to_csv(SECTION_DIRS["06"] / "data" / "follow_up_timing_summary.csv", index=False)
    vertical_bar_chart(
        follow_up_timing,
        "follow_up_timing_bucket",
        "readmission_rate",
        SECTION_DIRS["06"] / "images" / "readmission_by_follow_up_timing.svg",
        "Readmission Rate By Follow-Up Timing",
        "Timing uses the imputed analysis field and should be reviewed with missing-value flags.",
        "percent",
        color=AMBER,
        max_value=0.5,
    )

    # Financial analysis.
    financial_by_outcome = (
        df.groupby("readmission_label")
        .agg(
            patient_count=("patient_id", "count"),
            avg_total_care_cost=("total_care_cost_nonnegative", "mean"),
            avg_readmission_cost=("readmission_cost_nonnegative", "mean"),
            avg_penalty_cost=("penalty_cost_nonnegative", "mean"),
            avg_net_reimbursement_gap=("net_reimbursement_gap", "mean"),
            total_care_cost=("total_care_cost_nonnegative", "sum"),
            total_penalty_cost=("penalty_cost_nonnegative", "sum"),
        )
        .reset_index()
    )
    financial_by_outcome.to_csv(SECTION_DIRS["07"] / "data" / "financial_baseline_summary.csv", index=False)
    vertical_bar_chart(
        financial_by_outcome,
        "readmission_label",
        "avg_total_care_cost",
        SECTION_DIRS["07"] / "images" / "total_cost_by_readmission_outcome.svg",
        "Average Total Care Cost By Readmission Outcome",
        "Uses nonnegative companion fields from the cleaned financial dataset.",
        "money",
        color=BLUE,
        max_value=float(financial_by_outcome["avg_total_care_cost"].max()) * 1.18,
    )
    components = pd.DataFrame(
        [
            {"component": "Readmission cost", "amount": df["readmission_cost_nonnegative"].sum()},
            {"component": "Length-of-stay cost", "amount": df["length_of_stay_cost_nonnegative"].sum()},
            {"component": "CMS penalty cost", "amount": df["penalty_cost_nonnegative"].sum()},
            {"component": "Follow-up program cost", "amount": df["follow_up_program_cost_nonnegative"].sum()},
        ]
    ).sort_values("amount", ascending=True)
    components.to_csv(SECTION_DIRS["07"] / "data" / "financial_cost_components.csv", index=False)
    horizontal_bar_chart(
        components,
        "component",
        "amount",
        SECTION_DIRS["07"] / "images" / "financial_cost_components.svg",
        "Financial Exposure By Cost Component",
        "Component totals use nonnegative cleaned financial fields.",
        "money",
        color=TEAL,
    )
    financial_segments = all_segments.copy()
    financial_segments.to_csv(SECTION_DIRS["07"] / "data" / "financial_by_segment.csv", index=False)
    penalty_segment = segment_summary(df, "discharge_disposition", "Discharge disposition").sort_values("avg_total_care_cost", ascending=True)
    horizontal_bar_chart(
        penalty_segment,
        "segment",
        "avg_net_reimbursement_gap",
        SECTION_DIRS["07"] / "images" / "net_reimbursement_gap_by_discharge_disposition.svg",
        "Average Net Reimbursement Gap By Discharge Disposition",
        "Gap equals total care cost minus reimbursement amount.",
        "money",
        color=AMBER,
    )

    # ROI scenarios.
    avg_readmission_value = df.loc[df["readmitted_within_30_days"].eq(1), ["readmission_cost_nonnegative", "penalty_cost_nonnegative"]].sum(axis=1).mean()
    scenarios = pd.DataFrame(
        [
            {"scenario": "Conservative", "readmission_reduction_rate": 0.05, "implementation_cost_assumption": 1_000_000},
            {"scenario": "Expected", "readmission_reduction_rate": 0.10, "implementation_cost_assumption": 1_750_000},
            {"scenario": "Optimistic", "readmission_reduction_rate": 0.15, "implementation_cost_assumption": 2_500_000},
        ]
    )
    scenarios["avoided_readmissions"] = (readmitted_count * scenarios["readmission_reduction_rate"]).round().astype(int)
    scenarios["average_avoided_value_per_readmission"] = avg_readmission_value
    scenarios["gross_savings"] = scenarios["avoided_readmissions"] * scenarios["average_avoided_value_per_readmission"]
    scenarios["net_savings"] = scenarios["gross_savings"] - scenarios["implementation_cost_assumption"]
    scenarios["roi"] = scenarios["net_savings"] / scenarios["implementation_cost_assumption"]
    scenarios.to_csv(SECTION_DIRS["10"] / "data" / "roi_scenarios.csv", index=False)
    vertical_bar_chart(
        scenarios,
        "scenario",
        "net_savings",
        SECTION_DIRS["10"] / "images" / "net_savings_scenarios.svg",
        "Estimated Net Savings By Scenario",
        "Preliminary assumptions should be replaced with approved implementation costs.",
        "money",
        color=GREEN,
        max_value=float(scenarios["net_savings"].max()) * 1.2,
    )
    vertical_bar_chart(
        scenarios,
        "scenario",
        "roi",
        SECTION_DIRS["10"] / "images" / "roi_scenarios.svg",
        "Estimated ROI By Scenario",
        "ROI equals net savings divided by implementation cost assumption.",
        "score",
        color=TEAL,
        max_value=float(scenarios["roi"].max()) * 1.2,
    )

    # Dashboard and executive summary.
    kpis = [
        ("Patients analyzed", fmt_int(total_patients), "Matched across all three datasets"),
        ("Readmission rate", fmt_pct(readmission_rate), f"{fmt_int(readmitted_count)} readmitted patients"),
        ("Total care cost", fmt_money(total_care_cost), "Nonnegative cleaned financial field"),
        ("CMS penalty exposure", fmt_money(penalty_cost), "Nonnegative cleaned penalty field"),
        ("Model ROC-AUC", f"{expanded['metrics']['roc_auc']:.2f}", "Expanded clinical model holdout"),
        ("Expected net savings", fmt_money(scenarios.loc[scenarios["scenario"].eq("Expected"), "net_savings"].iloc[0]), "Preliminary ROI scenario"),
    ]
    kpi_cards(
        kpis,
        SECTION_DIRS["01"] / "images" / "executive_kpi_cards.svg",
        "Executive KPI Summary",
        "Board-ready metrics from the current analysis pass.",
    )
    business_metrics.to_csv(SECTION_DIRS["01"] / "data" / "executive_kpis.csv", index=False)
    dashboard_kpis = business_metrics.copy()
    dashboard_kpis.to_csv(SECTION_DIRS["08"] / "data" / "dashboard_kpis.csv", index=False)
    measure_definitions = pd.DataFrame(
        [
            {"measure": "Readmission Rate", "definition": "SUM(readmitted_within_30_days) / COUNT(patient_id)", "recommended_visual": "KPI card and trend or segment bar"},
            {"measure": "High-Risk Patients", "definition": "COUNT(patient_id) where risk_decile is 8, 9, or 10", "recommended_visual": "KPI card and patient segment table"},
            {"measure": "Total Care Cost", "definition": "SUM(total_care_cost_nonnegative)", "recommended_visual": "KPI card and cost component chart"},
            {"measure": "CMS Penalties", "definition": "SUM(penalty_cost_nonnegative)", "recommended_visual": "KPI card and penalty segment chart"},
            {"measure": "ROI", "definition": "net_savings / implementation_cost_assumption from roi_scenarios.csv", "recommended_visual": "Scenario bar chart"},
            {"measure": "Intervention Completion", "definition": "AVG(follow_up_completed), AVG(medication_review_completed), and related binary fields", "recommended_visual": "Care coordination bar chart"},
        ]
    )
    measure_definitions.to_csv(SECTION_DIRS["08"] / "data" / "dashboard_measure_definitions.csv", index=False)
    dashboard_extract_cols = [
        "patient_id",
        "age_group",
        "gender",
        "insurance_type",
        "primary_diagnosis",
        "chronic_condition_bucket",
        "prior_admissions_bucket",
        "ed_visits_bucket",
        "admission_type",
        "discharge_disposition",
        "follow_up_status",
        "readmitted_within_30_days",
        "readmission_label",
        "preliminary_readmission_risk_score",
        "risk_decile",
        "total_care_cost_nonnegative",
        "readmission_cost_nonnegative",
        "penalty_cost_nonnegative",
        "net_reimbursement_gap",
        "care_coordinator_assigned",
        "follow_up_completed",
        "medication_review_completed",
        "home_health_referral",
        "transportation_assistance_provided",
        "any_post_discharge_call_flag",
        "intervention_count",
        "has_data_quality_issue_flag",
    ]
    df[dashboard_extract_cols].to_csv(SECTION_DIRS["08"] / "data" / "dashboard_ready_extract.csv", index=False)
    dashboard_wireframe(SECTION_DIRS["08"] / "images" / "dashboard_wireframe.svg")

    # Recommendations and roadmap.
    recommendations = pd.DataFrame(
        [
            {
                "recommendation": "Deploy a pre-discharge readmission risk score",
                "short_label": "Risk score",
                "evidence": "Expanded clinical model ROC-AUC is 0.74 and risk deciles separate observed readmission rates.",
                "impact_score": 5,
                "effort_score": 3,
                "priority": "High",
                "timeframe": "0-3 months",
            },
            {
                "recommendation": "Prioritize emergency admissions and skilled nursing discharges for enhanced discharge review",
                "short_label": "Discharge review",
                "evidence": "Emergency admissions and skilled nursing discharges show elevated readmission rates.",
                "impact_score": 4,
                "effort_score": 3,
                "priority": "High",
                "timeframe": "0-3 months",
            },
            {
                "recommendation": "Close follow-up documentation and completion gaps",
                "short_label": "Follow-up gaps",
                "evidence": "Unknown follow-up status has the highest observed readmission rate and 2,587 records lack follow-up status.",
                "impact_score": 4,
                "effort_score": 2,
                "priority": "High",
                "timeframe": "0-3 months",
            },
            {
                "recommendation": "Target care coordination resources to high-risk chronic disease and prior-admission groups",
                "short_label": "Targeted care",
                "evidence": "Patients with 5+ chronic conditions and 3+ prior admissions show materially higher readmission rates.",
                "impact_score": 5,
                "effort_score": 4,
                "priority": "High",
                "timeframe": "3-6 months",
            },
            {
                "recommendation": "Launch an executive readmission dashboard",
                "short_label": "Dashboard",
                "evidence": "The project requires integrated clinical, financial, and operational reporting for executive decisions.",
                "impact_score": 3,
                "effort_score": 2,
                "priority": "Medium",
                "timeframe": "3-6 months",
            },
        ]
    )
    recommendations.to_csv(SECTION_DIRS["09"] / "data" / "recommendation_evidence_matrix.csv", index=False)
    matrix_chart(
        recommendations,
        SECTION_DIRS["09"] / "images" / "recommendation_priority_matrix.svg",
        "Recommendation Priority Matrix",
        "Prioritize high-impact actions that can be implemented within the 12-month window.",
    )
    roadmap = pd.DataFrame(
        [
            {"phase": "0-3 months", "initiative": "Approve dashboard KPIs, risk model governance, and readmission reduction targets.", "owner": "Executive sponsor and analytics lead", "success_measure": "Approved definitions and baseline metrics"},
            {"phase": "0-3 months", "initiative": "Pilot pre-discharge risk scoring for emergency admissions and skilled nursing discharges.", "owner": "Clinical operations and analytics", "success_measure": "Risk scores available before discharge"},
            {"phase": "0-3 months", "initiative": "Fix follow-up status documentation workflow and missing-value monitoring.", "owner": "Care coordination leadership", "success_measure": "Reduced unknown follow-up status"},
            {"phase": "3-6 months", "initiative": "Expand targeted care coordination for high-risk chronic disease and prior-admission groups.", "owner": "Care coordination leadership", "success_measure": "Higher intervention completion in high-risk groups"},
            {"phase": "3-6 months", "initiative": "Build Tableau dashboard using the prepared dashboard extract.", "owner": "BI team", "success_measure": "Published executive dashboard"},
            {"phase": "6-12 months", "initiative": "Track ROI, readmission reduction, CMS penalty exposure, and intervention performance monthly.", "owner": "Finance and quality leadership", "success_measure": "Monthly executive review cadence"},
            {"phase": "6-12 months", "initiative": "Refresh and validate the risk model with new outcomes and operational feedback.", "owner": "Analytics and clinical governance", "success_measure": "Updated model performance and threshold review"},
        ]
    )
    roadmap.to_csv(SECTION_DIRS["11"] / "data" / "implementation_roadmap.csv", index=False)
    timeline_chart(roadmap, SECTION_DIRS["11"] / "images" / "implementation_timeline.svg")
    success_metrics = pd.DataFrame(
        [
            {"dimension": "Clinical", "metric": "Readmission rate", "target_direction": "Decrease", "source": "Dashboard extract"},
            {"dimension": "Clinical", "metric": "High-risk patient intervention completion", "target_direction": "Increase", "source": "Care coordination data"},
            {"dimension": "Financial", "metric": "CMS penalty exposure", "target_direction": "Decrease", "source": "Financial impact data"},
            {"dimension": "Financial", "metric": "Net savings", "target_direction": "Increase", "source": "ROI scenario model"},
            {"dimension": "Operational", "metric": "Unknown follow-up status rate", "target_direction": "Decrease", "source": "Patient readmission data"},
            {"dimension": "Analytics", "metric": "Model ROC-AUC and recall", "target_direction": "Maintain or improve", "source": "Model evaluation"},
        ]
    )
    success_metrics.to_csv(SECTION_DIRS["11"] / "data" / "success_metrics.csv", index=False)
    risk_matrix_chart(SECTION_DIRS["11"] / "images" / "risk_matrix.svg")

    # Notes files.
    top_age = all_segments[all_segments["segment_type"].eq("Age group")].sort_values("readmission_rate", ascending=False).iloc[0]
    top_chronic = all_segments[all_segments["segment_type"].eq("Chronic condition bucket")].sort_values("readmission_rate", ascending=False).iloc[0]
    top_prior = all_segments[all_segments["segment_type"].eq("Prior admissions bucket")].sort_values("readmission_rate", ascending=False).iloc[0]
    top_discharge = all_segments[all_segments["segment_type"].eq("Discharge disposition")].sort_values("readmission_rate", ascending=False).iloc[0]
    emergency = all_segments[(all_segments["segment_type"].eq("Admission type")) & (all_segments["segment"].eq("Emergency"))].iloc[0]
    unknown_follow = all_segments[(all_segments["segment_type"].eq("Follow-up status")) & (all_segments["segment"].eq("Unknown"))].iloc[0]
    completed_follow = all_segments[(all_segments["segment_type"].eq("Follow-up status")) & (all_segments["segment"].eq("Completed"))].iloc[0]
    expected = scenarios[scenarios["scenario"].eq("Expected")].iloc[0]
    model_row = metrics[metrics["model"].eq("Expanded clinical logistic model")].iloc[0]

    note_files = {
        SECTION_DIRS["01"] / "notes" / "executive_summary_findings.md": f"""# Executive Summary Findings

## Board-Level Message

NHN's readmission challenge is clinically important, operationally disruptive, and financially material. The cleaned analytical dataset contains {fmt_int(total_patients)} matched patient records and a 30-day readmission rate of {fmt_pct(readmission_rate)}.

## Key Findings

- Highest observed clinical risk appears among the `{top_chronic['segment']}` chronic condition group, with a readmission rate of {fmt_pct(top_chronic['readmission_rate'])}.
- Patients with `{top_prior['segment']}` prior admissions have a readmission rate of {fmt_pct(top_prior['readmission_rate'])}.
- `{top_discharge['segment']}` discharges have a readmission rate of {fmt_pct(top_discharge['readmission_rate'])}.
- The expanded clinical logistic model reached ROC-AUC {model_row['roc_auc']:.2f} on the holdout set.
- The expected ROI scenario estimates {fmt_int(expected['avoided_readmissions'])} avoided readmissions and {fmt_money(expected['net_savings'])} net savings before final implementation cost validation.

## Recommended Executive Priorities

1. Deploy a pre-discharge readmission risk score for risk stratification.
2. Prioritize enhanced discharge review for emergency admissions and skilled nursing discharges.
3. Close follow-up documentation and completion gaps.

## Caveat

These findings use the supplied project data and should be treated as an analytical planning baseline. Care coordination comparisons are observed associations and should not be interpreted as causal effects without additional design or adjustment.
""",
        SECTION_DIRS["02"] / "notes" / "business_problem_findings.md": f"""# Business Problem Findings

## What The Board Needs To Understand

NHN's engagement packet frames rising readmissions as a clinical, operational, and financial problem. Historical readmission rates rose from 14.2% in 2022 to 18.4% in 2025.

## Dataset Evidence

- The cleaned analytical sample has {fmt_int(total_patients)} patients.
- The sample readmission rate is {fmt_pct(readmission_rate)}.
- Emergency admissions show a readmission rate of {fmt_pct(emergency['readmission_rate'])}.
- Unknown follow-up status has a readmission rate of {fmt_pct(unknown_follow['readmission_rate'])}, compared with {fmt_pct(completed_follow['readmission_rate'])} for completed follow-up.
- Total care cost in the cleaned dataset is {fmt_money(total_care_cost)} and nonnegative CMS penalty exposure is {fmt_money(penalty_cost)}.

## Presentation Use

Use this section to explain why NHN needs an integrated clinical, financial, and operational response rather than a single isolated intervention.
""",
        SECTION_DIRS["03"] / "notes" / "data_overview_findings.md": f"""# Data Overview Findings

## Data Sources

The analysis integrates patient readmission, financial impact, and care coordination data using `patient_id`.

## Data Quality Summary

- All three datasets contain {fmt_int(total_patients)} unique patient IDs after cleaning.
- Patient IDs match across all datasets.
- The largest data quality issue is missing follow-up status, affecting {fmt_int(int(df['follow_up_status_missing_flag'].sum()))} records.
- Financial fields include missing and negative values, so nonnegative companion fields and quality flags were created.

## Recommended Slide Message

The data is usable for executive analytics because the join key is complete and unique across datasets, but the Board should understand that missing follow-up documentation and questionable financial values create limitations for precise ROI estimates.
""",
        SECTION_DIRS["04"] / "notes" / "clinical_analysis_findings.md": f"""# Clinical Analysis Findings

## Key Clinical Patterns

- Older patients show higher observed readmission rates. The highest age group is `{top_age['segment']}` at {fmt_pct(top_age['readmission_rate'])}.
- Chronic condition burden is a strong risk marker. The `{top_chronic['segment']}` bucket has a readmission rate of {fmt_pct(top_chronic['readmission_rate'])}.
- Prior admissions are also important. The `{top_prior['segment']}` bucket has a readmission rate of {fmt_pct(top_prior['readmission_rate'])}.
- `{top_discharge['segment']}` discharge disposition has the highest observed readmission rate among discharge categories.

## Interpretation

Clinical risk appears concentrated in older patients, patients with more chronic conditions, patients with repeated prior admissions, and patients discharged to higher-acuity post-acute settings. These groups should be prioritized for risk scoring, discharge planning, and care coordination.
""",
        SECTION_DIRS["05"] / "notes" / "predictive_modeling_findings.md": f"""# Predictive Modeling Findings

## Models Built

- Baseline numeric clinical logistic model.
- Expanded clinical logistic model with numeric and categorical clinical fields.

## Best Current Model

The expanded clinical model performed better on the holdout set:

- Accuracy: {fmt_pct(model_row['accuracy'])}
- Precision: {fmt_pct(model_row['precision'])}
- Recall: {fmt_pct(model_row['recall'])}
- F1 score: {fmt_pct(model_row['f1_score'])}
- ROC-AUC: {model_row['roc_auc']:.2f}

## Leading Predictive Features

The largest standardized coefficients include emergency admission type, skilled nursing discharge, prior admissions, chronic conditions, length of stay, and age.

## Use In Presentation

Position the model as a practical risk stratification tool, not a final production algorithm. NHN should validate thresholds, monitor bias and calibration, and govern operational use before deployment.
""",
        SECTION_DIRS["06"] / "notes" / "care_coordination_findings.md": """# Care Coordination Findings

## Key Message

The care coordination data supports analysis of which services patients received, but raw intervention comparisons should not be treated as causal evidence. High-risk patients may be more likely to receive intensive support.

## Interpretation Guidance

- Use intervention rates and readmission rates to identify where care coordination activity is concentrated.
- Treat higher readmission among some intervention groups as a possible targeting signal, not proof that the intervention caused readmission.
- Prioritize subgroup analysis after risk stratification to determine whether interventions are reaching the patients who need them most.

## Recommended Next Analysis

Compare intervention completion within high-risk deciles and evaluate whether support intensity aligns with predicted readmission risk.
""",
        SECTION_DIRS["07"] / "notes" / "financial_impact_findings.md": f"""# Financial Impact Findings

## Financial Baseline

- Total care cost in the cleaned dataset is {fmt_money(total_care_cost)}.
- Nonnegative CMS penalty exposure is {fmt_money(penalty_cost)}.
- Average net reimbursement gap is {fmt_money(avg_gap)}.

## Interpretation

The financial data supports a Board-level story about the cost burden of readmission-related care and the potential value of reducing avoidable readmissions. Because some financial fields include missing or negative values, final ROI should use nonnegative fields and sensitivity analysis.
""",
        SECTION_DIRS["08"] / "notes" / "dashboard_walkthrough_notes.md": """# Dashboard Walkthrough Notes

## Recommended Pages

1. Executive KPI Summary.
2. Clinical Analytics.
3. Financial Analytics.
4. Care Coordination Analytics.
5. Executive Recommendation Center.

## Walkthrough Flow

Start with the readmission rate and high-risk population. Move into clinical drivers, then financial exposure, then care coordination performance. End with the recommendation center and implementation priorities.
""",
        SECTION_DIRS["08"] / "notes" / "tableau_powerbi_build_guide.md": """# Tableau Dashboard Build Guide

## Requirement

The project requires an executive dashboard using Tableau. This repository now includes dashboard-ready CSV files, but it does not contain a native Tableau workbook (`.twb` or `.twbx`).

## Recommended Data Files

- `sections/08_executive_dashboard_walkthrough/data/dashboard_ready_extract.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv`
- `sections/08_executive_dashboard_walkthrough/data/dashboard_measure_definitions.csv`
- `sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv`

## Recommended Dashboard Pages

### Executive KPI Summary

Use KPI cards for:

- Readmission Rate.
- High-Risk Patients.
- Total Care Cost.
- CMS Penalties.
- Expected ROI.

### Clinical Analytics

Recommended visuals:

- Readmission rate by age group.
- Readmission rate by diagnosis.
- Readmission rate by chronic condition bucket.
- Readmission rate by prior admissions bucket.
- Risk decile readmission rate.

### Financial Analytics

Recommended visuals:

- Total care cost by readmission outcome.
- Cost component totals.
- Net reimbursement gap by discharge disposition.
- ROI scenarios.

### Care Coordination Analytics

Recommended visuals:

- Readmission rate by intervention.
- Intervention completion rates.
- Readmission rate by intervention count.
- Follow-up timing analysis.

### Executive Recommendation Center

Recommended visuals:

- Recommendation priority matrix.
- Implementation roadmap.
- Success metrics table.

## Suggested Calculated Measures

- Readmission Rate: `SUM(readmitted_within_30_days) / COUNT(patient_id)`
- Total Care Cost: `SUM(total_care_cost_nonnegative)`
- CMS Penalties: `SUM(penalty_cost_nonnegative)`
- High-Risk Patients: `COUNT(patient_id)` filtered to `risk_decile` in 8, 9, or 10
- Average Risk Score: `AVG(preliminary_readmission_risk_score)`
- Intervention Completion Rate: average of selected binary intervention fields

## Suggested Filters

- Primary diagnosis.
- Age group.
- Admission type.
- Discharge disposition.
- Insurance type.
- Risk decile.
- Readmission outcome.
- Data quality issue flag.

## Practical Recommendation

Use Tableau for the final submitted dashboard. Use the SVG visuals in each section folder as backup presentation assets or as quick slide visuals if the live dashboard is not ready.
""",
        SECTION_DIRS["09"] / "notes" / "strategic_recommendations.md": """# Strategic Recommendations

## Priority Recommendations

1. Deploy a pre-discharge readmission risk score.
2. Prioritize enhanced discharge review for emergency admissions and skilled nursing discharges.
3. Close follow-up documentation and completion gaps.
4. Target care coordination resources to high-risk chronic disease and prior-admission groups.
5. Launch an executive dashboard that integrates clinical, financial, and operational indicators.

## Board-Level Framing

The recommendations are designed to help NHN move from retrospective reporting to proactive risk identification, targeted intervention, and measurable financial accountability.
""",
        SECTION_DIRS["10"] / "notes" / "roi_analysis_notes.md": """# Financial Impact And ROI Notes

## Scenario Design

The ROI scenarios estimate avoided readmissions using conservative, expected, and optimistic readmission reduction assumptions. Implementation costs are preliminary placeholders and should be replaced with NHN-approved cost estimates before final presentation.

## Current Scenario Assumptions

- Conservative: 5% readmission reduction, $1.0M implementation cost.
- Expected: 10% readmission reduction, $1.75M implementation cost.
- Optimistic: 15% readmission reduction, $2.5M implementation cost.

## Presentation Caveat

Use these scenarios to show financial logic and potential value. Do not present them as final budget commitments until implementation cost assumptions are validated.
""",
        SECTION_DIRS["11"] / "notes" / "implementation_roadmap_notes.md": """# Implementation Roadmap Notes

## Roadmap Logic

The roadmap prioritizes steps that can produce measurable improvement within 12 months while respecting NHN's staffing, technology, regulatory, and operational constraints.

## Implementation Phases

- 0-3 months: define KPIs, pilot risk scoring, fix follow-up documentation.
- 3-6 months: expand targeted care coordination and build the executive dashboard.
- 6-12 months: track ROI, refresh the model, and institutionalize executive review.

## Success Measures

Success should be measured through readmission rate, high-risk intervention completion, CMS penalty exposure, net savings, follow-up documentation quality, and model performance.
""",
    }
    for path, content in note_files.items():
        path.write_text(content.strip() + "\n", encoding="utf-8")

    # Root manifest.
    manifest = {
        "generated_by": "scripts/generate_section_assets.py",
        "primary_dataset": str(MASTER_PATH.relative_to(ROOT)),
        "section_count": len(SECTION_DIRS),
        "total_patients": total_patients,
        "readmission_rate": readmission_rate,
        "expanded_model_roc_auc": float(model_row["roc_auc"]),
        "expected_roi_net_savings": float(expected["net_savings"]),
    }
    (ROOT / "ANALYSIS_ASSETS_SUMMARY.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary_md = f"""# Analysis Assets Summary

Generated section-level data analysis, visualization, and presentation assets for the NHN healthcare consulting project.

## Primary Dataset

- `data/processed/nhn_patient_level_analysis.csv`

## Key Outputs

- Section-level CSV summary tables in each `sections/*/data/` folder.
- PPT-ready SVG visuals in each `sections/*/images/` folder.
- Section finding notes and presentation talking points in each `sections/*/notes/` folder.
- Tableau dashboard-ready files in `sections/08_executive_dashboard_walkthrough/data/`.
- Tableau build guidance in `sections/08_executive_dashboard_walkthrough/notes/tableau_powerbi_build_guide.md`.

## Current Analytical Baseline

- Patients analyzed: {fmt_int(total_patients)}
- Readmission rate: {fmt_pct(readmission_rate)}
- Expanded clinical model ROC-AUC: {model_row['roc_auc']:.2f}
- Expected scenario net savings: {fmt_money(expected['net_savings'])}

## Tableau Dashboard Status

The project requires a Tableau dashboard. A native Tableau workbook was not generated in this repository, but the required dashboard-ready CSVs, KPI definitions, recommended pages, measures, and visual layout are prepared in section 08.

## Important Caveats

- Care coordination intervention comparisons are observed associations and should not be presented as causal effects.
- ROI scenarios use preliminary implementation cost assumptions and should be validated before final presentation.
- The predictive model is a planning baseline and should be validated before production clinical use.
"""
    (ROOT / "ANALYSIS_ASSETS_SUMMARY.md").write_text(summary_md, encoding="utf-8")


if __name__ == "__main__":
    generate_assets()
