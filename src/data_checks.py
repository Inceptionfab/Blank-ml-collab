"""Schema, value-range and null checks for the raw Telco churn CSV.

Usage: python -m src.data_checks <path-to-csv>   (exit code 1 if any check fails)
"""

import sys

import pandas as pd

EXPECTED_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn",
]  # fmt: skip
YES_NO = {"Yes", "No"}
ADDON = {"Yes", "No", "No internet service"}
ALLOWED_VALUES = {
    "gender": {"Male", "Female"},
    "SeniorCitizen": {0, 1},
    "Partner": YES_NO,
    "Dependents": YES_NO,
    "PhoneService": YES_NO,
    "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": ADDON,
    "OnlineBackup": ADDON,
    "DeviceProtection": ADDON,
    "TechSupport": ADDON,
    "StreamingTV": ADDON,
    "StreamingMovies": ADDON,
    "Contract": {"Month-to-month", "One year", "Two year"},
    "PaperlessBilling": YES_NO,
    "PaymentMethod": {
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    },
    "Churn": YES_NO,
}
RANGES = {"tenure": (0, 72), "MonthlyCharges": (0, 200)}
MAX_BLANK_TOTAL_CHARGES = 0.05  # at most 5% of rows may have a blank TotalCharges


def check(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable problems; empty list means the data is valid."""
    if list(df.columns) != EXPECTED_COLUMNS:
        return [f"columns differ from schema: {list(df.columns)}"]
    errors = []
    nulls = df.isna().sum()
    if nulls.any():
        errors.append(f"null values found: {nulls[nulls > 0].to_dict()}")
    if df["customerID"].duplicated().any():
        errors.append("duplicate customerID values")
    for col, allowed in ALLOWED_VALUES.items():
        unexpected = set(df[col].dropna().unique()) - allowed
        if unexpected:
            errors.append(f"{col}: unexpected values {sorted(map(str, unexpected))}")
    for col, (low, high) in RANGES.items():
        if not df[col].between(low, high).all():
            errors.append(f"{col}: values outside [{low}, {high}]")
    total = pd.to_numeric(df["TotalCharges"], errors="coerce")
    if total.isna().mean() > MAX_BLANK_TOTAL_CHARGES:
        errors.append(f"TotalCharges: {total.isna().mean():.1%} blank/non-numeric")
    if (total.dropna() < 0).any():
        errors.append("TotalCharges: negative values")
    return errors


def main(path: str) -> None:
    df = pd.read_csv(path)
    errors = check(df)
    for e in errors:
        print(f"FAIL: {e}")
    if errors:
        sys.exit(1)
    print(f"OK: {path} passed all data checks ({len(df)} rows, {df.shape[1]} columns)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/raw/telco_churn.csv")
