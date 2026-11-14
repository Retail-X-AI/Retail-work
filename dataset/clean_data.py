
from pathlib import Path
from datetime import datetime

import pandas as pd

from load_dataset import load_dataset


REPO_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = REPO_ROOT / "dataset" / "processed"
CLEANED_FILE = OUTPUT_DIR / "retail_store_inventory_clean.csv"
REPORT_FILE = Path(__file__).resolve().parent / "M10-02-cleaning-validation-report.md"

REQUIRED_COLUMNS = [
    "Date",
    "Store ID",
    "Product ID",
    "Units Sold",
]

EXPECTED_COLUMNS = [
    "Date",
    "Store ID",
    "Product ID",
    "Category",
    "Region",
    "Inventory Level",
    "Units Sold",
    "Units Ordered",
    "Demand Forecast",
    "Price",
    "Discount",
    "Weather Condition",
    "Holiday/Promotion",
    "Competitor Pricing",
    "Seasonality",
]

NUMERIC_COLUMNS = [
    "Inventory Level",
    "Units Sold",
    "Units Ordered",
    "Demand Forecast",
    "Price",
    "Discount",
    "Holiday/Promotion",
    "Competitor Pricing",
]


def clean_and_validate():
    """Clean the approved dataset and produce a validation report."""

    print("\n" + "=" * 60)
    print("RETAILAI - DATA CLEANING AND VALIDATION")
    print("=" * 60)

    # Load the source dataset without modifying the raw CSV.
    df = load_dataset()
    initial_rows = len(df)
    initial_columns = len(df.columns)

    missing_expected = [
        column for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    missing_required = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_required:
        raise ValueError(
            "Required columns are missing: "
            + ", ".join(missing_required)
        )

    # Normalize text fields and convert blank strings to missing values.
    for column in df.columns:
        df[column] = df[column].map(
            lambda value: value.strip()
            if isinstance(value, str) else value
        )

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Record missing values before cleaning.
    missing_before = df.isna().sum()

    # Convert dates and record invalid date values.
    original_dates = df["Date"].copy()
    df["Date"] = pd.to_datetime(
        df["Date"], errors="coerce"
    )

    invalid_dates = int(
        (original_dates.notna() & df["Date"].isna()).sum()
    )

    # Convert numeric fields and record invalid values.
    invalid_numeric = {}

    for column in NUMERIC_COLUMNS:
        if column not in df.columns:
            continue

        original_values = df[column].copy()
        converted_values = pd.to_numeric(
            original_values, errors="coerce"
        )

        invalid_numeric[column] = int(
            (original_values.notna() & converted_values.isna()).sum()
        )

        df[column] = converted_values

    # Remove exact duplicate records, keeping the first occurrence.
    exact_duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Remove rows that cannot identify a dated sales observation.
    rows_before_required_check = len(df)

    df = df.dropna(subset=REQUIRED_COLUMNS).copy()

    missing_required_rows_removed = (
        rows_before_required_check - len(df)
    )

    # Validate suspicious values without silently deleting them.
    negative_sales = (
        int((df["Units Sold"] < 0).sum())
        if "Units Sold" in df.columns else 0
    )

    negative_demand_forecasts = (
        int((df["Demand Forecast"] < 0).sum())
        if "Demand Forecast" in df.columns else 0
    )

    negative_inventory = (
        int((df["Inventory Level"] < 0).sum())
        if "Inventory Level" in df.columns else 0
    )

    # Identify repeated date/store/product combinations.
    business_key = ["Date", "Store ID", "Product ID"]

    duplicate_business_key_rows = int(
        df.duplicated(subset=business_key, keep=False).sum()
    )

    # Sort the cleaned observations for consistent downstream processing.
    df = df.sort_values(
        business_key
    ).reset_index(drop=True)

    missing_after = df.isna().sum()

    # Save cleaned data separately from the original raw dataset.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_FILE, index=False, date_format="%Y-%m-%d")

    # Build a reproducible Markdown evidence report.
    report = [
        "# M10-02 — Dataset Cleaning and Validation",
        "",
        f"- **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "- **Source:** `dataset/raw/retail_store_inventory.csv`",
        "- **Cleaning script:** `python-ai/data/clean_data.py`",
        f"- **Original rows:** {initial_rows:,}",
        f"- **Original columns:** {initial_columns}",
        f"- **Final cleaned rows:** {len(df):,}",
        f"- **Final columns:** {len(df.columns)}",
        f"- **Exact duplicate rows removed:** {exact_duplicates:,}",
        f"- **Rows removed for missing required values:** {missing_required_rows_removed:,}",
        f"- **Invalid dates converted to missing:** {invalid_dates:,}",
        f"- **Rows with negative Units Sold retained for review:** {negative_sales:,}",
        f"- **Rows with negative Demand Forecast retained for review:** {negative_demand_forecasts:,}",
        f"- **Rows with negative Inventory Level retained for review:** {negative_inventory:,}",
        f"- **Rows belonging to repeated date/store/product keys:** {duplicate_business_key_rows:,}",
        "",
        "## Schema validation",
        "",
        f"- **Missing expected columns:** {', '.join(missing_expected) if missing_expected else 'None'}",
        f"- **Unexpected columns:** {', '.join(unexpected_columns) if unexpected_columns else 'None'}",
        "",
        "## Missing values before cleaning",
        "",
        "| Column | Missing values |",
        "|---|---:|",
    ]

    for column, count in missing_before.items():
        report.append(f"| {column} | {int(count):,} |")

    report.extend([
        "",
        "## Missing values after cleaning",
        "",
        "| Column | Missing values |",
        "|---|---:|",
    ])

    for column, count in missing_after.items():
        report.append(f"| {column} | {int(count):,} |")

    report.extend([
        "",
        "## Invalid numeric values",
        "",
        "| Column | Values that could not be converted |",
        "|---|---:|",
    ])

    for column, count in invalid_numeric.items():
        report.append(f"| {column} | {count:,} |")

    report.extend([
        "",
        "## Cleaning decisions",
        "",
        "- The original raw CSV is not modified.",
        "- Blank text values are treated as missing.",
        "- Dates and numeric columns are converted to appropriate types.",
        "- Exact duplicate records are removed.",
        "- Rows missing Date, Store ID, Product ID, or Units Sold are removed.",
        "- Negative values and repeated business keys are reported for review, not silently deleted.",
        "- Missing optional values are reported rather than automatically imputed.",
        "",
        f"**Cleaned dataset:** `{CLEANED_FILE.relative_to(REPO_ROOT)}`",
        "",
    ])

    REPORT_FILE.write_text(
        "\n".join(report), encoding="utf-8"
    )

    # Print a concise summary as test evidence.
    print("\nCLEANING SUMMARY")
    print("-" * 60)
    print(f"Original rows:                 {initial_rows:,}")
    print(f"Original columns:              {initial_columns}")
    print(f"Exact duplicates removed:      {exact_duplicates:,}")
    print(f"Rows missing required values:  {missing_required_rows_removed:,}")
    print(f"Invalid dates:                 {invalid_dates:,}")
    print(f"Cleaned rows:                  {len(df):,}")
    print(f"Negative demand forecasts:     {negative_demand_forecasts:,}")
    print(f"Repeated business-key rows:    {duplicate_business_key_rows:,}")
    print(f"\nCleaned CSV saved to: {CLEANED_FILE}")
    print(f"Validation report saved to: {REPORT_FILE}")

    return df


if __name__ == "__main__":
    clean_and_validate()
