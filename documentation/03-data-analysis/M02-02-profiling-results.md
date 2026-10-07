# M02-02 — Dataset Profiling Results

**Issue:** M02-02  
**Analyst:** Khanyisile Skhulile  
**Generated:** 2026-10-01 01:31  
**Source file:** `dataset/raw/retail_store_inventory.csv`

---

## 1. Shape

- **Rows:** 73,100
- **Columns:** 15

## 2. Columns and Data Types

| # | Column | Dtype | Non-Null | Null | Unique |
|---|--------|-------|----------|------|--------|
| 1 | `Date` | str | 73,100 | 0 | 731 |
| 2 | `Store ID` | str | 73,100 | 0 | 5 |
| 3 | `Product ID` | str | 73,100 | 0 | 20 |
| 4 | `Category` | str | 73,100 | 0 | 5 |
| 5 | `Region` | str | 73,100 | 0 | 4 |
| 6 | `Inventory Level` | int64 | 73,100 | 0 | 451 |
| 7 | `Units Sold` | int64 | 73,100 | 0 | 498 |
| 8 | `Units Ordered` | int64 | 73,100 | 0 | 181 |
| 9 | `Demand Forecast` | float64 | 73,100 | 0 | 31,608 |
| 10 | `Price` | float64 | 73,100 | 0 | 8,999 |
| 11 | `Discount` | int64 | 73,100 | 0 | 5 |
| 12 | `Weather Condition` | str | 73,100 | 0 | 4 |
| 13 | `Holiday/Promotion` | int64 | 73,100 | 0 | 2 |
| 14 | `Competitor Pricing` | float64 | 73,100 | 0 | 9,751 |
| 15 | `Seasonality` | str | 73,100 | 0 | 4 |

## 3. Date Range

- **Column:** `Date`
- **Earliest:** 2022-01-01 00:00:00
- **Latest:** 2024-01-01 00:00:00
- **Span:** 730 days

## 4. Categorical Breakdowns

- **Store ID** (5 unique): ['S001', 'S002', 'S003', 'S004', 'S005']
- **Product ID** (20 unique): ['P0001', 'P0002', 'P0003', 'P0004', 'P0005', 'P0006', 'P0007', 'P0008', 'P0009', 'P0010', 'P0011', 'P0012', 'P0013', 'P0014', 'P0015', 'P0016', 'P0017', 'P0018', 'P0019', 'P0020']
- **Category** (5 unique): ['Clothing', 'Electronics', 'Furniture', 'Groceries', 'Toys']
- **Region** (4 unique): ['East', 'North', 'South', 'West']

## 5. Missing Values

No missing values detected.

## 6. Numeric Summary

| Column | Min | Max | Mean | Std |
|--------|-----|-----|------|-----|
| `Inventory Level` | 50.00 | 500.00 | 274.47 | 129.95 |
| `Units Sold` | 0.00 | 499.00 | 136.46 | 108.92 |
| `Units Ordered` | 20.00 | 200.00 | 110.00 | 52.28 |
| `Demand Forecast` | -9.99 | 518.55 | 141.49 | 109.25 |
| `Price` | 10.00 | 100.00 | 55.14 | 26.02 |
| `Discount` | 0.00 | 20.00 | 10.01 | 7.08 |
| `Holiday/Promotion` | 0.00 | 1.00 | 0.50 | 0.50 |
| `Competitor Pricing` | 5.03 | 104.94 | 55.15 | 26.19 |

## 7. Negative-Value Check

- **`Demand Forecast`** has **673** negative values.

## 8. Duplicate Rows

- **Exact duplicate rows:** 0

## 9. First 5 Rows

```
         Date Store ID Product ID     Category Region  Inventory Level  Units Sold  Units Ordered  Demand Forecast  Price  Discount Weather Condition  Holiday/Promotion  Competitor Pricing Seasonality
0  2022-01-01     S001      P0001    Groceries  North              231         127             55           135.47  33.50        20             Rainy                  0               29.69      Autumn
1  2022-01-01     S001      P0002         Toys  South              204         150             66           144.04  63.01        20             Sunny                  0               66.16      Autumn
2  2022-01-01     S001      P0003         Toys   West              102          65             51            74.02  27.99        10             Sunny                  1               31.32      Summer
3  2022-01-01     S001      P0004         Toys  North              469          61            164            62.18  32.72        10            Cloudy                  1               34.74      Autumn
4  2022-01-01     S001      P0005  Electronics   East              166          14            135             9.26  73.64         0             Sunny                  0               68.95      Summer
```
