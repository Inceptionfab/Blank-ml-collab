# Conflict resolution for #8 (vs #7)

| Candidate | model | n_estimators | max_depth | min_samples_leaf | C | roc_auc | f1 |
|---|---|---|---|---|---|---|---|
| A: dev after #7 | logistic_regression | 100 | 6 | 1 | 1.0 | 0.8359 | 0.6099 |
| B: this PR | random_forest | 300 | 9 | 5 | 1.0 | 0.8359 | 0.5774 |
| C | logistic_regression | 100 | 6 | 1 | 0.3 | 0.8358 | 0.6068 |
| D | logistic_regression | 100 | 6 | 1 | 3.0 | 0.8356 | 0.6110 |

Kept: D (logistic_regression, C=3.0) because its roc_auc (0.8356) is within 0.001 of the top roc_auc (0.8359), and it achieves the highest f1 score (0.6110) among all candidates (rule: highest roc_auc; within 0.001 → higher f1).
