"""Reusable cleaning logic for the Telco Customer Churn dataset."""

import pandas as pd

TARGET = "Churn"
ID_COL = "customerID"
NUMERIC_COLS = ["tenure", "MonthlyCharges", "TotalCharges"]


def clean_telco(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw Telco data without looking at any statistics of the data.

    - TotalCharges is stored as text and is blank for brand-new customers:
      convert to float, blanks become NaN (imputed later, on the train split only).
    - customerID is an identifier, not a feature: drop it.
    - Churn Yes/No becomes 1/0.
    """
    out = df.copy()
    out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")
    out = out.drop(columns=[ID_COL], errors="ignore")
    out[TARGET] = out[TARGET].map({"Yes": 1, "No": 0}).astype(int)
    return out
