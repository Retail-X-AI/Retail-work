
"""Retail-X-AI historical sales analysis."""

from pathlib import Path

import pandas as pd


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[1]

DATA_FILE = (
    REPO_ROOT
    / "dataset"
    / "raw"
    / "retail_store_inventory.csv"
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_sales_data():
    """Load and validate historical retail sales data."""

    if not DATA_FILE.is_file():
        raise FileNotFoundError(
            f"Sales dataset not found: {DATA_FILE}"
        )

    data = pd.read_csv(
        DATA_FILE,
        dtype={
            "Store ID": str,
            "Product ID": str
        }
    )

    required_columns = [
        "Date",
        "Store ID",
        "Product ID",
        "Category",
        "Units Sold",
        "Price",
        "Discount",
        "Holiday/Promotion",
        "Weather Condition",
        "Seasonality"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required sales columns: {missing_columns}"
        )

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "Units Sold",
        "Price",
        "Discount",
        "Holiday/Promotion"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(
        subset=[
            "Date",
            "Store ID",
            "Product ID",
            "Units Sold"
        ]
    )

    if data.empty:
        raise ValueError("No valid sales records are available.")

    return data


# --------------------------------------------------
# SALES SUMMARY
# --------------------------------------------------

def generate_sales_summary():
    """Generate an overall summary of historical sales."""

    data = load_sales_data()

    daily_sales = (
        data.groupby("Date")["Units Sold"]
        .sum()
    )

    store_sales = (
        data.groupby("Store ID")["Units Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    category_sales = (
        data.groupby("Category")["Units Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "total_records": len(data),
        "total_units_sold": data["Units Sold"].sum(),
        "average_daily_sales": daily_sales.mean(),
        "highest_sales_day": daily_sales.idxmax(),
        "highest_daily_sales": daily_sales.max(),
        "start_date": data["Date"].min(),
        "end_date": data["Date"].max(),
        "store_sales": store_sales,
        "category_sales": category_sales
    }


# --------------------------------------------------
# SALES FACTOR ANALYSIS
# --------------------------------------------------

def analyze_sales_factors():
    """Examine relationships between dataset factors and units sold."""

    data = load_sales_data()

    promotion_sales = (
        data.groupby("Holiday/Promotion")["Units Sold"]
        .agg(["count", "mean"])
    )

    weather_sales = (
        data.groupby("Weather Condition")["Units Sold"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
    )

    seasonal_sales = (
        data.groupby("Seasonality")["Units Sold"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
    )

    numeric_correlations = (
        data[
            [
                "Units Sold",
                "Price",
                "Discount",
                "Competitor Pricing"
            ]
        ]
        .corr()["Units Sold"]
        .drop("Units Sold")
        .sort_values(ascending=False)
    )

    return {
        "promotion_sales": promotion_sales,
        "weather_sales": weather_sales,
        "seasonal_sales": seasonal_sales,
        "numeric_correlations": numeric_correlations
    }


# --------------------------------------------------
# TOP SELLING PRODUCTS
# --------------------------------------------------


def get_top_selling_products(store_id=None, limit=10):
    """Rank product IDs by total historical units sold."""

    data = load_sales_data()

    if store_id:
        store_id = store_id.upper()

        data = data[
            data["Store ID"] == store_id
        ]

        if data.empty:
            return data

    products = (
        data.groupby("Product ID", as_index=False)
        .agg(
            total_units_sold=("Units Sold", "sum"),
            average_units_sold=("Units Sold", "mean"),
            sales_records=("Units Sold", "count"),
            categories=("Category", lambda x: ", ".join(
                sorted(x.unique())
            ))
        )
        .sort_values(
            "total_units_sold",
            ascending=False
        )
        .head(limit)
        .reset_index(drop=True)
    )

    products.insert(
        0,
        "Rank",
        range(1, len(products) + 1)
    )

    return products
