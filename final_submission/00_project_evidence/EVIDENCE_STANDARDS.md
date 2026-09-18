# Evidence Standards For Analysis And Reporting

These standards apply to all NHN healthcare consulting reports, dashboard notes, and Board presentation content.

## Evidence Rules

1. Numerical claims must come from the project data, not assumption-based language.
2. Each major finding should cite the exact internal source table used to calculate it.
3. External references support context, regulatory framing, methods, and care-transition rationale. They do not replace project data.
4. Care coordination findings must be described as observed associations unless the analysis uses a causal design.
5. Financial results must preserve the missing-value and negative-value caveats from the cleaning workflow.
6. Predictive model results must include validation caveats and should not be presented as production-ready clinical decision support.
7. ROI assumptions must be explicitly labeled as scenario assumptions.
8. If a number appears in a report, deck, or dashboard, it should be reproducible from `data/processed/nhn_patient_level_analysis.csv` or a section-level CSV.

## Required Report Citation Pattern

Use this pattern in final reports:

- Data source sentence: `Source: [INT-6], calculated in sections/.../data/...csv.`
- External context sentence: `This interpretation aligns with [EXT-1] and [EXT-3].`
- Caveat sentence: `This is descriptive and should not be interpreted causally [EXT-7].`

## Minimum Reference Coverage

The final written report package should include at least six external references:

- CMS HRRP policy or public program data.
- AHRQ HCUP 30-day readmission context.
- Peer-reviewed readmission cost or quality framing.
- Peer-reviewed care transition intervention evidence.
- Peer-reviewed discharge redesign evidence.
- Prediction model reporting or validation guidance.

## Prohibited Phrasing Unless Supported

- Do not write that an intervention "caused" lower readmissions unless a causal analysis was performed.
- Do not write that a model is "ready for clinical production" unless externally validated and operationally approved.
- Do not write that ROI is guaranteed. Use "scenario estimate" or "planning estimate."
- Do not write that missing follow-up status equals no follow-up. It may represent either a true gap or a documentation gap.
