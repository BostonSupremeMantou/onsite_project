# Predictive Modeling Findings

## Models Built

- Baseline numeric clinical logistic model.
- Expanded clinical logistic model with numeric and categorical clinical fields.

## Best Current Model

The expanded clinical model performed better on the holdout set:

- Accuracy: 68.3%
- Precision: 66.2%
- Recall: 55.3%
- F1 score: 60.3%
- ROC-AUC: 0.74

## Leading Predictive Features

The largest standardized coefficients include emergency admission type, skilled nursing discharge, prior admissions, chronic conditions, length of stay, and age.

## Use In Presentation

Position the model as a practical risk stratification tool, not a final production algorithm. NHN should validate thresholds, monitor bias and calibration, and govern operational use before deployment.
