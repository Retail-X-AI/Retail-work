# M02-05 - Forecasting Target and Leakage Analysis

**Issue:** M02-05  
**Analyst:** Khanyisile Skhulile  
**Generated:** 2026-10-02 22:37  
**Source file:** `dataset/raw/retail_store_inventory.csv`

---

## 1. Recommended Forecasting Target

**Target column:** `Units Sold`

**Reason:** `Units Sold` is the concrete, observable quantity we want to forecast at daily (Store, Product) granularity. It represents what actually happened at the till - which is what 'demand' means in a retail context. It has no negative values and its distribution is realistic.

### Target column statistics

- **Type:** int64
- **Non-null:** 73,100 / 73,100
- **Min:** 0.00
- **Max:** 499.00
- **Mean:** 136.46
- **Std:** 108.92
- **Negative values:** 0

## 2. Leakage Risk Columns

These columns must **NOT** be used as inputs when predicting the target:

### `Demand Forecast` (present in dataset: yes)

Direct derivative of the target. If we predict Units Sold, Demand Forecast already encodes the answer. Including it as an input would be pure data leakage. Also currently contains 673 negative values, so it is not yet reliable as a target either.

### `Units Ordered` (present in dataset: yes)

Reflects post-sale restocking decisions. Often causally downstream of Units Sold - you order more because you sold more. Using it as an input would leak the outcome.

### `Inventory Level` (present in dataset: yes)

End-of-day stock is affected by how many units were sold. If the level is measured at end of day, it contains post-sale information - a mild leakage risk. Only safe to use if measured at the start of the day before any sales.

## 3. Safe Feature Columns

The following columns are safe to use as model inputs because their values are known **before** the day's sales occur:

- `Date` (present: yes)
- `Store ID` (present: yes)
- `Product ID` (present: yes)
- `Category` (present: yes)
- `Region` (present: yes)
- `Price` (present: yes)
- `Discount` (present: yes)
- `Competitor Pricing` (present: yes)
- `Weather Condition` (present: yes)
- `Holiday/Promotion` (present: yes)
- `Seasonality` (present: yes)

## 4. Correlation of Numeric Columns with the Target

| Column | Correlation with target |
|--------|------------------------|
| `Demand Forecast` | 0.9969 |
| `Inventory Level` | 0.5900 |
| `Discount` | 0.0026 |
| `Competitor Pricing` | 0.0013 |
| `Price` | 0.0011 |
| `Units Ordered` | -0.0009 |
| `Holiday/Promotion` | -0.0004 |

High correlation with the target is a **warning sign** for potential leakage - investigate any column that correlates very strongly with `Units Sold` before using it as a feature.

## 5. Summary and Recommendation

- **Forecasting target:** `Units Sold`
- **Excluded (leakage risk):** `Demand Forecast`, `Units Ordered`, `Inventory Level`
- **Safe input features:** `Date`, `Store ID`, `Product ID`, `Category`, `Region`, `Price`, `Discount`, `Competitor Pricing`, `Weather Condition`, `Holiday/Promotion`, `Seasonality`

### Notes
- `Demand Forecast` cannot be used as a feature OR as a target in its current state - it has 673 negative values.
- `Inventory Level` is only safe if measured at start-of-day.
- Time-based train/test split must be used (no random splitting), to avoid leaking future information into the training set.