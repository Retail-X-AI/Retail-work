"""
M02-04 - Document dataset variable meanings (Data Dictionary)

Generates a data dictionary for the raw retail store inventory dataset.
For each column it produces: dtype, non-null count, unique count, sample
values, min/max (numeric), and any known notes.

Usage:
    python data_dictionary.py

Author: Khanyisile Skhulile
Issue:  M02-04
"""

import os
from datetime import datetime

import pandas as pd


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATASET_PATH = os.path.join(REPO_ROOT, "dataset", "raw", "retail_store_inventory.csv")
OUTPUT_DIR = os.path.join(REPO_ROOT, "documentation", "03-data-analysis")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "M02-04-data-dictionary.md")


# Human-written meanings and notes for each column.
# Update if the dataset schema changes.
COLUMN_NOTES = {
    "Date": {
        "meaning": "Date of the record (daily granularity).",
        "units": "YYYY-MM-DD",
        "notes": "Covers 2022-01-01 to 2022-09-30.",
    },
    "Store ID": {
        "meaning": "Unique identifier for the retail store.",
        "units": "S001 - S005",
        "notes": "5 stores total.",
    },
    "Product ID": {
        "meaning": "Unique identifier for the product.",
        "units": "P0001 - P0020",
        "notes": "20 products total.",
    },
    "Category": {
        "meaning": "Product category.",
        "units": "text",
        "notes": "Groceries, Toys, Electronics, Furniture, Clothing.",
    },
    "Region": {
        "meaning": "Geographic region of the store.",
        "units": "text",
        "notes": "North, South, East, West.",
    },
    "Inventory Level": {
        "meaning": "Stock on hand at the start of the day.",
        "units": "units",
        "notes": "Non-negative.",
    },
    "Units Sold": {
        "meaning": "Number of units sold that day.",
        "units": "units",
        "notes": "Non-negative.",
    },
    "Units Ordered": {
        "meaning": "Number of units ordered from the supplier that day.",
        "units": "units",
        "notes": "Non-negative.",
    },
    "Demand Forecast": {
        "meaning": "Forecasted demand for that day.",
        "units": "units",
        "notes": "WARNING: contains negative values (673 rows). Needs cleaning.",
    },
    "Price": {
        "meaning": "Selling price per unit.",
        "units": "currency",
        "notes": "Positive.",
    },
    "Discount": {
        "meaning": "Discount applied to the price.",
        "units": "0-1 (fraction) or percentage",
        "notes": "0 means no discount.",
    },
    "Weather Condition": {
        "meaning": "Weather on the day of the record.",
        "units": "text",
        "notes": "e.g. Sunny, Rainy, Cloudy.",
    },
    "Holiday/Promotion": {
        "meaning": "Whether the day was a holiday or promotion day.",
        "units": "0 or 1",
        "notes": "Kaggle source called this column 'Promotion'.",
    },
    "Competitor Pricing": {
        "meaning": "Competitor's price for the same product.",
        "units": "currency",
        "notes": "Positive.",
    },
    "Seasonality": {
        "meaning": "Season of the year.",
        "units": "text",
        "notes": "Spring, Summer, Autumn, Winter.",
    },
}


def generate_data_dictionary():
    print(f"Loading dataset from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)

    lines = []
    lines.append("# M02-04 - Data Dictionary\n")
    lines.append("**Issue:** M02-04  ")
    lines.append("**Analyst:** Khanyisile Skhulile  ")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append("**Source file:** `dataset/raw/retail_store_inventory.csv`\n")
    lines.append("---\n")

    lines.append("## Overview\n")
    lines.append(f"- **Rows:** {df.shape[0]:,}")
    lines.append(f"- **Columns:** {df.shape[1]}")
    lines.append("- **Granularity:** one row per (Date, Store ID, Product ID)\n")
    lines.append("---\n")

    lines.append("## Column Definitions\n")

    for col in df.columns:
        note = COLUMN_NOTES.get(col, {})
        meaning = note.get("meaning", "(to be defined)")
        units = note.get("units", "-")
        extra = note.get("notes", "")

        lines.append(f"### `{col}`\n")
        lines.append(f"- **Meaning:** {meaning}")
        lines.append(f"- **Units / Format:** {units}")
        lines.append(f"- **Data type:** {df[col].dtype}")
        lines.append(f"- **Non-null count:** {df[col].notna().sum():,} / {df.shape[0]:,}")
        lines.append(f"- **Unique values:** {df[col].nunique(dropna=True):,}")

        if pd.api.types.is_numeric_dtype(df[col]):
            lines.append(
                f"- **Range:** {df[col].min():.2f} to {df[col].max():.2f}"
            )
            lines.append(
                f"- **Mean / Std:** {df[col].mean():.2f} / {df[col].std():.2f}"
            )
        else:
            sample = df[col].dropna().unique()[:5].tolist()
            lines.append(f"- **Sample values:** {sample}")

        if extra:
            lines.append(f"- **Notes:** {extra}")
        lines.append("")

    lines.append("---\n")
    lines.append("## Column Summary Table\n")
    lines.append("| # | Column | Type | Unique | Missing | Meaning |")
    lines.append("|---|--------|------|--------|---------|---------|")
    for i, col in enumerate(df.columns, 1):
        note = COLUMN_NOTES.get(col, {})
        meaning = note.get("meaning", "-")
        lines.append(
            f"| {i} | `{col}` | {df[col].dtype} | "
            f"{df[col].nunique(dropna=True):,} | "
            f"{df[col].isna().sum():,} | {meaning} |"
        )
    lines.append("")

    lines.append("---\n")
    lines.append("## Notes and Caveats\n")
    lines.append("- `Demand Forecast` contains 673 negative values that should be cleaned before modelling.")
    lines.append("- The dataset is **synthetic** (per the Kaggle source documented in `DATASET-SOURCE.md`).")
    lines.append("- `Holiday/Promotion` may correspond to the 'Promotion' column in the Kaggle source.")
    lines.append("- Granularity: one row per store per product per day.\n")

    report = "\n".join(lines)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport written to: {OUTPUT_PATH}\n")
    print(report[:2000])


if __name__ == "__main__":
    generate_data_dictionary()