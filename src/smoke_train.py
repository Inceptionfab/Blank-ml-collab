"""CI smoke test: prepare -> train -> evaluate on a small sample, in memory.

Writes nothing to data/ or models/, so it never touches DVC-tracked files.
Usage: python -m src.smoke_train --data tests/data/telco_sample.csv
"""

import argparse

import pandas as pd

from src.evaluate import compute_metrics
from src.features import TARGET, clean_telco
from src.prepare import split_data
from src.train import fit
from src.utils import load_params, set_seed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="tests/data/telco_sample.csv")
    args = parser.parse_args()

    params = load_params()
    set_seed(params["seed"])
    df = clean_telco(pd.read_csv(args.data))
    train, test = split_data(df, params["split"]["test_size"], params["seed"])
    model = fit(train, params["train"], params["seed"])
    X, y = test.drop(columns=[TARGET]), test[TARGET]
    metrics = compute_metrics(y, model.predict(X), model.predict_proba(X)[:, 1])
    print(f"smoke-train on {len(df)} rows: {metrics}")
    if not 0.5 < metrics["roc_auc"] <= 1.0:
        raise SystemExit("Smoke model is no better than chance - pipeline is broken")


if __name__ == "__main__":
    main()
