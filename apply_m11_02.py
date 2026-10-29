"""Apply M11-02 leakage-safe demand-history features to RetailAI.

Run this script from the root of the Retail-work repository:
    python apply_m11_02.py

It changes only feature_engineering.py and creates the M11-02 test/report files.
It refuses to overwrite a file that already contains the M11-02 features.
"""
from pathlib import Path

ROOT = Path.cwd()
FEATURE_FILE = ROOT / "python-ai" / "forecasting" / "feature_engineering.py"
TEST_FILE = ROOT / "python-ai" / "tests" / "test_feature_engineering.py"
REPORT_FILE = ROOT / "python-ai" / "forecasting" / "M11-02-feature-engineering-results.md"

if not FEATURE_FILE.is_file():
    raise SystemExit(
        "Could not find python-ai/forecasting/feature_engineering.py. "
        "Run this script from the Retail-work repository root."
    )

source = FEATURE_FILE.read_text(encoding="utf-8")
if "DEMAND_HISTORY_COLUMNS" in source or "demand_rolling_mean_28" in source:
    raise SystemExit(
        "M11-02 demand-history features already appear to exist. "
        "No files were changed. Inspect the file before proceeding."
    )

constant_anchor = 'TARGET_COLUMN = "Units Sold"\n'
if source.count(constant_anchor) != 1:
    raise SystemExit("Could not safely find the TARGET_COLUMN declaration; no changes made.")

source = source.replace(
    constant_anchor,
    constant_anchor
    + '\nGROUP_COLUMNS = ["Store ID", "Product ID"]\n'
    + 'DEMAND_HISTORY_COLUMNS = [\n'
    + '    "demand_lag_1",\n'
    + '    "demand_lag_7",\n'
    + '    "demand_lag_14",\n'
    + '    "demand_rolling_mean_7",\n'
    + '    "demand_rolling_mean_28",\n'
    + ']\n',
    1,
)

required_anchor = "REQUIRED_COLUMNS = [\n"
helper = '''def add_demand_history_features(df):
    """Add past-demand features without using the current or future target.

    Rolling features use the previous observations for each store-product
    series. They are intended for rolling one-step-ahead forecasting, where
    prior observed demand is available when the next prediction is made.
    """

    data = df.sort_values(
        ["Store ID", "Product ID", "Date"], kind="stable"
    ).copy()
    history = data.groupby(GROUP_COLUMNS, sort=False)[TARGET_COLUMN]

    data["demand_lag_1"] = history.shift(1)
    data["demand_lag_7"] = history.shift(7)
    data["demand_lag_14"] = history.shift(14)

    for window in (7, 28):
        column = f"demand_rolling_mean_{window}"
        data[column] = history.transform(
            lambda values: values.shift(1).rolling(
                window=window, min_periods=1
            ).mean()
        )

    # Restore chronological order for the split logic that follows.
    return data.sort_values(
        ["Date", "Store ID", "Product ID"], kind="stable"
    ).reset_index(drop=True)


'''
if source.count(required_anchor) != 1:
    raise SystemExit("Could not safely find REQUIRED_COLUMNS; no changes made.")
source = source.replace(required_anchor, helper + required_anchor, 1)

sort_anchor = '''    data = data.sort_values(
        ["Date", "Store ID", "Product ID"]
    ).reset_index(drop=True)
'''
if source.count(sort_anchor) != 1:
    raise SystemExit("Could not safely find the chronological sort; no changes made.")
source = source.replace(
    sort_anchor,
    sort_anchor + '\n    # Build lag/rolling features from earlier observations only.\n'
    '    data = add_demand_history_features(data)\n',
    1,
)

numeric_anchor = "    numeric_features = NUMERIC_COLUMNS + calendar_columns\n"
if source.count(numeric_anchor) != 1:
    raise SystemExit("Could not safely find numeric feature assembly; no changes made.")
source = source.replace(
    numeric_anchor,
    "    numeric_features = NUMERIC_COLUMNS + DEMAND_HISTORY_COLUMNS + calendar_columns\n",
    1,
)

metadata_anchor = '        "target_column": TARGET_COLUMN,\n'
if source.count(metadata_anchor) != 1:
    raise SystemExit("Could not safely find metadata target field; no changes made.")
source = source.replace(
    metadata_anchor,
    metadata_anchor + '        "demand_history_columns": DEMAND_HISTORY_COLUMNS,\n',
    1,
)

# Create an executable regression suite. Existing files are never overwritten.
TEST_FILE.parent.mkdir(parents=True, exist_ok=True)
if TEST_FILE.exists():
    raise SystemExit(
        f"{TEST_FILE.relative_to(ROOT)} already exists. No files were changed; "
        "review it before deciding how to add M11-02 tests."
    )
if REPORT_FILE.exists():
    raise SystemExit(
        f"{REPORT_FILE.relative_to(ROOT)} already exists. No files were changed; "
        "review it before deciding how to add M11-02 evidence."
    )

test_source = r'''"""Regression tests for M11-02 demand-history feature engineering."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

FORECASTING_DIR = Path(__file__).resolve().parents[1] / "forecasting"
sys.path.insert(0, str(FORECASTING_DIR))

from feature_engineering import (  # noqa: E402
    DEMAND_HISTORY_COLUMNS,
    add_demand_history_features,
    prepare_forecasting_data,
    prepare_forecasting_train_validation_test,
)


def sample_data(days=40):
    rows = []
    dates = pd.date_range("2024-01-01", periods=days, freq="D")
    for day, date in enumerate(dates):
        for store, base in (("S1", 0), ("S2", 100)):
            rows.append({
                "Date": date,
                "Store ID": store,
                "Product ID": "P1",
                "Category": "Grocery",
                "Region": "North",
                "Weather Condition": "Sunny",
                "Seasonality": "Regular",
                "Price": 10.0,
                "Discount": 0.0,
                "Competitor Pricing": 10.5,
                "Holiday/Promotion": 0,
                "Units Sold": base + day + 1,
                "Demand Forecast": 9999,
                "Units Ordered": 8888,
                "Inventory Level": 7777,
            })
    return pd.DataFrame(rows)


class DemandHistoryFeatureTests(unittest.TestCase):
    def test_lags_and_rolling_means_use_prior_observations(self):
        result = add_demand_history_features(sample_data())
        row = result.loc[
            (result["Store ID"] == "S1")
            & (result["Product ID"] == "P1")
            & (result["Date"] == pd.Timestamp("2024-01-21"))
        ].iloc[0]
        self.assertEqual(row["Units Sold"], 21)
        self.assertEqual(row["demand_lag_1"], 20)
        self.assertEqual(row["demand_lag_7"], 14)
        self.assertEqual(row["demand_lag_14"], 7)
        self.assertAlmostEqual(row["demand_rolling_mean_7"], 17.0)
        self.assertAlmostEqual(row["demand_rolling_mean_28"], 10.5)

    def test_demand_history_does_not_mix_store_product_series(self):
        result = add_demand_history_features(sample_data())
        row = result.loc[
            (result["Store ID"] == "S2")
            & (result["Product ID"] == "P1")
            & (result["Date"] == pd.Timestamp("2024-01-21"))
        ].iloc[0]
        self.assertEqual(row["demand_lag_1"], 120)
        self.assertAlmostEqual(row["demand_rolling_mean_7"], 117.0)

    def test_current_target_does_not_change_its_own_history_features(self):
        original = sample_data()
        changed = original.copy()
        target = (
            (changed["Store ID"] == "S1")
            & (changed["Date"] == pd.Timestamp("2024-01-21"))
        )
        changed.loc[target, "Units Sold"] += 5000
        before = add_demand_history_features(original)
        after = add_demand_history_features(changed)
        key = (
            (before["Store ID"] == "S1")
            & (before["Date"] == pd.Timestamp("2024-01-21"))
        )
        for column in DEMAND_HISTORY_COLUMNS:
            self.assertEqual(before.loc[key, column].iloc[0], after.loc[key, column].iloc[0])

    def test_prepared_features_are_numeric_finite_and_exclude_leakage_columns(self):
        train, test, prepared, metadata = prepare_forecasting_data(
            sample_data(), train_fraction=0.7
        )
        self.assertTrue((train["Date"].max() < test["Date"].min()))
        self.assertTrue(set(DEMAND_HISTORY_COLUMNS).issubset(metadata["feature_columns"]))
        self.assertFalse({"Demand Forecast", "Units Ordered", "Inventory Level"}.intersection(prepared.columns))
        numeric = prepared.drop(columns=["Date", "Units Sold"])
        self.assertTrue(np.isfinite(numeric.to_numpy(dtype=float)).all())

    def test_three_way_split_is_chronological(self):
        train, validation, test, prepared, metadata = (
            prepare_forecasting_train_validation_test(
                sample_data(), train_fraction=0.7, validation_fraction=0.15
            )
        )
        self.assertLess(train["Date"].max(), validation["Date"].min())
        self.assertLess(validation["Date"].max(), test["Date"].min())
        self.assertEqual(len(prepared), len(sample_data()))
        self.assertEqual(
            len(train) + len(validation) + len(test), len(sample_data())
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''

report = '''# M11-02 — Forecasting Feature Engineering Evidence

## Objective

Extend the existing M10-03 feature preparation with leakage-safe historical demand features for each store-product series.

## Features added

- `demand_lag_1`: previous observed demand
- `demand_lag_7`: demand seven observations earlier
- `demand_lag_14`: demand fourteen observations earlier
- `demand_rolling_mean_7`: mean of up to the previous seven observations
- `demand_rolling_mean_28`: mean of up to the previous twenty-eight observations

Every lag and rolling mean is shifted so the current row's `Units Sold` value is not used to construct that row's history features. Features are calculated independently for each store-product pair. Missing initial history is imputed using medians calculated from the training period only. Existing chronological split logic and one-hot category alignment are retained. `Demand Forecast`, `Units Ordered`, and `Inventory Level` remain excluded from model features.

## Verification

Run from the repository root:

```bash
python -m unittest discover -s python-ai/tests -p "test_feature_engineering.py" -v
python -m py_compile python-ai/forecasting/feature_engineering.py python-ai/tests/test_feature_engineering.py
```

The regression tests cover lag and rolling calculations, separation between store-product series, current-target leakage, finite prepared features, excluded columns, and chronological three-way splitting. Record the actual test output in the pull request before merging.

## Forecasting assumption

Lag features support rolling one-step-ahead forecasting: prior observed demand is available when each next-day prediction is made. A multi-day forecast made all at once must instead recursively feed predictions into later lag features or use a horizon-specific strategy.
'''

# All safety checks have passed; write only the intended files.
FEATURE_FILE.write_text(source, encoding="utf-8")
TEST_FILE.write_text(test_source, encoding="utf-8")
REPORT_FILE.write_text(report, encoding="utf-8")
print("Updated python-ai/forecasting/feature_engineering.py")
print("Created python-ai/tests/test_feature_engineering.py")
print("Created python-ai/forecasting/M11-02-feature-engineering-results.md")
print("Next: run the test and compile commands printed in the evidence report.")
