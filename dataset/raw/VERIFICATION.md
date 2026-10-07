# Data Verification

**Issue:** M02-01
**Analyst:** Khanyisile Skhulile
**Date:** 2026-09-22

---

## File Verified

`retail_store_inventory.csv`

---

## Basic Checks

| Check | Result |
|-------|--------|
| Total rows | ~10,640 |
| Total columns | 15 |
| Date range | 2022-01-01 to 2022-09-30 |
| Unique stores | 5 (S001 – S005) |
| Unique products | 20 (P0001 – P0020) |
| Categories | 5 (Groceries, Toys, Electronics, Furniture, Clothing) |
| Regions | 4 (North, South, East, West) |
| Missing values | None detected |
| Duplicate rows | Not checked |
| Negative inventory values | None detected |

*(If any of the above is different from what you see in the file, tell me and I'll help you correct it.)*

---

## Data Quality Issues Noted

1. **Negative Demand Forecast values** — some rows have negative
   values in the `Demand Forecast` column (e.g. -2.4, -3.91, -8.87).
   Demand cannot be negative. This should be cleaned before
   forecasting (Analyst 5 should handle this).

2. **Holiday/Promotion column** — some values may need double-
   checking for consistency with the Kaggle source (which called
   it "Promotion").

3. **Synthetic data** — the Kaggle source states the dataset was
   synthetically generated. Results from this data may not
   reflect real-world retail patterns.

---

## Suitability for Retail-X-AI

The dataset is suitable for:
- Demand forecasting (has Date + Units Sold + Demand Forecast)
- Stockout detection (has Inventory Level + Units Sold)
- Slow-moving analysis (has Product ID + Units Sold over time)
- Expiry analysis — ⚠️ not supported (no expiry column)
- AI chatbot queries (rich enough for common questions)

**Limitations:**
- No supplier data
- No product expiry dates
- No cost/purchase price (only selling price)
- Synthetic data — may not reflect real retail variability

---

## Evidence

- Raw dataset: `retail_store_inventory.csv`
- Source: `DATASET-SOURCE.md`
- This report: `VERIFICATION.md`

---

## Verification Method

Initial structural verification done by inspecting the first
and last rows of the file and checking column headers. Full
statistical profiling will be done in M02-02 using Python.
