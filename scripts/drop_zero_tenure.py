"""One-off data update: drop customers with tenure 0 (their TotalCharges is blank)."""

import pandas as pd

PATH = "data/raw/telco_churn.csv"
df = pd.read_csv(PATH, dtype=str, keep_default_na=False)  # read as text: values rewritten unchanged
before = len(df)
df = df[df["tenure"] != "0"]
df.to_csv(PATH, index=False, lineterminator="\n")
print(f"rows: {before} -> {len(df)}")
