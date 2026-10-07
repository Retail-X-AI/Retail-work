"""
M02-05 - Identify forecasting target and leakage risks

Analyses the raw retail store inventory dataset to:
  1. Recommend a forecasting target column.
  2. Identify leakage-risk columns that should NOT be used as
     model inputs when predicting that target.

Produces a markdown report at
documentation/03-data-analysis/M02-05-target-and-leakage.md

Usage:
    python target_and_leakage_analysis.py

Author: Khanyisile Skhulile
Issue:  M02-05
"""

import os
from datetime import datetime

import pandas as pd


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATASET_PATH = os.path.join(REPO_ROOT, "dataset", "raw", "retail_store_inventory.csv")
OUTPUT_DIR = os.path.join(REPO_ROOT, "documentation", "03-data-analysis")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "M02-05-target-and-leakage.md")


LEAKAGE_COLUMNS = {
    "Demand Forecast": (
        "Direct derivative of the target. If we predict Units Sold, "
        "Demand Forecast already encodes the answer. Including it as "
        "an input would be pure data leakage. Also currently contains "
        "673 negative values, so it is not yet reliable as a target either."
    ),
    "Units Ordered": (
        "Reflects post-sale restocking decisions. Often causally "
        "downstream of Units Sold - you order more because you sold more. "
        "Using it as an input would leak the outcome."
    ),
    "Inventory Level": (
        "End-of-day stock is affected by how many units were sold. "
        "If the level is measured at end of day, it contains post-sale "
        "information - a mild leakage risk. Only safe to use if measured "
        "at the start of the day before any sales."
    ),
}


RECOMMENDED_TARGET = "Units Sold"
TARGET_REASON = (
    "`Units Sold` is the concrete, observable quantity we want to forecast "
    "at daily (Store, Product) granularity. It represents what actually "
    "happened at the till - which is what 'demand' means in a retail "
    "context. It has no negative values and its distribution is realistic."
)


SAFE_FEATURES = [
    "Date",
    "Store ID",
    "Product ID",
    "Category",
    "Region",
    "Price",
    "Discount",
    "Competitor Pricing",
    "Weather Condition",
    "Holiday/Promotion",
    "Seasonality",
]


def analyse():
    print(f"Loading dataset from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)

    lines = []
    lines.append("# M02-05 - Forecasting Target and Leakage Analysis\n")
    lines.append("**Issue:** M02-05  ")
    lines.append("**Analyst:** Khanyisile Skhulile  ")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append("**Source file:** `dataset/raw/retail_store_inventory.csv`\n")
    lines.append("---\n")

    # 1. Recommended target
    lines.append("## 1. Recommended Forecasting Target\n")
    lines.append(f"**Target column:** `{RECOMMENDED_TARGET}`\n")
    lines.append(f"**Reason:** {TARGET_REASON}\n")

    if RECOMMENDED_TARGET in df.columns:
        s = df[RECOMMENDED_TARGET]
        lines.append("### Target column statistics\n")
        lines.append(f"- **Type:** {s.dtype}")
        lines.append(f"- **Non-null:** {s.notna().sum():,} / {len(s):,}")
        lines.append(f"- **Min:** {s.min():.2f}")
        lines.append(f"- **Max:** {s.max():.2f}")
        lines.append(f"- **Mean:** {s.mean():.2f}")
        lines.append(f"- **Std:** {s.std():.2f}")
        lines.append(f"- **Negative values:** {(s < 0).sum():,}\n")

    # 2. Leakage risks
    lines.append("## 2. Leakage Risk Columns\n")
    lines.append("These columns must **NOT** be used as inputs when predicting the target:\n")
    for col, reason in LEAKAGE_COLUMNS.items():
        present = "yes" if col in df.columns else "no"
        lines.append(f"### `{col}` (present in dataset: {present})\n")
        lines.append(f"{reason}\n")

    # 3. Safe features
    lines.append("## 3. Safe Feature Columns\n")
    lines.append("The following columns are safe to use as model inputs because their "
                 "values are known **before** the day's sales occur:\n")
    for col in SAFE_FEATURES:
        present = "yes" if col in df.columns else "no"
        lines.append(f"- `{col}` (present: {present})")
    lines.append("")

    # 4. Correlation check
    lines.append("## 4. Correlation of Numeric Columns with the Target\n")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if RECOMMENDED_TARGET in numeric_cols:
        corr = (
            df[numeric_cols]
            .corr()[RECOMMENDED_TARGET]
            .drop(RECOMMENDED_TARGET)
            .sort_values(key=abs, ascending=False)
        )
        lines.append("| Column | Correlation with target |")
        lines.append("|--------|------------------------|")
        for col, val in corr.items():
            lines.append(f"| `{col}` | {val:.4f} |")
        lines.append("")
        lines.append("High correlation with the target is a **warning sign** for "
                     "potential leakage - investigate any column that correlates "
                     "very strongly with `Units Sold` before using it as a feature.\n")
    else:
        lines.append("Target column is not numeric; skipping correlation analysis.\n")

    # 5. Summary / recommendation
    lines.append("## 5. Summary and Recommendation\n")
    lines.append(f"- **Forecasting target:** `{RECOMMENDED_TARGET}`")
    lines.append(f"- **Excluded (leakage risk):** {', '.join('`'+c+'`' for c in LEAKAGE_COLUMNS)}")
    lines.append(f"- **Safe input features:** {', '.join('`'+c+'`' for c in SAFE_FEATURES)}")
    lines.append("")
    lines.append("### Notes")
    lines.append("- `Demand Forecast` cannot be used as a feature OR as a target in its "
                 "current state - it has 673 negative values.")
    lines.append("- `Inventory Level` is only safe if measured at start-of-day.")
    lines.append("- Time-based train/test split must be used (no random splitting), "
                 "to avoid leaking future information into the training set.")

    report = "\n".join(lines)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport written to: {OUTPUT_PATH}\n")
    print(report[:2500])


if __name__ == "__main__":
    analyse()