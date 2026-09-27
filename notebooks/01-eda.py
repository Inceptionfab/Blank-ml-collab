# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
# ---

# %% [markdown]
# # Exploratory data analysis: Telco Customer Churn
#
# All cleaning goes through `clean_telco` in `src/features.py`; no cleaning code lives here.

# %%
import sys
from pathlib import Path

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.append(str(ROOT))

import pandas as pd

from src.features import clean_telco

# %%
raw = pd.read_csv(ROOT / "data/raw/telco_churn.csv")
df = clean_telco(raw)

# %%
import matplotlib.pyplot as plt

# %% [markdown]
# ## 1. Overview

# %%
raw.shape

# %%
raw.dtypes

# %%
raw.head()

# %% [markdown]
# ## 2. Blank TotalCharges
#
# `TotalCharges` is read as text, not as a number, because some values are blank.

# %%
raw["TotalCharges"].dtype

# %%
blank = raw["TotalCharges"].str.strip() == ""
blank.sum()

# %% [markdown]
# The blank rows are exactly the customers with `tenure == 0`: brand-new customers with no bill yet.

# %%
(blank == (raw["tenure"] == 0)).all()

# %%
raw.loc[blank, ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]]

# %% [markdown]
# ## 3. Target balance

# %%
df["Churn"].mean()

# %%
ax = df["Churn"].value_counts().sort_index().plot(kind="bar")
ax.set_title("Target balance")
ax.set_xlabel("Churn (0 = No, 1 = Yes)")
ax.set_ylabel("Number of customers")
plt.show()

# %% [markdown]
# ## 4. Churn rate by category


# %%
def plot_churn_rate(by, title, xlabel):
    rate = df.groupby(by, observed=True)["Churn"].mean()
    ax = rate.plot(kind="bar")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Churn rate")
    plt.xticks(rotation=30, ha="right")
    plt.show()
    return rate


# %%
plot_churn_rate("Contract", "Churn rate by contract type", "Contract")

# %%
plot_churn_rate("InternetService", "Churn rate by internet service", "Internet service")

# %%
plot_churn_rate("PaymentMethod", "Churn rate by payment method", "Payment method")

# %%
tenure_bin = pd.cut(df["tenure"], [0, 12, 24, 48, 72])
plot_churn_rate(tenure_bin, "Churn rate by tenure", "Tenure (months)")

# %% [markdown]
# ## 5. Numeric features by churn

# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, col in zip(axes, ["tenure", "MonthlyCharges"], strict=True):
    df.boxplot(column=col, by="Churn", ax=ax)
    ax.set_title(f"{col} by churn")
    ax.set_xlabel("Churn (0 = No, 1 = Yes)")
    ax.set_ylabel(col)
fig.suptitle("")
plt.show()

# %% [markdown]
# Median of each numeric feature for non-churners (0) and churners (1):

# %%
df.groupby("Churn")[["tenure", "MonthlyCharges"]].median()

# %% [markdown]
# ## 6. Key findings
#
# - The target is imbalanced: about **26.5%** of customers churn, so accuracy alone is misleading
#   (use ROC AUC / F1).
# - `TotalCharges` has **11 blank values**, exactly the customers with `tenure == 0`; they are
#   NaN after `clean_telco` and must be imputed on the train split only.
# - **Contract** is the strongest signal: month-to-month customers churn at ~43%, versus ~11%
#   (one year) and ~3% (two year).
# - **Fiber optic** customers churn at ~42%, and **electronic check** payers at ~45%, far above
#   the other groups.
# - Churn falls with **tenure**: ~48% in the first 12 months versus ~10% after 48 months;
#   churners have a median tenure of 10 months versus 38.
# - Churners pay more per month (median `MonthlyCharges` ~80 versus ~64).
