"""M12-03: Detect observed stockouts and forecast-based stockout risk.

This module is advisory only. It does not create purchase orders or claim to
represent live inventory when it is run against historical dataset records.
"""

from math import ceil, isfinite
from pathlib import Path
import json
from typing import Any

DEFAULT_LEAD_TIME_DAYS = 3
DEFAULT_REVIEW_PERIOD_DAYS = 1
DEFAULT_SAFETY_STOCK_DAYS = 1

STATUSES = {
    "STOCKOUT",
    "STOCKOUT_RISK",
    "WATCH",
    "NO_STOCKOUT_RISK",
    "DATA_REQUIRED",
    "INSUFFICIENT_HISTORY",
}


def _number(value: Any):
    """Return a finite float, or None when value is missing or invalid."""
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if isfinite(number) else None


def _validate_setting(name: str, value: Any) -> float:
    number = _number(value)
    if number is None or number < 0:
        raise ValueError(f"{name} must be a finite, non-negative number.")
    return number


def detect_stockout(
    current_stock,
    forecast_daily_demand,
    lead_time_days=DEFAULT_LEAD_TIME_DAYS,
    review_period_days=DEFAULT_REVIEW_PERIOD_DAYS,
    safety_stock_days=DEFAULT_SAFETY_STOCK_DAYS,
):
    """Classify stock availability from on-hand stock and daily demand.

    Thresholds use M12-01 assumptions:
      safety stock = ceil(daily demand * safety-stock days)
      reorder point = ceil(daily demand * lead time + safety stock)
      target stock = ceil(daily demand * (lead time + review period)
                          + safety stock)

    A zero on-hand value is an observed STOCKOUT even when demand is missing.
    Positive stock at/below the reorder point is STOCKOUT_RISK; stock between
    the reorder point and target is WATCH; stock at/above target is clear of
    the baseline stockout-risk threshold. These are planning flags, not a
    guarantee that stock will or will not run out.
    """
    lead_time = _validate_setting("lead_time_days", lead_time_days)
    review_period = _validate_setting("review_period_days", review_period_days)
    buffer_days = _validate_setting("safety_stock_days", safety_stock_days)

    stock = _number(current_stock)
    if stock is None or stock < 0:
        return {
            "safety_stock": None,
            "reorder_point": None,
            "target_stock": None,
            "days_of_cover": None,
            "stockout_status": "DATA_REQUIRED",
            "stockout_reason": "Inventory is missing, invalid or negative; verify the stock record.",
        }

    # This is observable from inventory alone, so it takes precedence over a
    # missing demand forecast.
    if stock == 0:
        demand = _number(forecast_daily_demand)
        normalized_demand = max(0.0, demand) if demand is not None else None
        return {
            "safety_stock": int(ceil(normalized_demand * buffer_days)) if normalized_demand is not None else None,
            "reorder_point": int(ceil(normalized_demand * lead_time + ceil(normalized_demand * buffer_days))) if normalized_demand is not None else None,
            "target_stock": int(ceil(normalized_demand * (lead_time + review_period) + ceil(normalized_demand * buffer_days))) if normalized_demand is not None else None,
            "days_of_cover": 0.0,
            "stockout_status": "STOCKOUT",
            "stockout_reason": "On-hand inventory is zero; confirm availability and replenish according to the approved process.",
        }

    demand = _number(forecast_daily_demand)
    if demand is None:
        return {
            "safety_stock": None,
            "reorder_point": None,
            "target_stock": None,
            "days_of_cover": None,
            "stockout_status": "INSUFFICIENT_HISTORY",
            "stockout_reason": "No valid model forecast or prior-demand fallback is available.",
        }

    demand = max(0.0, demand)
    safety_stock = int(ceil(demand * buffer_days))
    reorder_point = int(ceil(demand * lead_time + safety_stock))
    target_stock = int(ceil(demand * (lead_time + review_period) + safety_stock))
    days_of_cover = None if demand == 0 else round(stock / demand, 2)

    if stock <= reorder_point:
        status = "STOCKOUT_RISK"
        reason = (
            f"Stock {stock:g} is at or below the baseline reorder point {reorder_point}; "
            "demand during supplier lead time may exhaust available stock."
        )
    elif stock < target_stock:
        status = "WATCH"
        reason = (
            f"Stock {stock:g} is above reorder point {reorder_point} but below "
            f"target stock {target_stock}; monitor inventory closely."
        )
    else:
        status = "NO_STOCKOUT_RISK"
        reason = (
            f"Stock {stock:g} meets or exceeds baseline target stock {target_stock}; "
            "continue routine monitoring."
        )

    return {
        "safety_stock": safety_stock,
        "reorder_point": reorder_point,
        "target_stock": target_stock,
        "days_of_cover": days_of_cover,
        "stockout_status": status,
        "stockout_reason": reason,
    }


def build_stockout_detections(inventory_df, forecast_df):
    """Join inventory and model forecasts by date/store/product, then classify.

    When a model forecast is missing, use only the mean of available prior
    seven-day observed demand for that same store/product. Future rows are
    never used as fallback demand for an earlier date.
    """
    import numpy as np
    import pandas as pd

    key_columns = ["Date", "Store ID", "Product ID"]
    inventory_required = key_columns + ["Inventory Level", "Units Sold"]
    forecast_required = key_columns + ["Forecast Units Sold"]
    missing_inventory = [c for c in inventory_required if c not in inventory_df.columns]
    missing_forecast = [c for c in forecast_required if c not in forecast_df.columns]
    if missing_inventory:
        raise ValueError(f"Inventory dataset is missing required columns: {missing_inventory}")
    if missing_forecast:
        raise ValueError(f"Forecast file is missing required columns: {missing_forecast}")

    inventory = inventory_df[inventory_required].copy()
    inventory["Date"] = pd.to_datetime(inventory["Date"], errors="coerce").dt.normalize()
    inventory = inventory.dropna(subset=key_columns)
    for column in ["Store ID", "Product ID"]:
        inventory[column] = inventory[column].astype(str)
    inventory["Inventory Level"] = pd.to_numeric(inventory["Inventory Level"], errors="coerce")
    inventory["Units Sold"] = pd.to_numeric(inventory["Units Sold"], errors="coerce")
    inventory = inventory.sort_values(["Store ID", "Product ID", "Date"], kind="stable")
    if inventory.duplicated(key_columns, keep=False).any():
        raise ValueError("Inventory input contains duplicate Date/Store ID/Product ID rows.")

    inventory["Prior 7-Day Mean Demand"] = inventory.groupby(
        ["Store ID", "Product ID"], sort=False
    )["Units Sold"].transform(
        lambda values: values.shift(1).rolling(window=7, min_periods=1).mean()
    )

    forecasts = forecast_df[key_columns + ["Forecast Units Sold"]].copy()
    forecasts["Date"] = pd.to_datetime(forecasts["Date"], errors="coerce").dt.normalize()
    forecasts = forecasts.dropna(subset=key_columns)
    for column in ["Store ID", "Product ID"]:
        forecasts[column] = forecasts[column].astype(str)
    forecasts["Forecast Units Sold"] = pd.to_numeric(forecasts["Forecast Units Sold"], errors="coerce")
    if forecasts.duplicated(key_columns, keep=False).any():
        raise ValueError("Forecast input contains duplicate Date/Store ID/Product ID rows.")

    merged = forecasts.merge(
        inventory[key_columns + ["Inventory Level", "Prior 7-Day Mean Demand"]],
        on=key_columns,
        how="left",
        validate="one_to_one",
    )

    rows = []
    for record in merged.to_dict(orient="records"):
        forecast_demand = record.get("Forecast Units Sold")
        prior_mean = record.get("Prior 7-Day Mean Demand")
        if forecast_demand is not None and np.isfinite(forecast_demand):
            used_demand = max(0.0, float(forecast_demand))
            demand_source = "SAVED_MODEL_FORECAST"
        elif prior_mean is not None and np.isfinite(prior_mean):
            used_demand = max(0.0, float(prior_mean))
            demand_source = "PRIOR_7_DAY_MEAN"
        else:
            used_demand = None
            demand_source = "UNAVAILABLE"

        result = detect_stockout(
            current_stock=record.get("Inventory Level"),
            forecast_daily_demand=used_demand,
            lead_time_days=DEFAULT_LEAD_TIME_DAYS,
            review_period_days=DEFAULT_REVIEW_PERIOD_DAYS,
            safety_stock_days=DEFAULT_SAFETY_STOCK_DAYS,
        )
        rows.append({
            "Date": pd.Timestamp(record["Date"]).strftime("%Y-%m-%d"),
            "Store ID": record["Store ID"],
            "Product ID": record["Product ID"],
            "Inventory Level": record.get("Inventory Level"),
            "Forecast Units Sold": forecast_demand,
            "Prior 7-Day Mean Demand": prior_mean,
            "Demand Used for Detection": used_demand,
            "Demand Source": demand_source,
            "Lead Time Days": DEFAULT_LEAD_TIME_DAYS,
            "Review Period Days": DEFAULT_REVIEW_PERIOD_DAYS,
            "Safety Stock Days": DEFAULT_SAFETY_STOCK_DAYS,
            **result,
        })

    return pd.DataFrame(rows).sort_values(key_columns, kind="stable").reset_index(drop=True)


def main():
    """Generate historical stockout-detection evidence from repository data."""
    import pandas as pd

    restocking_dir = Path(__file__).resolve().parent
    repo_root = restocking_dir.parents[1]
    data_file = repo_root / "dataset" / "raw" / "retail_store_inventory.csv"
    forecast_file = repo_root / "python-ai" / "forecasting" / "outputs" / "retail_demand_forecasts_m11_06.csv"
    output_dir = restocking_dir / "outputs"
    output_file = output_dir / "retail_stockout_detection_m12_03.csv"
    summary_file = output_dir / "retail_stockout_detection_summary_m12_03.json"
    report_file = repo_root / "documentation" / "07-ai" / "M12-03-stockout-detection.md"

    if not data_file.is_file():
        raise FileNotFoundError(
            f"Inventory dataset not found: {data_file}"
        )
    if not forecast_file.is_file():
        raise FileNotFoundError(f"M11-06 forecast output not found: {forecast_file}")

    inventory_df = pd.read_csv(data_file, dtype={"Store ID": str, "Product ID": str})
    forecast_df = pd.read_csv(forecast_file, dtype={"Store ID": str, "Product ID": str})
    detections = build_stockout_detections(inventory_df, forecast_df)
    if detections.empty:
        raise ValueError("No forecast rows were available for stockout detection.")

    output_dir.mkdir(parents=True, exist_ok=True)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    detections.to_csv(output_file, index=False)
    status_counts = {str(k): int(v) for k, v in detections["stockout_status"].value_counts().items()}
    summary = {
        "issue": "M12-03",
        "records_processed": int(len(detections)),
        "unique_store_product_pairs": int(detections[["Store ID", "Product ID"]].drop_duplicates().shape[0]),
        "date_start": str(detections["Date"].min()),
        "date_end": str(detections["Date"].max()),
        "status_counts": status_counts,
        "observed_stockout_count": int((detections["stockout_status"] == "STOCKOUT").sum()),
        "stockout_risk_count": int((detections["stockout_status"] == "STOCKOUT_RISK").sum()),
        "watch_count": int((detections["stockout_status"] == "WATCH").sum()),
        "output_file": output_file.relative_to(repo_root).as_posix(),
        "important_note": "Historical replay against date-aligned inventory and M11-06 model forecasts; not a live alert feed or a guarantee of future availability.",
    }
    summary_file.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    status_table = "\n".join(f"| {status} | {count:,} |" for status, count in sorted(status_counts.items()))
    report = f"""# M12-03 — Stockout Detection

## Purpose

Flag observed zero-stock records and identify positive-stock records whose demand-adjusted stock is at or below the M12-01 baseline reorder point. Results are advisory and do not guarantee future availability.

## Detection rules

- `STOCKOUT`: on-hand inventory is exactly zero, regardless of forecast availability.
- `STOCKOUT_RISK`: positive stock is at or below the baseline reorder point (lead time plus safety stock).
- `WATCH`: stock is above the reorder point but below target stock.
- `NO_STOCKOUT_RISK`: stock meets or exceeds target stock under the baseline assumptions.
- `DATA_REQUIRED`: inventory is missing, invalid or negative.
- `INSUFFICIENT_HISTORY`: stock is positive but neither a model forecast nor prior demand is available.

Demand defaults to a valid saved M11-06 model forecast. If missing, detection uses only the available prior seven days of observed demand for the same store-product series; it never uses future actual sales as a fallback. Negative demand is normalized to zero.

## Configured assumptions

| Setting | Value |
|---|---:|
| Supplier lead time | {DEFAULT_LEAD_TIME_DAYS} days |
| Review period | {DEFAULT_REVIEW_PERIOD_DAYS} day(s) |
| Safety stock buffer | {DEFAULT_SAFETY_STOCK_DAYS} day(s) of demand |

## Run summary

| Item | Result |
|---|---|
| Records processed | {summary['records_processed']:,} |
| Store-product pairs | {summary['unique_store_product_pairs']:,} |
| Date range | {summary['date_start']} to {summary['date_end']} |
| Observed stockouts | {summary['observed_stockout_count']:,} |
| Stockout-risk flags | {summary['stockout_risk_count']:,} |
| Watch flags | {summary['watch_count']:,} |

## Status counts

| Status | Records |
|---|---:|
{status_table}

## Output

- CSV: `python-ai/restocking/outputs/retail_stockout_detection_m12_03.csv`
- Summary: `python-ai/restocking/outputs/retail_stockout_detection_summary_m12_03.json`

## Reproduce

From the repository root, run:

```powershell
python .\\python-ai\\restocking\\stockout.py
```

**Scope note:** this is historical replay using inventory and forecasts aligned to dates in the M11-06 evaluation period. It is not a live current-stock monitoring service.
"""
    report_file.write_text(report, encoding="utf-8")
    print("Stockout detection completed successfully.")
    print(f"Records processed: {summary['records_processed']:,}")
    print(f"Date range: {summary['date_start']} to {summary['date_end']}")
    print(f"Observed stockouts: {summary['observed_stockout_count']:,}")
    print(f"Stockout-risk flags: {summary['stockout_risk_count']:,}")
    print(f"CSV: {output_file}")
    print(f"Summary: {summary_file}")
    print(f"Evidence report: {report_file}")
    print(summary["important_note"])


if __name__ == "__main__":
    main()
