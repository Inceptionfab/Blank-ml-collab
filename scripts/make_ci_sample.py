"""Create the 300-row stratified sample that CI uses (CI has no DVC credentials)."""

import pandas as pd

df = pd.read_csv("data/raw/telco_churn.csv", dtype=str, keep_default_na=False)
sample = df.groupby("Churn", group_keys=False).sample(frac=300 / len(df), random_state=42)
sample.to_csv("tests/data/telco_sample.csv", index=False, lineterminator="\n")
print(f"{len(sample)} rows written to tests/data/telco_sample.csv")
