# Blank-ml-collab: Telco Customer Churn

Predict which telecom customers will churn (binary classification), run like a real ML team:
Git + DVC, reviewed pull requests, CI and reproducible, tagged releases.

## Dataset
- Source: [Telco Customer Churn on Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- 7,043 customers × 21 columns; target `Churn` (Yes/No, about 26.5% Yes)
- Stored at `data/raw/telco_churn.csv`, tracked by DVC, never by Git

## Team
| Member | Role |
|---|---|
| Ahsan | Data owner |
| Fahad | Model owner |
| Taha | Platform owner |

## Setup
```bash
uv sync
```

## Get the data
Temporarily: download the CSV from Kaggle into `data/raw/telco_churn.csv`.
(After DVC is set up: `uv run dvc pull`.)

## Run
```bash
uv run python src/train.py
```