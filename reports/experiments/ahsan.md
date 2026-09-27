| Experiment                  | roc_auc   | f1     | precision   | recall   | accuracy   | train.model         | train.C   |
|-----------------------------|-----------|--------|-------------|----------|------------|---------------------|-----------|
| workspace                   | 0.8341    | 0.5386 | 0.6552      | 0.4572   | 0.7918     | random_forest       | 1         |
| exp/ahsan-logreg            | 0.8341    | 0.5386 | 0.6552      | 0.4572   | 0.7918     | random_forest       | 1         |
| ├── 6897f74 [ahsan-lr-c10]  | 0.8353    | 0.6054 | 0.6426      | 0.5722   | 0.8017     | logistic_regression | 10        |
| ├── 1bf50fe [ahsan-lr-c1]   | 0.8359    | 0.6099 | 0.6495      | 0.5749   | 0.8045     | logistic_regression | 1         |
| └── 9252dfe [ahsan-lr-c0.1] | 0.8352    | 0.6074 | 0.6543      | 0.5668   | 0.8053     | logistic_regression | 0.1       |
