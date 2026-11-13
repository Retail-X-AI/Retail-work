"""M12-02: Generate advisory reorder recommendations from forecast outputs."""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from reorder import (
    DEFAULT_LEAD_TIME_DAYS,
    DEFAULT_REVIEW_PERIOD_DAYS,
    DEFAULT_SAFETY_STOCK_DAYS,
    calculate_reorder_recommendation,
)


RESTOCKING_DIR = Path(__file__).resolve().parent
REPO_ROOT = RESTOCKING_DIR.parents[1]
DATA_FILE = REPO_ROOT / "dataset" / "raw" / "retail_store_inventory.csv"
FORECAST_FILE = (
    REPO_ROOT
    / "python-ai"
    / "forecasting"
    / "outputs"
    / "retail_demand_forecasts_m11_06.csv"
)
OUTPUT_DIR = RESTOCKING_DIR / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "retail_restocking_recommendations_m12_02.csv"
SUMMARY_FILE = OUTPUT_DIR / "retail_restocking_summary_m12_02.json"
REPORT_FILE = REPO_ROOT / "documentation" / "07-ai" / "M12-02-reorder-recommendations.md"

KEY_COLUMNS = ["Date", "Store ID", "Product ID"]


def prepare_inventory_history(inventory_df):
    """Prepare inventory data and prior-only demand fallback by series."""
    required = KEY_COLUMNS + ["Inventory Level", "Units Sold"]
    missing = [column for column in required if column not in inventory_df.columns]
    if missing:
        raise ValueError(f"Inventory dataset is missing required columns: {missing}")

    data = inventory_df[required].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce").dt.normalize()
    data = data.dropna(subset=["Date", "Store ID", "Product ID"])
    data["Store ID"] = data["Store ID"].astype(str)
    data["Product ID"] = data["Product ID"].astype(str)
    data["Inventory Level"] = pd.to_numeric(data["Inventory Level"], errors="coerce")
    data["Units Sold"] = pd.to_numeric(data["Units Sold"], errors="coerce")
    data = data.sort_values(KEY_COLUMNS, kind="stable").reset_index(drop=True)

    duplicates = data.duplicated(KEY_COLUMNS, keep=False)
    if duplicates.any():
        raise ValueError(
            "Inventory input has duplicate Date/Store ID/Product ID rows; "
            "resolve duplicates before generating recommendations."
        )

    data["Prior 7-Day Mean Demand"] = data.groupby(
        ["Store ID", "Product ID"], sort=False
    )["Units Sold"].transform(
        lambda values: values.shift(1).rolling(window=7, min_periods=1).mean()
    )
    return data[KEY_COLUMNS + ["Inventory Level", "Prior 7-Day Mean Demand"]]


def build_recommendations(inventory_df, forecast_df):
    """Join forecast and inventory rows and calculate one recommendation per row."""
    forecast_required = KEY_COLUMNS + ["Forecast Units Sold"]
    missing = [column for column in forecast_required if column not in forecast_df.columns]
    if missing:
        raise ValueError(f"Forecast file is missing required columns: {missing}")

    forecasts = forecast_df.copy()
    forecasts["Date"] = pd.to_datetime(forecasts["Date"], errors="coerce").dt.normalize()
    forecasts = forecasts.dropna(subset=["Date", "Store ID", "Product ID"])
    forecasts["Store ID"] = forecasts["Store ID"].astype(str)
    forecasts["Product ID"] = forecasts["Product ID"].astype(str)
    forecasts["Forecast Units Sold"] = pd.to_numeric(
        forecasts["Forecast Units Sold"], errors="coerce"
    )

    duplicate_forecasts = forecasts.duplicated(KEY_COLUMNS, keep=False)
    if duplicate_forecasts.any():
        raise ValueError(
            "Forecast input has duplicate Date/Store ID/Product ID rows."
        )

    inventory = prepare_inventory_history(inventory_df)
    merged = forecasts.merge(
        inventory,
        on=KEY_COLUMNS,
        how="left",
        validate="one_to_one",
    )

    rows = []
    for record in merged.to_dict(orient="records"):
        model_forecast = record.get("Forecast Units Sold")
        history_fallback = record.get("Prior 7-Day Mean Demand")

        if model_forecast is not None and np.isfinite(model_forecast):
            demand = max(0.0, float(model_forecast))
            demand_source = "SAVED_MODEL_FORECAST"
        elif history_fallback is not None and np.isfinite(history_fallback):
            demand = max(0.0, float(history_fallback))
            demand_source = "PRIOR_7_DAY_MEAN"
        else:
            demand = None
            demand_source = "UNAVAILABLE"

        result = calculate_reorder_recommendation(
            current_stock=record.get("Inventory Level"),
            forecast_daily_demand=demand,
            lead_time_days=DEFAULT_LEAD_TIME_DAYS,
            review_period_days=DEFAULT_REVIEW_PERIOD_DAYS,
            safety_stock_days=DEFAULT_SAFETY_STOCK_DAYS,
        )

        rows.append({
            "Date": pd.Timestamp(record["Date"]).strftime("%Y-%m-%d"),
            "Store ID": record["Store ID"],
            "Product ID": record["Product ID"],
            "Inventory Level": record.get("Inventory Level"),
            "Forecast Units Sold": model_forecast,
            "Prior 7-Day Mean Demand": history_fallback,
            "Demand Used for Recommendation": demand,
            "Demand Source": demand_source,
            "Lead Time Days": DEFAULT_LEAD_TIME_DAYS,
            "Review Period Days": DEFAULT_REVIEW_PERIOD_DAYS,
            "Safety Stock Days": DEFAULT_SAFETY_STOCK_DAYS,
            **result,
        })

    output = pd.DataFrame(rows).sort_values(KEY_COLUMNS, kind="stable").reset_index(drop=True)
    return output


def main():
    print("=" * 65)
    print("RETAILAI - M12-02 REORDER RECOMMENDATIONS")
    print("=" * 65)

    if not DATA_FILE.is_file():
       raise FileNotFoundError(f"Inventory dataset not found: {DATA_FILE}")
    if not FORECAST_FILE.is_file():
        raise FileNotFoundError(
            f"Forecast outputs not found: {FORECAST_FILE}. "
            "Run python .\\python-ai\\forecasting\\forecast.py first."
        )

    inventory_df = pd.read_csv(DATA_FILE, dtype={"Store ID": str, "Product ID": str})
    forecast_df = pd.read_csv(
        FORECAST_FILE, dtype={"Store ID": str, "Product ID": str}
    )
    recommendations = build_recommendations(inventory_df, forecast_df)

    if recommendations.empty:
        raise ValueError("No forecast rows were available for reorder recommendations.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    recommendations.to_csv(OUTPUT_FILE, index=False)

    status_counts = {
        str(status): int(count)
        for status, count in recommendations["recommendation_status"].value_counts().items()
    }
    reorder_rows = recommendations.loc[
        recommendations["recommendation_status"] == "REORDER_NOW"
    ]
    valid_quantities = recommendations["suggested_order_quantity"].dropna()

    summary = {
        "issue": "M12-02",
        "recommendation_method": "Reorder point and target stock using M12-01 assumptions",
        "lead_time_days": DEFAULT_LEAD_TIME_DAYS,
        "review_period_days": DEFAULT_REVIEW_PERIOD_DAYS,
        "safety_stock_days": DEFAULT_SAFETY_STOCK_DAYS,
        "records_processed": int(len(recommendations)),
        "unique_store_product_pairs": int(
            recommendations[["Store ID", "Product ID"]].drop_duplicates().shape[0]
        ),
        "date_start": str(recommendations["Date"].min()),
        "date_end": str(recommendations["Date"].max()),
        "status_counts": status_counts,
        "reorder_now_count": int(len(reorder_rows)),
        "records_with_positive_order_quantity": int((valid_quantities > 0).sum()),
        "total_suggested_order_units": int(valid_quantities.sum()),
        "output_file": OUTPUT_FILE.relative_to(REPO_ROOT).as_posix(),
        "important_note": (
            "These are historical replay recommendations aligned to the forecast dataset dates, "
            "not live recommendations for current inventory."
        ),
    }
    SUMMARY_FILE.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    status_table = "\n".join(
        f"| {status} | {count:,} |" for status, count in sorted(status_counts.items())
    ) or "| No records | 0 |"
    report = f"""# M12-02 — Reorder Recommendations

## Objective

Generate advisory inventory reorder recommendations from the M11-06 forecast output and inventory records using the baseline assumptions defined in M12-01.

## Method

- Match forecast and inventory data by date, store and product.
- Prefer the saved model forecast; use the prior 7-day mean of observed demand only when a model forecast is unavailable.
- Calculate safety stock, reorder point, target stock and suggested order quantity.
- Flag missing/invalid inventory or unavailable demand instead of inventing quantities.
- Generate one recommendation per matched forecast row; recommendations are advisory and do not place orders.

## Configured assumptions

| Setting | Value |
|---|---:|
| Supplier lead time | {DEFAULT_LEAD_TIME_DAYS} days |
| Review period | {DEFAULT_REVIEW_PERIOD_DAYS} day(s) |
| Safety-stock buffer | {DEFAULT_SAFETY_STOCK_DAYS} day(s) of demand |

These are provisional defaults and should be updated when verified supplier and operational data becomes available.

## Run summary

| Item | Result |
|---|---|
| Records processed | {len(recommendations):,} |
| Store-product pairs | {summary['unique_store_product_pairs']:,} |
| Date range | {summary['date_start']} to {summary['date_end']} |
| REORDER_NOW records | {summary['reorder_now_count']:,} |
| Records with positive order quantity | {summary['records_with_positive_order_quantity']:,} |
| Total suggested order units across historical records | {summary['total_suggested_order_units']:,} |

## Status counts

| Status | Records |
|---|---:|
{status_table}

## Outputs

- Recommendations CSV: `python-ai/restocking/outputs/retail_restocking_recommendations_m12_02.csv`
- Summary JSON: `python-ai/restocking/outputs/retail_restocking_summary_m12_02.json`

## Reproduce

Run from the repository root:

```powershell
python .\\python-ai\\restocking\\recommendations.py
```

**Scope note:** this output is a historical replay using inventory values from the dates in the forecasting test period. It is not a live current-stock recommendation feed.
"""
    REPORT_FILE.write_text(report, encoding="utf-8")

    print("\nRecommendation generation completed successfully.")
    print(f"Records processed: {len(recommendations):,}")
    print(f"Date range: {summary['date_start']} to {summary['date_end']}")
    print(f"Reorder now: {summary['reorder_now_count']:,}")
    print(f"Records with positive suggested order quantity: {summary['records_with_positive_order_quantity']:,}")
    print(f"CSV: {OUTPUT_FILE}")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Evidence report: {REPORT_FILE}")
    print(summary["important_note"])


if __name__ == "__main__":
    main()
