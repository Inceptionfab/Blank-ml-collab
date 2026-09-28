import pandas as pd

from src.data_checks import check

SAMPLE = "tests/data/telco_sample.csv"


def test_committed_sample_is_valid():
    assert check(pd.read_csv(SAMPLE)) == []


def test_detects_bad_category():
    df = pd.read_csv(SAMPLE)
    df.loc[0, "Contract"] = "Weekly"
    assert any("Contract" in e for e in check(df))


def test_detects_out_of_range_tenure():
    df = pd.read_csv(SAMPLE)
    df.loc[0, "tenure"] = 500
    assert any("tenure" in e for e in check(df))


def test_detects_missing_column():
    df = pd.read_csv(SAMPLE).drop(columns=["Churn"])
    assert check(df) != []
