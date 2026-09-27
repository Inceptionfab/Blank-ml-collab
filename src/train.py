"""Stage 2 - fit preprocessing + model on the TRAIN split only."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.features import NUMERIC_COLS, TARGET
from src.utils import load_params, set_seed

MODEL_PATH = Path("models/model.joblib")


def build_model(cfg: dict, seed: int):
    if cfg["model"] == "random_forest":
        return RandomForestClassifier(
            n_estimators=cfg["n_estimators"],
            max_depth=cfg["max_depth"],
            min_samples_leaf=cfg["min_samples_leaf"],
            random_state=seed,
            n_jobs=1,  # single-threaded: identical floating-point results on every machine
        )
    if cfg["model"] == "logistic_regression":
        return LogisticRegression(C=cfg["C"], max_iter=2000, random_state=seed)
    raise ValueError(f"Unknown model in params.yaml: {cfg['model']}")


def build_pipeline(X: pd.DataFrame, cfg: dict, seed: int) -> Pipeline:
    numeric = [c for c in NUMERIC_COLS if c in X.columns]
    categorical = [c for c in X.columns if c not in numeric]
    numeric_steps = Pipeline(
        [("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    preprocess = ColumnTransformer(
        [
            ("num", numeric_steps, numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ]
    )
    return Pipeline([("preprocess", preprocess), ("model", build_model(cfg, seed))])


def fit(train_df: pd.DataFrame, cfg: dict, seed: int) -> Pipeline:
    X, y = train_df.drop(columns=[TARGET]), train_df[TARGET]
    pipe = build_pipeline(X, cfg, seed)
    pipe.fit(X, y)  # imputer, scaler and encoder learn from train rows only
    return pipe


def main() -> None:
    params = load_params()
    set_seed(params["seed"])
    model = fit(pd.read_csv("data/processed/train.csv"), params["train"], params["seed"])
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"train: saved {MODEL_PATH}")


if __name__ == "__main__":
    main()
