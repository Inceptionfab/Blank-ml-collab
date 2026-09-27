"""Starter code adapted from Kaggle notebook "CUSTOMER CHURN PREDICTION 📈" by Bharti Prasad: https://www.kaggle.com/code/bhartiprasad17/customer-churn-prediction"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


def main() -> None:
    df = pd.read_csv(Path("data/raw/telco_churn.csv"))

    df = df.drop(["customerID"], axis=1)
    df["TotalCharges"] = pd.to_numeric(df.TotalCharges, errors="coerce")
    df.drop(labels=df[df["tenure"] == 0].index, axis=0, inplace=True)
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].mean())
    df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})

    for col in df.select_dtypes(include=["object", "str"]).columns:
        df[col] = LabelEncoder().fit_transform(df[col])

    X = df.drop(columns=["Churn"])
    y = df["Churn"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )

    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    scaler = StandardScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    clf1 = GradientBoostingClassifier(random_state=42)
    clf2 = LogisticRegression(random_state=42)
    clf3 = AdaBoostClassifier(random_state=42)
    eclf1 = VotingClassifier(estimators=[("gbc", clf1), ("lr", clf2), ("abc", clf3)], voting="soft")
    eclf1.fit(X_train, y_train)
    predictions = eclf1.predict(X_test)
    print("Final Accuracy Score:", accuracy_score(y_test, predictions))


if __name__ == "__main__":
    main()
