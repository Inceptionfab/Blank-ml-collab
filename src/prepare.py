"""Stage 1 - clean the raw CSV and write a fixed, stratified train/test split."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from src.features import TARGET, clean_telco
from src.utils import load_params, set_seed

OUT_DIR = Path("data/processed")


def split_data(df: pd.DataFrame, test_size: float, seed: int):
    """Stratified split on TARGET, fixed by seed, so the test set never changes across runs."""
    return train_test_split(
        df, test_size=test_size, random_state=seed, shuffle=True, stratify=df[TARGET]
    )


def main() -> None:
    params = load_params()
    set_seed(params["seed"])
    df = clean_telco(pd.read_csv(params["data"]["raw"]))
    train, test = split_data(df, params["split"]["test_size"], params["seed"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    train.to_csv(OUT_DIR / "train.csv", index=False)
    test.to_csv(OUT_DIR / "test.csv", index=False)
    print(f"prepare: {len(train)} train rows, {len(test)} test rows")


if __name__ == "__main__":
    main()
