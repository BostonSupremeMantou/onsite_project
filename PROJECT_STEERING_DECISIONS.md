# Project Steering Decisions

## Dashboard And Presentation Direction

- Use Tableau as the primary dashboard tool. Power BI remains a backup implementation path.
- Design the dashboard for presentation and executive review rather than daily operational use.
- Keep the Meds Consulting light executive template consistent across presentation assets.

## Analysis Framing

- Treat readmission as a multi-lens problem. Clinical quality, financial impact, capacity strain, care coordination, data quality, and implementation feasibility all need separate analysis rather than one dominant emphasis.
- Cover all recommendation themes in the final narrative: risk workflow, discharge review, follow-up documentation, targeted care coordination, dashboard reporting, financial impact, and implementation roadmap.
- Keep missing follow-up status and financial data quality caveats visible in the main analysis and presentation. These are material limitations, not appendix-only details.

## Risk Modeling And Intervention Strategy

- Use broad high-risk coverage rather than a minimum viable pilot. Prioritize risk deciles 8-10 and clinically elevated segments such as emergency admissions, skilled nursing discharges, high chronic condition burden, and repeated prior admissions.
- Do not rely on one model as the sole healthcare decision engine. Use a staged workflow that combines model scoring, clinical rules, care team review, and monthly validation.
- Balance recall and precision through model segmentation and process design. The project should avoid both missed high-risk patients and incorrect intervention assignment.

## Care Coordination Interpretation

- State the selection-bias caveat clearly: observed intervention comparisons are associations, not causal estimates.
- Use the stronger operational conclusion: NHN should redesign care coordination targeting and timing so high-risk patients receive the right support earlier and more consistently.

## Financial Assumptions

- Retain the current ROI implementation cost assumptions:
  - Conservative: $1.0M.
  - Expected: $1.75M.
  - Optimistic: $2.5M.
- Continue to present ROI estimates as planning scenarios that need finance validation before budget commitment.

## Narrative Style

- Favor a presentation and explanation style over a pure Board approval pitch.
- Keep recommendations clear and actionable, but show the analysis process and caveats so the project reads as a complete data science consulting engagement.
