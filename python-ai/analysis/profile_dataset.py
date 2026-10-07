"""
M02-02 — Profile dataset rows, columns and date range

Profiles the raw retail store inventory dataset for the Retail-X-AI project.
Outputs a markdown report to documentation/03-data-analysis/.

Usage:
    python profile_dataset.py

Author: Khanyisile Skhulile
Issue:  M02-02
"""

import os
from datetime import datetime

import pandas as pd


# ---------------------------------------------------------------------------
# Paths (relative to the repository root)
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATASET_PATH = os.path.join(REPO_ROOT, "dataset", "raw", "retail_store_inventory.csv")
OUTPUT_DIR = os.path.join(REPO_ROOT, "documentation", "03-data-analysis")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "M02-02-profiling-results.md")


def profile_dataset():
    print(f"Loading dataset from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)

    lines = []
    lines.append("# M02-02 — Dataset Profiling Results\n")
    lines.append("**Issue:** M02-02  ")
    lines.append("**Analyst:** Khanyisile Skhulile  ")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append("**Source file:** `dataset/raw/retail_store_inventory.csv`\n")
    lines.append("---\n")

    # 1. Shape
    lines.append("## 1. Shape\n")
    lines.append(f"- **Rows:** {df.shape[0]:,}")
    lines.append(f"- **Columns:** {df.shape[1]}\n")

    # 2. Columns & dtypes
    lines.append("## 2. Columns and Data Types\n")
    lines.append("| # | Column | Dtype | Non-Null | Null | Unique |")
    lines.append("|---|--------|-------|----------|------|--------|")
    for i, col in enumerate(df.columns, 1):
        nulls = int(df[col].isna().sum())
        non_null = df.shape[0] - nulls
        uniq = int(df[col].nunique(dropna=True))
        lines.append(
            f"| {i} | `{col}` | {df[col].dtype} | {non_null:,} | {nulls:,} | {uniq:,} |"
        )
    lines.append("")

    # 3. Date range
    lines.append("## 3. Date Range\n")
    date_col = None
    for candidate in ["Date", "date", "Order Date", "Transaction Date"]:
        if candidate in df.columns:
            date_col = candidate
            break
    if date_col:
        try:
            dates = pd.to_datetime(df[date_col], errors="coerce")
            lines.append(f"- **Column:** `{date_col}`")
            lines.append(f"- **Earliest:** {dates.min()}")
            lines.append(f"- **Latest:** {dates.max()}")
            lines.append(f"- **Span:** {(dates.max() - dates.min()).days:,} days\n")
        except Exception as exc:
            lines.append(f"- Could not parse dates: {exc}\n")
    else:
        lines.append("- No date column found.\n")

    # 4. Categorical breakdowns
    lines.append("## 4. Categorical Breakdowns\n")
    for col in ["Store ID", "Product ID", "Category", "Region"]:
        if col in df.columns:
            values = sorted(df[col].dropna().unique().tolist())
            lines.append(f"- **{col}** ({len(values)} unique): {values}")
    lines.append("")

    # 5. Missing values
    lines.append("## 5. Missing Values\n")
    total_missing = int(df.isna().sum().sum())
    if total_missing == 0:
        lines.append("No missing values detected.\n")
    else:
        lines.append("| Column | Missing | % |")
        lines.append("|--------|---------|---|")
        for col in df.columns:
            n = int(df[col].isna().sum())
            if n > 0:
                pct = 100 * n / len(df)
                lines.append(f"| `{col}` | {n:,} | {pct:.2f}% |")
        lines.append("")

    # 6. Numeric summary
    lines.append("## 6. Numeric Summary\n")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        lines.append("| Column | Min | Max | Mean | Std |")
        lines.append("|--------|-----|-----|------|-----|")
        for col in numeric_cols:
            lines.append(
                f"| `{col}` | {df[col].min():.2f} | {df[col].max():.2f} | "
                f"{df[col].mean():.2f} | {df[col].std():.2f} |"
            )
        lines.append("")

    # 7. Negative-value check
    lines.append("## 7. Negative-Value Check\n")
    negatives_found = False
    for col in numeric_cols:
        n_neg = int((df[col] < 0).sum())
        if n_neg > 0:
            negatives_found = True
            lines.append(f"- **`{col}`** has **{n_neg:,}** negative values.")
    if not negatives_found:
        lines.append("No negative values detected in numeric columns.")
    lines.append("")

    # 8. Duplicate rows
    lines.append("## 8. Duplicate Rows\n")
    dupes = int(df.duplicated().sum())
    lines.append(f"- **Exact duplicate rows:** {dupes:,}\n")

    # 9. Head sample
    lines.append("## 9. First 5 Rows\n")
    lines.append("```")
    lines.append(df.head(5).to_string())
    lines.append("```\n")

    # Write output
    report = "\n".join(lines)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport written to: {OUTPUT_PATH}\n")
    print(report)


if __name__ == "__main__":
    profile_dataset()