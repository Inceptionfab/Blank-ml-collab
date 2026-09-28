"""One-off data update: drop customers with tenure 0 (their TotalCharges is blank).

Why tenure == 0 is the cut rule: these customers joined in the current billing month, so
they have no bill yet (TotalCharges is blank) and have had no chance to churn. They are
exactly the rows with a blank TotalCharges found in the EDA (notebooks/01-eda.ipynb).

Usage: python scripts/drop_zero_tenure.py   (safe to re-run: a second run drops nothing)
"""

import pandas as pd

PATH = "data/raw/telco_churn.csv"


def drop_zero_tenure(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split raw text data into (kept, dropped) rows on the tenure == 0 rule."""
    is_zero = df["tenure"] == "0"
    return df[~is_zero], df[is_zero]


def main() -> None:
    """Rewrite the raw CSV without zero-tenure rows and report what was dropped."""
    df = pd.read_csv(PATH, dtype=str, keep_default_na=False)  # text: values rewritten unchanged
    kept, dropped = drop_zero_tenure(df)
    kept.to_csv(PATH, index=False, lineterminator="\n")
    print(f"rows: {len(df)} -> {len(kept)} ({len(dropped)} dropped)")
    print(f"Churn of dropped rows: {dropped['Churn'].value_counts().to_dict()}")
    blank = (dropped["TotalCharges"].str.strip() == "").sum()
    print(f"dropped rows with blank TotalCharges: {blank} of {len(dropped)}")


if __name__ == "__main__":
    main()
