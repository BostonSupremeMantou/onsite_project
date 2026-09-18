import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");
const RUNTIME_NODE_MODULES = process.env.RUNTIME_NODE_MODULES;
const OUTPUT_DIR = path.join(ROOT, "deliverables", "06_executive_dashboard", "final");
const PREVIEW_DIR = path.join(ROOT, "deliverables", "06_executive_dashboard", "images", "dashboard_package_preview");
const OUTPUT_XLSX = path.join(OUTPUT_DIR, "nhn_dashboard_build_package.xlsx");
const VALIDATION_JSON = path.join(OUTPUT_DIR, "nhn_dashboard_build_package.validation.json");

if (!RUNTIME_NODE_MODULES || !path.isAbsolute(RUNTIME_NODE_MODULES)) {
  throw new Error("Set RUNTIME_NODE_MODULES to the bundled Node module directory.");
}

const requireFromRuntime = createRequire(path.join(RUNTIME_NODE_MODULES, "__runtime__.cjs"));
const artifactToolPath = requireFromRuntime.resolve("@oai/artifact-tool");
const { FileBlob, SpreadsheetFile, Workbook } = await import(pathToFileURL(artifactToolPath).href);

const FONT = "Arial";
const COLORS = {
  ink: "#0B2A33",
  teal: "#0B6F75",
  darkTeal: "#0E5360",
  gold: "#E4B73D",
  green: "#16A34A",
  red: "#DC2626",
  blue: "#0F6B78",
  light: "#F5F8FA",
  border: "#C5D6DE",
  white: "#FFFFFF",
};

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

const n = (value) => Number(value);
const round = (value, digits = 4) => Number(n(value).toFixed(digits));

function title(text) {
  return text.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function sheetSetup(sheet) {
  sheet.showGridLines = false;
  sheet.getRange("A:Z").format.font = { name: FONT, size: 10, color: COLORS.ink };
}

function writeTitle(sheet, titleText, subtitle = "") {
  sheet.getRange("B2").values = [[titleText]];
  sheet.getRange("B2").format.font = { name: FONT, size: 16, bold: true, color: COLORS.ink };
  sheet.getRange("B3:H3").format.borders = {
    bottom: { style: "medium", color: COLORS.gold },
  };
  if (subtitle) {
    sheet.getRange("B4").values = [[subtitle]];
    sheet.getRange("B4").format.font = { name: FONT, size: 10, italic: true, color: "#516773" };
  }
}

function writeTable(sheet, startCell, values, tableName, widths = []) {
  const start = sheet.getRange(startCell);
  start.write(values);
  const rowCount = values.length;
  const colCount = values[0].length;
  const tableRange = start.resize(rowCount, colCount);
  tableRange.format.borders = { preset: "all", style: "thin", color: COLORS.border };
  tableRange.format.verticalAlignment = "center";
  tableRange.format.wrapText = true;
  const header = start.resize(1, colCount);
  header.format.fill = COLORS.darkTeal;
  header.format.font = { name: FONT, size: 10, bold: true, color: COLORS.white };
  header.format.horizontalAlignment = "center";
  const table = sheet.tables.add(tableRange.address, true, tableName);
  table.style = "TableStyleMedium2";
  widths.forEach((width, index) => {
    if (width) start.offset(0, index).resize(rowCount, 1).format.columnWidth = width;
  });
  return tableRange;
}

function formatKpis(sheet) {
  sheet.getRange("B:E").format.columnWidth = 18;
  sheet.getRange("B7:E8").format.fill = COLORS.white;
  sheet.getRange("B7:E8").format.borders = { preset: "all", style: "thin", color: COLORS.border };
  sheet.getRange("B7:E7").format.font = { name: FONT, size: 9, bold: true, color: "#516773" };
  sheet.getRange("B8:E8").format.font = { name: FONT, size: 15, bold: true, color: COLORS.teal };
  sheet.getRange("B7:E8").format.horizontalAlignment = "center";
  sheet.getRange("B7:E8").format.verticalAlignment = "center";
  sheet.getRange("B8").setNumberFormat("0.0%");
  sheet.getRange("C8").setNumberFormat("#,##0");
  sheet.getRange("D8").setNumberFormat('$0.0"M"');
  sheet.getRange("E8").setNumberFormat("0.00x");
}

function styleChart(chart, titleText, valueFormat) {
  chart.title = titleText;
  chart.titleTextStyle.fontSize = 12;
  chart.titleTextStyle.typeface = FONT;
  chart.titleTextStyle.fill = COLORS.ink;
  chart.legend = { position: "bottom", textStyle: { typeface: FONT, fontSize: 10 } };
  chart.xAxis = { axisType: "textAxis", textStyle: { typeface: FONT, fontSize: 10 } };
  chart.yAxis = {
    numberFormatCode: valueFormat,
    numberFormatSourceLinked: false,
    textStyle: { typeface: FONT, fontSize: 10 },
  };
}

function coerceExtractRow(row) {
  const numeric = new Set([
    "readmitted_within_30_days",
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
  ]);
  return Object.entries(row).map(([key, value]) => {
    if (numeric.has(key)) return value === "" ? null : n(value);
    return value;
  });
}

await fs.mkdir(OUTPUT_DIR, { recursive: true });
await fs.mkdir(PREVIEW_DIR, { recursive: true });
try {
  await fs.rename(OUTPUT_XLSX, path.join(OUTPUT_DIR, `previous_${Date.now()}_${path.basename(OUTPUT_XLSX)}`));
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}

const [
  extract,
  kpis,
  measures,
  roi,
  recs,
  riskDeciles,
  clinicalSegments,
  interventions,
  roadmap,
  successMetrics,
] = await Promise.all([
  csv("sections/08_executive_dashboard_walkthrough/data/dashboard_ready_extract.csv"),
  csv("sections/08_executive_dashboard_walkthrough/data/dashboard_kpis.csv"),
  csv("sections/08_executive_dashboard_walkthrough/data/dashboard_measure_definitions.csv"),
  csv("sections/10_financial_impact_and_roi_analysis/data/roi_scenarios.csv"),
  csv("sections/09_strategic_recommendations/data/recommendation_evidence_matrix.csv"),
  csv("sections/05_predictive_modeling_results/data/risk_score_deciles.csv"),
  csv("sections/04_clinical_analysis/data/clinical_readmission_segments.csv"),
  csv("sections/06_care_coordination_analysis/data/intervention_effectiveness_summary.csv"),
  csv("sections/11_implementation_roadmap/data/implementation_roadmap.csv"),
  csv("sections/11_implementation_roadmap/data/success_metrics.csv"),
]);

const workbook = Workbook.create();
const summary = workbook.worksheets.add("Dashboard Summary");
const pages = workbook.worksheets.add("Dashboard Pages");
const defs = workbook.worksheets.add("Measure Definitions");
const build = workbook.worksheets.add("Build Tables");
const validation = workbook.worksheets.add("Validation Checks");
const data = workbook.worksheets.add("Data Extract");
const recommendations = workbook.worksheets.add("Recommendations");

for (const sheet of [summary, pages, defs, build, validation, data, recommendations]) {
  sheetSetup(sheet);
}

// Dashboard Summary
writeTitle(summary, "NHN Executive Dashboard Build Package", "Use this workbook with the CSV extracts to build a Tableau-first presentation dashboard. Power BI definitions are included as backup.");
summary.getRange("B7:E7").values = [["Readmission Rate", "High-Risk Patients", "Total Care Cost", "Expected ROI"]];
summary.getRange("B8:E8").formulas = [[
  "=SUM('Data Extract'!M7:M12006)/COUNTA('Data Extract'!B7:B12006)",
  '=COUNTIFS(\'Data Extract\'!P7:P12006,">=8")',
  "=SUM('Data Extract'!Q7:Q12006)/1000000",
  "='Build Tables'!K8",
]];
formatKpis(summary);
summary.getRange("B11:C21").values = [["Risk Decile", "Readmission Rate"], ...riskDeciles.map((row) => [`D${row.risk_decile}`, round(row.readmission_rate)])];
summary.getRange("B12:B21").format.horizontalAlignment = "center";
summary.getRange("C12:C21").setNumberFormat("0.0%");
summary.getRange("E11:F14").values = [["Scenario", "Net Savings"], ...roi.map((row) => [row.scenario, round(n(row.net_savings) / 1_000_000, 2)])];
summary.getRange("F12:F14").setNumberFormat("$0.0");
writeTable(summary, "H11:J16", [
  ["Priority", "Action", "Timing"],
  ...recs.map((row) => [row.priority, row.short_label, row.timeframe]),
], "SummaryRecommendations", [12, 24, 14]);
const riskChart = summary.charts.add("bar", summary.getRange("B11:C21"));
riskChart.setPosition("B23", "F38");
styleChart(riskChart, "Readmission rate by risk decile", "0%");
const roiChart = summary.charts.add("bar", summary.getRange("E11:F14"));
roiChart.setPosition("H23", "M38");
styleChart(roiChart, "Net savings by ROI scenario ($M)", "$0.0");
summary.freezePanes.freezeRows(6);

// Dashboard Pages
writeTitle(pages, "Dashboard Page Specification", "Build these five native dashboard pages in Tableau first for presentation use. Keep Power BI as a backup implementation path.");
writeTable(pages, "B6:E11", [
  ["Page", "Purpose", "Primary Visuals", "Recommended Filters"],
  ["Executive KPI Summary", "Presentation-level status", "KPI cards, risk decile chart, recommendation table", "Diagnosis, risk decile, readmission outcome"],
  ["Clinical Analytics", "Clinical quality lens", "Age, diagnosis, chronic burden, prior admissions", "Age group, diagnosis, admission type"],
  ["Financial Analytics", "Financial and capacity lens", "Cost components, penalties, ROI scenarios", "Readmission outcome, payer, discharge disposition"],
  ["Care Coordination Analytics", "Targeting and timing lens", "Intervention completion, follow-up timing, high-risk coverage", "Intervention flags, risk decile"],
  ["Executive Recommendation Center", "Full recommendation set", "Priority matrix, roadmap, success metrics", "Recommendation priority and timeframe"],
], "DashboardPages", [24, 24, 40, 34]);

// Measure Definitions
writeTitle(defs, "Calculated Measures And Field Map", "Use these definitions when building Tableau calculated fields. Power BI DAX equivalents can use the same measure logic.");
writeTable(defs, "B6:D12", [
  ["Measure", "Definition", "Recommended Visual"],
  ...measures.map((row) => [row.measure, row.definition, row.recommended_visual]),
], "MeasureDefinitions", [26, 54, 36]);
writeTable(defs, "F6:I19", [
  ["Field", "Data Type", "Role", "Notes"],
  ["patient_id", "Text or Whole Number", "Identifier", "Set as Do not summarize."],
  ["readmitted_within_30_days", "Whole Number", "Outcome", "Use as numerator for readmission rate."],
  ["risk_decile", "Whole Number", "Risk Segment", "Filter and chart by decile 1-10."],
  ["preliminary_readmission_risk_score", "Decimal", "Risk Score", "Average on executive pages."],
  ["total_care_cost_nonnegative", "Currency", "Financial Metric", "Use nonnegative field for dashboard visuals."],
  ["penalty_cost_nonnegative", "Currency", "Financial Metric", "Use nonnegative field for penalty exposure."],
  ["primary_diagnosis", "Text", "Clinical Segment", "Filter and group clinical views."],
  ["discharge_disposition", "Text", "Operational Segment", "Highlight skilled nursing discharges."],
  ["follow_up_status", "Text", "Care Coordination", "Track Unknown follow-up status."],
  ["intervention_count", "Whole Number", "Care Coordination", "Use as operating workload signal."],
  ["has_data_quality_issue_flag", "Whole Number", "Data Quality", "Include filter or QA note."],
  ["readmission_label", "Text", "Outcome Label", "Use for readable legend labels."],
  ["net_reimbursement_gap", "Currency", "Financial Metric", "Use for financial analytics page."],
], "FieldMap", [28, 20, 24, 44]);
writeTable(defs, "F23:I29", [
  ["Design Decision", "Default", "Reason", "Dashboard Impact"],
  ["Primary tool", "Tableau", "Team preference is Tableau first.", "Use Tableau calculated fields and presentation screenshots."],
  ["Audience", "Presentation", "Dashboard supports executive storytelling.", "Prioritize clear pages over daily operations density."],
  ["Risk coverage", "Deciles 8-10 and broader high-risk groups", "Coverage should be expansive rather than minimum viable.", "Use high-risk filters and segment views."],
  ["Model strategy", "Multiple checks or staged models", "One model should not carry all healthcare risk decisions.", "Use model output as one risk input, not the only decision rule."],
  ["Care coordination conclusion", "Redesign targeting and timing", "Selection bias limits causal claims but supports operational redesign.", "Show caveat and action together."],
  ["Data caveats", "Show visibly", "Missing follow-up status and financial data quality are material.", "Include caveat cards and validation page."],
], "DashboardDesignDecisions", [24, 24, 46, 38]);

// Build Tables
writeTitle(build, "Dashboard Build Tables", "Aggregated helper tables for workbook charts and native dashboard build checks.");
writeTable(build, "B6:E16", [
  ["Risk Decile", "Patients", "Average Risk Score", "Readmission Rate"],
  ...riskDeciles.map((row) => [n(row.risk_decile), n(row.patient_count), round(row.average_risk_score), round(row.readmission_rate)]),
], "RiskDecileSummary", [14, 14, 18, 18]);
build.getRange("C7:C16").setNumberFormat("#,##0");
build.getRange("D7:D16").setNumberFormat("0.00");
build.getRange("E7:E16").setNumberFormat("0.0%");
writeTable(build, "G6:K9", [
  ["Scenario", "Readmission Reduction", "Avoided Readmissions", "Net Savings", "ROI"],
  ...roi.map((row) => [row.scenario, round(row.readmission_reduction_rate), n(row.avoided_readmissions), n(row.net_savings), round(row.roi, 2)]),
], "RoiSummary", [18, 20, 20, 18, 12]);
build.getRange("H7:H9").setNumberFormat("0.0%");
build.getRange("I7:I9").setNumberFormat("#,##0");
build.getRange("J7:J9").setNumberFormat("$#,##0");
build.getRange("K7:K9").setNumberFormat("0.00x");
writeTable(build, "B20:E25", [
  ["Segment Type", "Segment", "Patients", "Readmission Rate"],
  ...clinicalSegments
    .filter((row) => ["Admission type", "Discharge disposition", "Chronic condition bucket", "Prior admissions bucket"].includes(row.segment_type))
    .sort((a, b) => n(b.readmission_rate) - n(a.readmission_rate))
    .slice(0, 5)
    .map((row) => [row.segment_type, row.segment, n(row.patient_count), round(row.readmission_rate)]),
], "ClinicalPrioritySegments", [24, 24, 14, 18]);
build.getRange("D21:D25").setNumberFormat("#,##0");
build.getRange("E21:E25").setNumberFormat("0.0%");
writeTable(build, "G20:K26", [
  ["Intervention", "With Intervention", "Without Intervention", "Rate With", "Observed Difference"],
  ...interventions.map((row) => [
    row.intervention,
    n(row.patients_with_intervention),
    n(row.patients_without_intervention),
    round(row.readmission_rate_with_intervention),
    round(row.observed_difference_pp),
  ]),
], "InterventionSummary", [30, 18, 20, 14, 18]);
build.getRange("J21:K26").setNumberFormat("0.0%");
// Validation Checks
writeTitle(validation, "Dashboard Validation Checks", "Use these checks after importing data into Tableau or Power BI.");
writeTable(validation, "B6:F13", [
  ["Check", "Expected", "Workbook Formula", "Actual", "Status"],
  ["Record count", 12000, "COUNT patient_id", null, null],
  ["Readmission rate", 0.432, "SUM readmitted / COUNT patient_id", null, null],
  ["Readmitted patients", 5184, "SUM readmitted", null, null],
  ["High-risk patients", 3600, "COUNT risk_decile >= 8", null, null],
  ["Total care cost", 303126133.99, "SUM total_care_cost_nonnegative", null, null],
  ["CMS penalty exposure", 21247891.9, "SUM penalty_cost_nonnegative", null, null],
  ["Unknown follow-up status", 2587, "COUNT follow_up_status = Unknown", null, null],
], "ValidationChecks", [30, 18, 52, 18, 14]);
validation.getRange("E7:E13").formulas = [
  ["=COUNTA('Data Extract'!B7:B12006)"],
  ["=SUM('Data Extract'!M7:M12006)/COUNTA('Data Extract'!B7:B12006)"],
  ["=SUM('Data Extract'!M7:M12006)"],
  ['=COUNTIFS(\'Data Extract\'!P7:P12006,">=8")'],
  ["=SUM('Data Extract'!Q7:Q12006)"],
  ["=SUM('Data Extract'!S7:S12006)"],
  ['=COUNTIFS(\'Data Extract\'!L7:L12006,"Unknown")'],
];
validation.getRange("F7:F13").formulas = [
  ['=IF(ABS(E7-C7)<0.01,"PASS","REVIEW")'],
  ['=IF(ABS(E8-C8)<0.001,"PASS","REVIEW")'],
  ['=IF(ABS(E9-C9)<0.01,"PASS","REVIEW")'],
  ['=IF(ABS(E10-C10)<0.01,"PASS","REVIEW")'],
  ['=IF(ABS(E11-C11)<1,"PASS","REVIEW")'],
  ['=IF(ABS(E12-C12)<1,"PASS","REVIEW")'],
  ['=IF(ABS(E13-C13)<0.01,"PASS","REVIEW")'],
];
validation.getRange("C7:E13").setNumberFormat("#,##0");
validation.getRange("C8:C8").setNumberFormat("0.0%");
validation.getRange("E8:E8").setNumberFormat("0.0%");
validation.getRange("C11:E12").setNumberFormat("$#,##0");

// Data Extract
writeTitle(data, "Dashboard Ready Extract", "One row per patient. Use this sheet or the source CSV as the Tableau or Power BI import table.");
const headers = Object.keys(extract[0]);
data.getRange("B6").write([headers, ...extract.map(coerceExtractRow)]);
const dataRange = data.getRange("B6").resize(extract.length + 1, headers.length);
dataRange.format.font = { name: FONT, size: 9, color: COLORS.ink };
dataRange.format.borders = { preset: "all", style: "thin", color: "#D7E2E8" };
data.getRange("B6").resize(1, headers.length).format.fill = COLORS.darkTeal;
data.getRange("B6").resize(1, headers.length).format.font = { name: FONT, size: 9, bold: true, color: COLORS.white };
data.tables.add(dataRange.address, true, "DashboardReadyExtract");
data.freezePanes.freezeRows(6);

// Recommendations
writeTitle(recommendations, "Recommendations And Roadmap", "Use this sheet for the Executive Recommendation Center dashboard page.");
writeTable(recommendations, "B6:G11", [
  ["Recommendation", "Short Label", "Evidence", "Impact", "Effort", "Timeframe"],
  ...recs.map((row) => [row.recommendation, row.short_label, row.evidence, n(row.impact_score), n(row.effort_score), row.timeframe]),
], "RecommendationMatrix", [40, 20, 54, 10, 10, 16]);
writeTable(recommendations, "B15:E22", [
  ["Phase", "Initiative", "Owner", "Success Measure"],
  ...roadmap.map((row) => [row.phase, row.initiative, row.owner, row.success_measure]),
], "ImplementationRoadmap", [14, 56, 34, 34]);
writeTable(recommendations, "B26:E32", [
  ["Dimension", "Metric", "Target Direction", "Source"],
  ...successMetrics.map((row) => [row.dimension, row.metric, row.target_direction, row.source]),
], "SuccessMetrics", [16, 36, 22, 28]);

for (const sheet of [summary, pages, defs, build, validation, data, recommendations]) {
  const used = sheet.getUsedRange();
  used.format.autofitColumns();
  used.format.autofitRows();
}

workbook.recalculate();

const errorScan = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
  maxChars: 4000,
});
const validationInspect = await workbook.inspect({
  kind: "table",
  sheetId: "Validation Checks",
  range: "B6:F13",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 6,
  maxChars: 6000,
});

for (const [sheetName, fileName] of [
  ["Dashboard Summary", "dashboard_summary.png"],
  ["Dashboard Pages", "dashboard_pages.png"],
  ["Measure Definitions", "measure_definitions.png"],
  ["Validation Checks", "validation_checks.png"],
]) {
  const preview = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(path.join(PREVIEW_DIR, fileName), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(OUTPUT_XLSX);

const saved = await SpreadsheetFile.importXlsx(await FileBlob.load(OUTPUT_XLSX));
const savedInspect = await saved.inspect({
  kind: "sheet,table,drawing",
  maxChars: 8000,
  tableMaxRows: 3,
  tableMaxCols: 6,
});

await fs.writeFile(VALIDATION_JSON, JSON.stringify({
  output: OUTPUT_XLSX,
  sourceRows: extract.length,
  sheets: ["Dashboard Summary", "Dashboard Pages", "Measure Definitions", "Build Tables", "Validation Checks", "Data Extract", "Recommendations"],
  checks: {
    formulaErrorScan: errorScan.ndjson,
    validationTable: validationInspect.ndjson,
    savedWorkbookInspect: savedInspect.ndjson,
  },
}, null, 2) + "\n");

console.log(JSON.stringify({
  output: OUTPUT_XLSX,
  previews: PREVIEW_DIR,
  validation: VALIDATION_JSON,
}, null, 2));
