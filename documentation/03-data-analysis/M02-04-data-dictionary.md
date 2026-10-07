# M02-04 - Data Dictionary

**Issue:** M02-04  
**Analyst:** Khanyisile Skhulile  
**Generated:** 2026-10-01 21:08  
**Source file:** `dataset/raw/retail_store_inventory.csv`

---

## Overview

- **Rows:** 73,100
- **Columns:** 15
- **Granularity:** one row per (Date, Store ID, Product ID)

---

## Column Definitions

### `Date`

- **Meaning:** Date of the record (daily granularity).
- **Units / Format:** YYYY-MM-DD
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 731
- **Sample values:** ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']
- **Notes:** Covers 2022-01-01 to 2022-09-30.

### `Store ID`

- **Meaning:** Unique identifier for the retail store.
- **Units / Format:** S001 - S005
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 5
- **Sample values:** ['S001', 'S002', 'S003', 'S004', 'S005']
- **Notes:** 5 stores total.

### `Product ID`

- **Meaning:** Unique identifier for the product.
- **Units / Format:** P0001 - P0020
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 20
- **Sample values:** ['P0001', 'P0002', 'P0003', 'P0004', 'P0005']
- **Notes:** 20 products total.

### `Category`

- **Meaning:** Product category.
- **Units / Format:** text
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 5
- **Sample values:** ['Groceries', 'Toys', 'Electronics', 'Furniture', 'Clothing']
- **Notes:** Groceries, Toys, Electronics, Furniture, Clothing.

### `Region`

- **Meaning:** Geographic region of the store.
- **Units / Format:** text
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 4
- **Sample values:** ['North', 'South', 'West', 'East']
- **Notes:** North, South, East, West.

### `Inventory Level`

- **Meaning:** Stock on hand at the start of the day.
- **Units / Format:** units
- **Data type:** int64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 451
- **Range:** 50.00 to 500.00
- **Mean / Std:** 274.47 / 129.95
- **Notes:** Non-negative.

### `Units Sold`

- **Meaning:** Number of units sold that day.
- **Units / Format:** units
- **Data type:** int64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 498
- **Range:** 0.00 to 499.00
- **Mean / Std:** 136.46 / 108.92
- **Notes:** Non-negative.

### `Units Ordered`

- **Meaning:** Number of units ordered from the supplier that day.
- **Units / Format:** units
- **Data type:** int64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 181
- **Range:** 20.00 to 200.00
- **Mean / Std:** 110.00 / 52.28
- **Notes:** Non-negative.

### `Demand Forecast`

- **Meaning:** Forecasted demand for that day.
- **Units / Format:** units
- **Data type:** float64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 31,608
- **Range:** -9.99 to 518.55
- **Mean / Std:** 141.49 / 109.25
- **Notes:** WARNING: contains negative values (673 rows). Needs cleaning.

### `Price`

- **Meaning:** Selling price per unit.
- **Units / Format:** currency
- **Data type:** float64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 8,999
- **Range:** 10.00 to 100.00
- **Mean / Std:** 55.14 / 26.02
- **Notes:** Positive.

### `Discount`

- **Meaning:** Discount applied to the price.
- **Units / Format:** 0-1 (fraction) or percentage
- **Data type:** int64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 5
- **Range:** 0.00 to 20.00
- **Mean / Std:** 10.01 / 7.08
- **Notes:** 0 means no discount.

### `Weather Condition`

- **Meaning:** Weather on the day of the record.
- **Units / Format:** text
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 4
- **Sample values:** ['Rainy', 'Sunny', 'Cloudy', 'Snowy']
- **Notes:** e.g. Sunny, Rainy, Cloudy.

### `Holiday/Promotion`

- **Meaning:** Whether the day was a holiday or promotion day.
- **Units / Format:** 0 or 1
- **Data type:** int64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 2
- **Range:** 0.00 to 1.00
- **Mean / Std:** 0.50 / 0.50
- **Notes:** Kaggle source called this column 'Promotion'.

### `Competitor Pricing`

- **Meaning:** Competitor's price for the same product.
- **Units / Format:** currency
- **Data type:** float64
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 9,751
- **Range:** 5.03 to 104.94
- **Mean / Std:** 55.15 / 26.19
- **Notes:** Positive.

### `Seasonality`

- **Meaning:** Season of the year.
- **Units / Format:** text
- **Data type:** str
- **Non-null count:** 73,100 / 73,100
- **Unique values:** 4
- **Sample values:** ['Autumn', 'Summer', 'Winter', 'Spring']
- **Notes:** Spring, Summer, Autumn, Winter.

---

## Column Summary Table

| # | Column | Type | Unique | Missing | Meaning |
|---|--------|------|--------|---------|---------|
| 1 | `Date` | str | 731 | 0 | Date of the record (daily granularity). |
| 2 | `Store ID` | str | 5 | 0 | Unique identifier for the retail store. |
| 3 | `Product ID` | str | 20 | 0 | Unique identifier for the product. |
| 4 | `Category` | str | 5 | 0 | Product category. |
| 5 | `Region` | str | 4 | 0 | Geographic region of the store. |
| 6 | `Inventory Level` | int64 | 451 | 0 | Stock on hand at the start of the day. |
| 7 | `Units Sold` | int64 | 498 | 0 | Number of units sold that day. |
| 8 | `Units Ordered` | int64 | 181 | 0 | Number of units ordered from the supplier that day. |
| 9 | `Demand Forecast` | float64 | 31,608 | 0 | Forecasted demand for that day. |
| 10 | `Price` | float64 | 8,999 | 0 | Selling price per unit. |
| 11 | `Discount` | int64 | 5 | 0 | Discount applied to the price. |
| 12 | `Weather Condition` | str | 4 | 0 | Weather on the day of the record. |
| 13 | `Holiday/Promotion` | int64 | 2 | 0 | Whether the day was a holiday or promotion day. |
| 14 | `Competitor Pricing` | float64 | 9,751 | 0 | Competitor's price for the same product. |
| 15 | `Seasonality` | str | 4 | 0 | Season of the year. |

---

## Notes and Caveats

- `Demand Forecast` contains 673 negative values that should be cleaned before modelling.
- The dataset is **synthetic** (per the Kaggle source documented in `DATASET-SOURCE.md`).
- `Holiday/Promotion` may correspond to the 'Promotion' column in the Kaggle source.
- Granularity: one row per store per product per day.
