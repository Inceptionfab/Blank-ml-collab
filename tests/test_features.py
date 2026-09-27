import pandas as pd

from src.features import clean_telco


def _raw():
    return pd.DataFrame(
        {
            "customerID": ["0001-A", "0002-B"],
            "tenure": [1, 0],
            "MonthlyCharges": [29.85, 20.0],
            "TotalCharges": ["29.85", " "],
            "Churn": ["No", "Yes"],
        }
    )


def test_blank_total_charges_becomes_nan():
    out = clean_telco(_raw())
    assert out["TotalCharges"].isna().sum() == 1
    assert out["TotalCharges"].iloc[0] == 29.85


def test_id_dropped_and_target_encoded():
    out = clean_telco(_raw())
    assert "customerID" not in out.columns
    assert out["Churn"].tolist() == [0, 1]


def test_input_not_modified():
    raw = _raw()
    clean_telco(raw)
    assert "customerID" in raw.columns
