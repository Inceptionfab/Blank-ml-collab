"""Stage 3 - score the held-out test split and write metrics.json."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score

from src.features import TARGET
from src.utils import git_info


def compute_metrics(y_true, y_pred, y_proba) -> dict:
    """Score predictions and round every metric to 4 decimals, as the team reports them."""
    scores = {
        "roc_auc": roc_auc_score(y_true, y_proba),
        "f1": f1_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "accuracy": accuracy_score(y_true, y_pred),
    }
    return {k: round(float(v), 4) for k, v in scores.items()}


def main() -> None:
    test = pd.read_csv("data/processed/test.csv")
    model = joblib.load("models/model.joblib")
    X, y = test.drop(columns=[TARGET]), test[TARGET]
    metrics = compute_metrics(y, model.predict(X), model.predict_proba(X)[:, 1])
    metrics.update(git_info())
    Path("metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"evaluate: {metrics}")


if __name__ == "__main__":
    main()
