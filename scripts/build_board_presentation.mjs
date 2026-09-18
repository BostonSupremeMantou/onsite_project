import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");
const SKILL_DIR = process.env.SKILL_DIR;
const RUNTIME_PYTHON = process.env.RUNTIME_PYTHON;
const TMP_DIR = process.env.TMP_DIR || path.join(ROOT, ".codex-build", "board-presentation");

if (!SKILL_DIR || !path.isAbsolute(SKILL_DIR)) {
  throw new Error("Set SKILL_DIR to the absolute presentations skill path.");
}
if (!RUNTIME_PYTHON || !path.isAbsolute(RUNTIME_PYTHON)) {
  throw new Error("Set RUNTIME_PYTHON to the bundled Python executable.");
}

const runtimeHelpersUrl = pathToFileURL(path.join(SKILL_DIR, "container_tools", "runtime_helpers.mjs")).href;
const utilsUrl = pathToFileURL(path.join(SKILL_DIR, "container_tools", "artifact_tool_utils.mjs")).href;
const { importRuntimeModule } = await import(runtimeHelpersUrl);
const { Presentation, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
const {
  applyPresentationChartFont,
  finalizePresentation,
  resolvePresentationFont,
} = await import(utilsUrl);

const W = 1280;
const H = 720;
const EMU_PER_PX = 9525;
const FINAL_PPTX = path.join(
  ROOT,
  "deliverables",
  "07_executive_board_presentation",
  "final",
  "nhn_readmission_board_presentation.pptx",
);
const PREVIEW_DIR = path.join(
  ROOT,
  "deliverables",
  "07_executive_board_presentation",
  "final",
  "preview",
);
const BACKGROUND_IMAGE = path.join(
  ROOT,
  "deliverables",
  "07_executive_board_presentation",
  "images",
  "healthcare_analytics_background.png",
);

const C = {
  ink: "#0B2A33",
  navy: "#0E5360",
  blue: "#0F6B78",
  sky: "#5FB8C4",
  teal: "#0B6F75",
  green: "#16A34A",
  amber: "#E4B73D",
  red: "#DC2626",
  slate: "#516773",
  lightSlate: "#EAF2F5",
  border: "#C5D6DE",
  page: "#F5F8FA",
  gold: "#E4B73D",
  white: "#FFFFFF",
};
const BRAND = "Meds Consulting LLC";

function parseCsv(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') {
        value += '"';
        i += 1;
      } else if (ch === '"') {
        quoted = false;
      } else {
        value += ch;
      }
      continue;
    }
    if (ch === '"') {
      quoted = true;
    } else if (ch === ",") {
      row.push(value);
      value = "";
    } else if (ch === "\n") {
      row.push(value);
      rows.push(row);
      row = [];
      value = "";
    } else if (ch !== "\r") {
      value += ch;
    }
  }
  if (value.length > 0 || row.length > 0) {
    row.push(value);
    rows.push(row);
  }
  const [headers, ...body] = rows.filter((item) => item.some((cell) => cell.trim() !== ""));
  return body.map((cells) => Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""])));
}

async function csv(relPath) {
  return parseCsv(await fs.readFile(path.join(ROOT, relPath), "utf8"));
}

const num = (value) => Number(value);
const chartValue = (value) => Number(num(value).toFixed(4));
const pct = (value, digits = 1) => `${(num(value) * 100).toFixed(digits)}%`;
const moneyM = (value, digits = 1) => `$${(num(value) / 1_000_000).toFixed(digits)}M`;
const int = (value) => Math.round(num(value)).toLocaleString("en-US");
const pp = (value) => `${(num(value) * 100).toFixed(1)} pp`;

function titleCaseFeature(value) {
  return value
    .replace(/^admission_type_/, "")
    .replace(/^discharge_disposition_/, "")
    .replace(/^insurance_type_/, "")
    .replace(/_imputed$/, "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function addText(slide, text, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: style.family ?? family,
    fontSize: style.fontSize ?? 24,
    bold: style.bold ?? false,
    color: style.color ?? C.ink,
    alignment: style.alignment ?? "left",
    autoFit: style.autoFit ?? "shrinkText",
  };
  return shape;
}

function addShape(slide, position, fill = C.lightSlate, line = { style: "solid", fill: C.border, width: 1 }) {
  return slide.shapes.add({
    geometry: "rect",
    position,
    fill,
    line,
  });
}

function addSlide(title, kicker) {
  const slide = presentation.slides.add();
  slide.background.fill = C.page;
  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 0, width: W, height: 16 },
    fill: C.navy,
    line: { style: "solid", fill: C.navy, width: 0 },
  });
  addText(slide, BRAND, {
    left: 64,
    top: 48,
    width: 360,
    height: 26,
  }, { fontSize: 18, bold: true, color: C.teal });
  addText(slide, kicker?.toUpperCase() ?? "NATIONAL HOSPITAL NETWORK", {
    left: 894,
    top: 50,
    width: 300,
    height: 22,
  }, { fontSize: 11, bold: true, color: C.slate, alignment: "right" });
  addText(slide, title, {
    left: 64,
    top: 88,
    width: 980,
    height: 70,
  }, { fontSize: 34, bold: true, color: C.ink });
  slide.shapes.add({
    geometry: "line",
    position: { left: 64, top: 162, width: 1030, height: 0 },
    fill: "none",
    line: { style: "solid", fill: C.gold, width: 2 },
  });
  addFooter(slide);
  return slide;
}

function addFooter(slide) {
  slide.shapes.add({
    geometry: "line",
    position: { left: 64, top: 660, width: 1152, height: 0 },
    fill: "none",
    line: { style: "solid", fill: "#CFE0E6", width: 1 },
  });
  addText(slide, "Source: Option 1 Healthcare Consulting Packet and project analysis", {
    left: 64,
    top: 674,
    width: 560,
    height: 20,
  }, { fontSize: 10, color: "#66808A" });
}

function addBullets(slide, items, left, top, width, options = {}) {
  const gap = options.gap ?? 48;
  const markerColor = options.markerColor ?? C.blue;
  items.forEach((item, index) => {
    const y = top + index * gap;
    addText(slide, "•", { left, top: y - 1, width: 24, height: 28 }, {
      fontSize: options.markerSize ?? 23,
      bold: true,
      color: markerColor,
    });
    addText(slide, item, { left: left + 28, top: y, width, height: options.height ?? 42 }, {
      fontSize: options.fontSize ?? 18,
      color: options.color ?? C.ink,
      bold: options.bold ?? false,
    });
  });
}

function addMetric(slide, label, value, position, accent = C.blue, note = "") {
  addText(slide, label.toUpperCase(), {
    left: position.left,
    top: position.top,
    width: position.width,
    height: 20,
  }, { fontSize: 11, bold: true, color: C.slate });
  addText(slide, value, {
    left: position.left,
    top: position.top + 28,
    width: position.width,
    height: 44,
  }, { fontSize: 30, bold: true, color: accent });
  if (note) {
    addText(slide, note, {
      left: position.left,
      top: position.top + 72,
      width: position.width,
      height: 32,
    }, { fontSize: 12, color: C.slate });
  }
}

function styleChart(chart) {
  applyPresentationChartFont(chart, { fontFamily: family });
  return chart;
}

function addBarChart(slide, position, categories, values, options = {}) {
  const chart = slide.charts.add("bar", {
    position,
    categories,
    series: [{
      name: options.seriesName ?? "Rate",
      values: values.map(chartValue),
      fill: options.fill ?? C.blue,
    }],
    barOptions: { direction: options.direction ?? "column", grouping: "clustered", gapWidth: 52 },
    hasLegend: false,
    title: options.title ?? "",
    titleTextStyle: { typeface: family, fontSize: 15, fill: C.ink, bold: true },
    xAxis: {
      textStyle: { typeface: family, fontSize: options.axisFontSize ?? 10, fill: C.slate },
      majorGridlines: null,
      line: { style: "solid", fill: "#CBD5E1", width: 1 },
    },
    yAxis: {
      min: options.min,
      max: options.max,
      numberFormatCode: options.numberFormatCode ?? "0%",
      textStyle: { typeface: family, fontSize: 10, fill: C.slate },
      majorGridlines: { style: "solid", fill: "#E2E8F0", width: 1 },
      line: { style: "solid", fill: "#CBD5E1", width: 1 },
    },
    dataLabels: {
      showValue: true,
      position: options.labelPosition ?? "outEnd",
      textStyle: { typeface: family, fontSize: 9, fill: C.ink },
    },
    chartFill: "white",
    plotAreaFill: "white",
    plotAreaLine: { style: "solid", fill: "white", width: 0 },
  });
  return styleChart(chart);
}

function addLineChart(slide, position, categories, values, options = {}) {
  const chart = slide.charts.add("line", {
    position,
    categories,
    series: [{
      name: options.seriesName ?? "Rate",
      values: values.map(chartValue),
      line: { style: "solid", fill: options.fill ?? C.blue, width: 3 },
      marker: { symbol: "circle", size: 6 },
    }],
    lineOptions: { smooth: false },
    hasLegend: false,
    title: options.title ?? "",
    titleTextStyle: { typeface: family, fontSize: 15, fill: C.ink, bold: true },
    xAxis: {
      textStyle: { typeface: family, fontSize: 11, fill: C.slate },
      majorGridlines: null,
      line: { style: "solid", fill: "#CBD5E1", width: 1 },
    },
    yAxis: {
      min: options.min,
      max: options.max,
      numberFormatCode: options.numberFormatCode ?? "0%",
      textStyle: { typeface: family, fontSize: 10, fill: C.slate },
      majorGridlines: { style: "solid", fill: "#E2E8F0", width: 1 },
      line: { style: "solid", fill: "#CBD5E1", width: 1 },
    },
    dataLabels: {
      showValue: true,
      position: "top",
      textStyle: { typeface: family, fontSize: 9, fill: C.ink },
    },
    chartFill: "white",
    plotAreaFill: "white",
    plotAreaLine: { style: "solid", fill: "white", width: 0 },
  });
  return styleChart(chart);
}

function addNativeTable(slide, values, frame, columnTracks) {
  const table = slide.tables.add({
    rows: values.length,
    columns: values[0].length,
    left: frame.left,
    top: frame.top,
    width: frame.width,
    height: frame.height,
    values,
    ...(columnTracks ? { columnTracks } : {}),
  });
  table.styleOptions = { headerRow: true, bandedRows: true };
  table.borders.assign({ style: "solid", fill: "#CBD5E1", width: 1 });
  table.cells.block({ row: 0, column: 0, rowCount: 1, columnCount: values[0].length }).assign({
    fill: C.navy,
    textStyle: { typeface: family, fontSize: 11, bold: true, color: C.white },
  });
  if (values.length > 1) {
    table.cells.block({ row: 1, column: 0, rowCount: values.length - 1, columnCount: values[0].length }).assign({
      textStyle: { typeface: family, fontSize: 10, color: C.ink },
    });
  }
  return table;
}

function setNotes(slide, notes) {
  slide.speakerNotes.textFrame.setText(notes);
}

await fs.mkdir(TMP_DIR, { recursive: true });
await fs.mkdir(PREVIEW_DIR, { recursive: true });
await fs.mkdir(path.dirname(FINAL_PPTX), { recursive: true });
try {
  await fs.rename(FINAL_PPTX, path.join(TMP_DIR, `previous_${Date.now()}_${path.basename(FINAL_PPTX)}`));
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}

const family = resolvePresentationFont();
const [
  kpis,
  businessMetrics,
  segments,
  quality,
  modelMetrics,
  featureImportance,
  riskDeciles,
  interventions,
  financialBaseline,
  costComponents,
  roi,
  recommendations,
  roadmap,
  successMetrics,
] = await Promise.all([
  csv("sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv"),
  csv("sections/02_business_problem/data/business_problem_metrics.csv"),
  csv("sections/04_clinical_analysis/data/clinical_readmission_segments.csv"),
  csv("sections/03_data_overview/data/data_quality_summary.csv"),
  csv("sections/05_predictive_modeling_results/data/model_metrics.csv"),
  csv("sections/05_predictive_modeling_results/data/model_feature_importance.csv"),
  csv("sections/05_predictive_modeling_results/data/risk_score_deciles.csv"),
  csv("sections/06_care_coordination_analysis/data/intervention_effectiveness_summary.csv"),
  csv("sections/07_financial_impact_analysis/data/financial_baseline_summary.csv"),
  csv("sections/07_financial_impact_analysis/data/financial_cost_components.csv"),
  csv("sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv"),
  csv("sections/09_strategic_recommendations/data/recommendation_evidence_matrix.csv"),
  csv("sections/11_implementation_roadmap/data/implementation_roadmap.csv"),
  csv("sections/11_implementation_roadmap/data/success_metrics.csv"),
]);

const kpiMap = new Map(kpis.map((row) => [row.metric, row]));
const expandedModel = modelMetrics.find((row) => row.model.startsWith("Expanded"));
const baselineModel = modelMetrics.find((row) => row.model.startsWith("Baseline"));
const expectedRoi = roi.find((row) => row.scenario === "Expected");
const clinicalTop = segments
  .filter((row) => ["Admission type", "Discharge disposition", "Chronic condition bucket", "Prior admissions bucket"].includes(row.segment_type))
  .sort((a, b) => num(b.readmission_rate) - num(a.readmission_rate))
  .slice(0, 6);
const presentation = Presentation.create({
  slideSize: { width: W, height: H },
});

// 1. Title
{
  const slide = presentation.slides.add();
  slide.background.fill = C.page;
  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 0, width: W, height: 16 },
    fill: C.navy,
    line: { style: "solid", fill: C.navy, width: 0 },
  });
  addText(slide, BRAND, {
    left: 64,
    top: 50,
    width: 360,
    height: 28,
  }, { fontSize: 18, bold: true, color: C.teal });
  addText(slide, "National Hospital Network readmission challenge", {
    left: 64,
    top: 96,
    width: 840,
    height: 104,
  }, { fontSize: 42, bold: true, color: C.ink });
  slide.shapes.add({
    geometry: "line",
    position: { left: 64, top: 198, width: 1030, height: 0 },
    fill: "none",
    line: { style: "solid", fill: C.gold, width: 2 },
  });
  addText(slide, "Executive Board presentation", {
    left: 64,
    top: 240,
    width: 500,
    height: 36,
  }, { fontSize: 28, bold: true, color: C.ink });
  addText(slide, "Clinical analytics, financial impact, care coordination, and 12-month implementation plan.", {
    left: 64,
    top: 294,
    width: 520,
    height: 70,
  }, { fontSize: 20, color: "#29444F" });
  slide.shapes.add({
    geometry: "line",
    position: { left: 636, top: 232, width: 0, height: 380 },
    fill: "none",
    line: { style: "solid", fill: C.border, width: 1 },
  });
  addText(slide, "Current decision context", {
    left: 684,
    top: 240,
    width: 390,
    height: 36,
  }, { fontSize: 28, bold: true, color: C.ink });
  addText(slide, "NHN has rising 30-day readmissions, elevated analytical-sample risk, and a material financial opportunity if intervention targeting improves.", {
    left: 684,
    top: 294,
    width: 420,
    height: 84,
  }, { fontSize: 20, color: "#29444F" });
  slide.shapes.add({
    geometry: "line",
    position: { left: 64, top: 394, width: 470, height: 0 },
    fill: "none",
    line: { style: "solid", fill: C.border, width: 1 },
  });
  addMetric(slide, "Analytical patients", "12,000", { left: 64, top: 428, width: 210, height: 110 }, C.teal, "Matched across 3 datasets");
  addMetric(slide, "Readmission rate", "43.2%", { left: 320, top: 428, width: 210, height: 110 }, C.amber, "Current analytical sample");
  addMetric(slide, "Expected net savings", "$8.8M", { left: 684, top: 428, width: 210, height: 110 }, C.green, "Before cost validation");
  addMetric(slide, "Model ROC-AUC", "0.74", { left: 940, top: 428, width: 210, height: 110 }, C.blue, "Expanded clinical model");
  addFooter(slide);
  setNotes(slide, "Open with the core ask: reduce avoidable readmissions while protecting quality, capacity, and financial performance.");
}

// 2. Executive summary
{
  const slide = addSlide("Executive Summary", "Decision context");
  addMetric(slide, "Readmission Rate", kpiMap.get("Analytical dataset readmission rate").display_value, { left: 64, top: 188, width: 250, height: 126 }, C.amber, "5,184 readmitted patients");
  addMetric(slide, "Model ROC-AUC", pct(expandedModel.roc_auc), { left: 340, top: 188, width: 250, height: 126 }, C.blue, "Expanded clinical model");
  addMetric(slide, "Penalty Exposure", kpiMap.get("CMS penalty exposure in cleaned dataset").display_value, { left: 616, top: 188, width: 250, height: 126 }, C.red, "Nonnegative exposure");
  addMetric(slide, "Expected ROI", `${num(expectedRoi.roi).toFixed(2)}x`, { left: 892, top: 188, width: 250, height: 126 }, C.green, `${moneyM(expectedRoi.net_savings)} net savings`);
  addBullets(slide, [
    "Use separate clinical quality, financial, capacity, care coordination, and data quality lenses for the readmission problem.",
    "Cover deciles 8-10 and other high-risk clinical groups rather than narrowing the pilot to one minimum segment.",
    "Build the executive dashboard in Tableau first using the prepared extract, KPI definitions, and validation checks.",
  ], 82, 372, 1000, { gap: 58, fontSize: 20, markerColor: C.teal });
  setNotes(slide, "The summary combines clinical, financial, and operating findings into the Board-level decision path.");
}

// 3. Business problem
{
  const slide = addSlide("Readmissions Are Moving In The Wrong Direction", "Business problem");
  addLineChart(
    slide,
    { left: 72, top: 172, width: 560, height: 350 },
    ["2022", "2023", "2024", "2025"],
    [0.142, 0.158, 0.169, 0.184],
    { title: "Historical NHN readmission trend", min: 0.1, max: 0.2, fill: C.red },
  );
  addBullets(slide, [
    "Readmissions increased from 14.2% in 2022 to 18.4% in 2025.",
    "Leadership estimates more than $42M in annual readmission-related cost.",
    "The challenge affects patient outcomes, inpatient capacity, staff workload, and CMS penalty exposure.",
  ], 704, 196, 450, { gap: 86, fontSize: 20, markerColor: C.red });
  setNotes(slide, "Use this slide to frame why the work matters before moving into the integrated data and analysis.");
}

// 4. Data overview
{
  const slide = addSlide("Integrated Data Foundation", "Data overview");
  addNativeTable(slide, [
    ["Dataset", "Records", "Role"],
    ["Patient readmissions", "12,000", "Clinical profile and target"],
    ["Financial impact", "12,000", "Cost, penalty, and reimbursement fields"],
    ["Care coordination", "12,000", "Intervention and follow-up activity"],
  ], { left: 72, top: 168, width: 560, height: 260 }, [
    { mode: "fr", value: 1.4 },
    { mode: "fr", value: 0.8 },
    { mode: "fr", value: 2.2 },
  ]);
  addNativeTable(slide, [
    ["Data quality issue", "Records", "Rate"],
    ...quality.slice(0, 5).map((row) => [
      row.issue,
      int(row.affected_rows),
      pct(row.affected_rate),
    ]),
  ], { left: 678, top: 168, width: 520, height: 320 }, [
    { mode: "fr", value: 1.5 },
    { mode: "fr", value: 0.7 },
    { mode: "fr", value: 1.8 },
  ]);
  addText(slide, "Join key: patient_id. All source files match cleanly across the 12,000-patient analytical sample.", {
    left: 90,
    top: 548,
    width: 1030,
    height: 42,
  }, { fontSize: 20, bold: true, color: C.teal, alignment: "center" });
  setNotes(slide, "Call out that the data joins cleanly, while follow-up documentation and financial field quality remain limitations.");
}

// 5. Clinical analysis
{
  const slide = addSlide("High-Risk Segments Are Clinically Intuitive", "Clinical analysis");
  addBarChart(
    slide,
    { left: 72, top: 166, width: 650, height: 390 },
    clinicalTop.map((row) => row.segment),
    clinicalTop.map((row) => num(row.readmission_rate)),
    { title: "Readmission rate by selected high-risk segment", fill: C.teal, max: 0.75, axisFontSize: 9 },
  );
  addBullets(slide, [
    "Emergency admissions have a 50.9% observed readmission rate.",
    "Skilled nursing discharge and higher chronic-condition burden signal elevated risk.",
    "Prior admissions remain one of the strongest clinical predictors.",
  ], 790, 192, 360, { gap: 90, fontSize: 20, markerColor: C.teal });
  setNotes(slide, "Tie the high-risk segments back to operational decisions such as discharge review and care coordination assignment.");
}

// 6. Predictive modeling results
{
  const slide = addSlide("Use A Staged Modeling Approach", "Predictive modeling");
  const metrics = ["accuracy", "precision", "recall", "f1_score", "roc_auc"];
  const metricLabels = ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"];
  const chart = slide.charts.add("bar", {
    position: { left: 70, top: 166, width: 600, height: 350 },
    categories: metricLabels,
    series: [
      { name: "Baseline", values: metrics.map((metric) => chartValue(baselineModel[metric])), fill: "#94A3B8" },
      { name: "Expanded", values: metrics.map((metric) => chartValue(expandedModel[metric])), fill: C.blue },
    ],
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 72 },
    hasLegend: true,
    legend: { position: "bottom", textStyle: { typeface: family, fontSize: 10, fill: C.slate } },
    title: "Model performance comparison",
    titleTextStyle: { typeface: family, fontSize: 15, fill: C.ink, bold: true },
    xAxis: { textStyle: { typeface: family, fontSize: 10, fill: C.slate }, majorGridlines: null },
    yAxis: {
      min: 0,
      max: 0.85,
      numberFormatCode: "0%",
      textStyle: { typeface: family, fontSize: 10, fill: C.slate },
      majorGridlines: { style: "solid", fill: "#E2E8F0", width: 1 },
    },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { typeface: family, fontSize: 9, fill: C.ink } },
    chartFill: "white",
    plotAreaFill: "white",
  });
  styleChart(chart);
  const topFeatures = featureImportance.slice(0, 6).map((row) => [
    titleCaseFeature(row.feature),
    num(row.coefficient).toFixed(2),
  ]);
  addNativeTable(slide, [
    ["Top model driver", "Coefficient"],
    ...topFeatures,
  ], { left: 728, top: 166, width: 430, height: 350 }, [
    { mode: "fr", value: 1.8 },
    { mode: "fr", value: 0.9 },
  ]);
  addText(slide, "Use model output as one layer in a broader risk workflow, not as the only decision rule.", {
    left: 734,
    top: 548,
    width: 420,
    height: 44,
  }, { fontSize: 17, bold: true, color: C.teal, alignment: "center" });
  setNotes(slide, "The model is not positioned as a single decision engine. Use staged risk scoring, clinical rules, and operational review to balance recall and precision.");
}

// 7. Risk stratification
{
  const slide = addSlide("Risk Deciles Separate Readmission Rates", "Operational use");
  addBarChart(
    slide,
    { left: 72, top: 166, width: 760, height: 390 },
    riskDeciles.map((row) => `D${row.risk_decile}`),
    riskDeciles.map((row) => num(row.readmission_rate)),
    { title: "Observed readmission rate by model risk decile", fill: C.blue, max: 0.9 },
  );
  addShape(slide, { left: 880, top: 190, width: 276, height: 242 }, "#EFF6FF", { style: "solid", fill: "#BFDBFE", width: 1 });
  addText(slide, "Recommended operating rule", { left: 904, top: 214, width: 230, height: 30 }, {
    fontSize: 18,
    bold: true,
    color: C.navy,
  });
  addText(slide, "Start with deciles 8-10 plus clinical rules for repeat admissions, chronic burden, emergency admission, and skilled nursing discharge.", {
    left: 904,
    top: 262,
    width: 230,
    height: 118,
  }, { fontSize: 19, color: C.ink });
  addText(slide, "Top decile rate: 82.3%", { left: 904, top: 414, width: 230, height: 34 }, {
    fontSize: 21,
    bold: true,
    color: C.blue,
  });
  setNotes(slide, "Risk deciles turn the model into an operational queue, but coverage should be broad and supported by clinical rules rather than a narrow decile-10-only pilot.");
}

// 8. Care coordination
{
  const slide = addSlide("Redesign Targeting And Timing", "Care coordination");
  const sortedInterventions = interventions
    .slice()
    .sort((a, b) => num(b.observed_difference_pp) - num(a.observed_difference_pp));
  const interventionLabel = (name) => ({
    "Medication review completed": "Medication review",
    "Any post-discharge call": "Post-discharge call",
    "Care coordinator assigned": "Coordinator",
    "Follow-up completed": "Follow-up",
    "Transportation assistance": "Transport",
    "Home health referral": "Home health",
  })[name] ?? name;
  addBarChart(
    slide,
    { left: 72, top: 166, width: 650, height: 360 },
    sortedInterventions.map((row) => interventionLabel(row.intervention)),
    sortedInterventions.map((row) => num(row.observed_difference_pp)),
    { title: "Observed readmission difference with intervention", fill: C.amber, numberFormatCode: "0.0%", max: 0.04, min: -0.01, axisFontSize: 8 },
  );
  addBullets(slide, [
    "Observed differences are associations, not causal estimates.",
    "Selection bias strengthens the case for better targeting and earlier intervention timing.",
    "Priority should be broad high-risk coverage, completion tracking, and redesign of intervention assignment rules.",
  ], 790, 180, 360, { gap: 94, fontSize: 19, markerColor: C.amber });
  setNotes(slide, "Keep the causal caveat visible, then make the stronger operational point: NHN should redesign targeting, timing, and intervention completion for high-risk patients.");
}

// 9. Financial impact
{
  const slide = addSlide("Financial Exposure Is Material", "Financial impact");
  addBarChart(
    slide,
    { left: 72, top: 166, width: 620, height: 370 },
    costComponents.map((row) => row.component.replace(" cost", "")),
    costComponents.map((row) => num(row.amount) / 1_000_000),
    { title: "Cost components in cleaned dataset", fill: C.red, numberFormatCode: "$0M", max: 240 },
  );
  const baselineRows = financialBaseline.map((row) => [
    row.readmission_label,
    int(row.patient_count),
    moneyM(row.total_care_cost),
    moneyM(row.total_penalty_cost),
  ]);
  addNativeTable(slide, [
    ["Group", "Patients", "Total cost", "Penalty cost"],
    ...baselineRows,
  ], { left: 748, top: 190, width: 420, height: 190 }, [
    { mode: "fr", value: 1.3 },
    { mode: "fr", value: 0.9 },
    { mode: "fr", value: 1.0 },
    { mode: "fr", value: 1.0 },
  ]);
  addText(slide, "Financial estimates should use nonnegative fields and scenario sensitivity because the raw file contains missing and negative financial values.", {
    left: 750,
    top: 426,
    width: 410,
    height: 86,
  }, { fontSize: 19, color: C.ink });
  setNotes(slide, "The analysis gives a strong directional financial case while preserving data quality caveats.");
}

// 10. Dashboard walkthrough
{
  const slide = addSlide("Dashboard Build Plan", "Executive dashboard");
  addNativeTable(slide, [
    ["Page", "Purpose", "Primary visuals"],
    ["Executive KPI Summary", "Presentation-level status", "KPI cards, risk decile chart, recommendation table"],
    ["Clinical Analytics", "Risk drivers", "Age, diagnosis, chronic burden, prior admissions"],
    ["Financial Analytics", "Cost exposure", "Cost components, penalty exposure, ROI scenarios"],
    ["Care Coordination", "Operational execution", "Intervention completion and follow-up timing"],
    ["Recommendation Center", "Management actions", "Priority matrix, roadmap, success metrics"],
  ], { left: 70, top: 180, width: 800, height: 342 }, [
    { mode: "fr", value: 1.2 },
    { mode: "fr", value: 1.4 },
    { mode: "fr", value: 2.1 },
  ]);
  addMetric(slide, "Required tool", "Tableau first", { left: 920, top: 192, width: 250, height: 128 }, C.blue, "Power BI backup path");
  addMetric(slide, "Dashboard rows", "12,000", { left: 920, top: 346, width: 250, height: 128 }, C.teal, "One row per patient");
  addText(slide, "Use dashboard_ready_extract.csv plus the Tableau build package and validation checks in deliverable 06.", {
    left: 920,
    top: 510,
    width: 250,
    height: 74,
  }, { fontSize: 17, color: C.ink });
  setNotes(slide, "This is the handoff from analytics to a native Tableau or Power BI dashboard build.");
}

// 11. Strategic recommendations
{
  const slide = addSlide("Recommendations Link Directly To Evidence", "Strategy");
  addNativeTable(slide, [
    ["Recommendation", "Evidence", "Timing"],
    ...recommendations.slice(0, 5).map((row) => [row.short_label, row.evidence, row.timeframe]),
  ], { left: 72, top: 180, width: 1020, height: 368 }, [
    { mode: "fr", value: 1.0 },
    { mode: "fr", value: 2.9 },
    { mode: "fr", value: 0.8 },
  ]);
  addText(slide, "Highest priority: risk score, discharge review, follow-up documentation, targeted care, and executive reporting.", {
    left: 110,
    top: 574,
    width: 960,
    height: 42,
  }, { fontSize: 22, bold: true, color: C.teal, alignment: "center" });
  setNotes(slide, "The table is structured for Board discussion. It keeps recommendations traceable to evidence and timing.");
}

// 12. ROI scenarios
{
  const slide = addSlide("Expected Scenario Produces $8.8M Net Savings", "ROI");
  addBarChart(
    slide,
    { left: 72, top: 166, width: 560, height: 350 },
    roi.map((row) => row.scenario),
    roi.map((row) => num(row.net_savings) / 1_000_000),
    { title: "Estimated net savings by scenario", fill: C.green, numberFormatCode: "$0.0M", max: 15 },
  );
  addNativeTable(slide, [
    ["Scenario", "Reduction", "Avoided readmissions", "Net savings", "ROI"],
    ...roi.map((row) => [
      row.scenario,
      pct(row.readmission_reduction_rate),
      int(row.avoided_readmissions),
      moneyM(row.net_savings),
      `${num(row.roi).toFixed(2)}x`,
    ]),
  ], { left: 692, top: 188, width: 500, height: 238 }, [
    { mode: "fr", value: 1.0 },
    { mode: "fr", value: 0.9 },
    { mode: "fr", value: 1.2 },
    { mode: "fr", value: 1.0 },
    { mode: "fr", value: 0.7 },
  ]);
  addText(slide, "Assumptions need final validation with Finance before they are treated as budget commitments.", {
    left: 704,
    top: 476,
    width: 456,
    height: 70,
  }, { fontSize: 20, color: C.ink });
  setNotes(slide, "The ROI slide should be presented as a planning scenario, not a guaranteed budget result.");
}

// 13. Implementation roadmap
{
  const slide = addSlide("12-Month Implementation Roadmap", "Implementation");
  addNativeTable(slide, [
    ["Phase", "Initiative", "Owner"],
    ...roadmap.map((row) => [row.phase, row.initiative, row.owner]),
  ], { left: 72, top: 180, width: 1040, height: 410 }, [
    { mode: "fr", value: 0.7 },
    { mode: "fr", value: 2.7 },
    { mode: "fr", value: 1.6 },
  ]);
  setNotes(slide, "Walk through the roadmap as a staged implementation, starting with governance, pilot design, and data quality.");
}

// 14. Success measures
{
  const slide = addSlide("Success Measures And Governance", "Measurement");
  addNativeTable(slide, [
    ["Dimension", "Metric", "Target direction", "Source"],
    ...successMetrics.map((row) => [row.dimension, row.metric, row.target_direction, row.source]),
  ], { left: 72, top: 180, width: 740, height: 340 }, [
    { mode: "fr", value: 0.9 },
    { mode: "fr", value: 1.7 },
    { mode: "fr", value: 1.1 },
    { mode: "fr", value: 1.2 },
  ]);
  addBullets(slide, [
    "Monthly executive review of readmission rate, penalties, net savings, and intervention completion.",
    "Quarterly model refresh review with clinical governance.",
    "Dashboard data quality checks before every executive reporting cycle.",
  ], 880, 182, 300, { gap: 96, fontSize: 18, markerColor: C.blue });
  setNotes(slide, "Define how the organization will know whether the program is working after launch.");
}

// 15. Board decision points
{
  const slide = addSlide("Board Decision Points", "Close");
  addBullets(slide, [
    "Approve a broad high-risk readmission reduction pilot covering deciles 8-10 and clinical-rule segments.",
    "Approve staged model governance so no single model carries the full healthcare decision risk.",
    "Approve Tableau dashboard development for presentation and executive review.",
    "Approve follow-up documentation workflow improvements.",
    "Validate implementation cost assumptions for ROI tracking.",
  ], 116, 174, 900, { gap: 70, fontSize: 22, markerColor: C.green });
  addShape(slide, { left: 116, top: 558, width: 980, height: 64 }, "#ECFDF5", { style: "solid", fill: "#BBF7D0", width: 1 });
  addText(slide, "Recommended decision: fund the 0-3 month pilot and dashboard build, then review ROI monthly.", {
    left: 146,
    top: 574,
    width: 920,
    height: 34,
  }, { fontSize: 22, bold: true, color: "#166534", alignment: "center" });
  setNotes(slide, "Close by asking for concrete approvals tied to a controlled pilot and transparent measurement cadence.");
}

const requirements = {
  explicitTotalSlideCount: 15,
  requiredNativeChartOwnerSlides: [3, 5, 6, 7, 8, 9, 12],
  requiredNativeTableOwnerSlides: [4, 6, 9, 10, 11, 12, 13, 14],
  materializeLiteralChartWorkbooks: true,
  nativeChartTargetApplication: "portable",
};
const fontPolicy = { basis: "design", families: [family] };
const expectedSlideSizeEmu = `${W * EMU_PER_PX},${H * EMU_PER_PX}`;

const candidatePath = path.join(TMP_DIR, "candidate_nhn_board_presentation.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);

const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(path.join(TMP_DIR, "candidate_montage.webp"), Buffer.from(await montage.arrayBuffer()));

const result = await finalizePresentation({
  ...requirements,
  workspaceDir: ROOT,
  candidatePath,
  finalPath: FINAL_PPTX,
  pythonExecutable: RUNTIME_PYTHON,
  integrityValidatorPath: path.join(SKILL_DIR, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: [
    "--expected-aspect", "16:9",
    "--expected-slide-count", "15",
    "--expected-slide-size-emu", expectedSlideSizeEmu,
    "--validate-heading-fit",
    ...requirements.requiredNativeTableOwnerSlides.flatMap((number) => ["--require-native-table-slide", String(number)]),
  ],
  fontPolicy,
  requiredNativeTableOwnerSlides: requirements.requiredNativeTableOwnerSlides,
  requiredNativeChartOwnerSlides: requirements.requiredNativeChartOwnerSlides,
  nativeChartTargetApplication: requirements.nativeChartTargetApplication,
  materializeLiteralChartWorkbooks: requirements.materializeLiteralChartWorkbooks,
  verifyArtifactToolImport: true,
  receiptPath: path.join(ROOT, ".codex-finalizer", `nhn_readmission_board_presentation.${Date.now()}.validation.json`),
});

await fs.writeFile(
  path.join(TMP_DIR, "build_result.json"),
  JSON.stringify({
    finalPath: result.finalPath,
    receiptPath: result.receiptPath,
    slideCount: requirements.explicitTotalSlideCount,
    fontFamily: family,
  }, null, 2) + "\n",
);

console.log(JSON.stringify({
  finalPath: result.finalPath,
  receiptPath: result.receiptPath,
  candidatePath,
  previewDir: PREVIEW_DIR,
}, null, 2));
