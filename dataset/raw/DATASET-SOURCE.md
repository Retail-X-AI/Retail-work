# Dataset Source

**Issue:** M02-01
**Milestone:** M02 — Dataset & Data Understanding
**Analyst:** Khanyisile Skhulile
**Date:** 2026-09-22

---

## Source Information

- **Name:** Retail Store Inventory and Demand Forecasting
- **Source:** Kaggle
- **URL:** https://www.kaggle.com/datasets/atomicd/retail-store-inventory-and-demand-forecasting
- **Author:** Wavelet (Kaggle user: atomicd)
- **Published:** 2025-05-21
- **License:** Apache 2.0
- **Downloaded on:** 2026-09-22

---

## Notes About Our Version

The dataset was provided by the project team. Our copy
(`retail_store_inventory.csv`) is based on this Kaggle source with
the following differences:

1. Column renamed: `Demand` → `Demand Forecast`
2. Column renamed: `Promotion` → `Holiday/Promotion`
3. Column removed: `Epidemic` (present in the Kaggle version)
4. Original Kaggle file was named `sales_data.csv`

These modifications were made by the team to simplify the dataset
for the Retail-X-AI system.

---

## Description

Synthetic daily retail inventory and sales records across 5 stores,
20 products, and multiple product categories, spanning 2022.

The Kaggle page states: *"This dataset was synthetically generated
and may not reflect real-world data."* — We are aware of this and
will note it in our AI documentation.

---

## Columns

| Column | Type | Description |
|--------|------|-------------|
| Date | Date | Transaction date |
| Store ID | String | Store identifier (S001–S005) |
| Product ID | String | Product identifier (P0001–P0020) |
| Category | String | Product category |
| Region | String | Store region |
| Inventory Level | Integer | Stock on hand |
| Units Sold | Integer | Units sold that day |
| Units Ordered | Integer | Units restocked |
| Demand Forecast | Float | Expected demand |
| Price | Float | Product price |
| Discount | Integer | Discount % |
| Weather Condition | String | Weather |
| Holiday/Promotion | Binary | 0 = no, 1 = yes |
| Competitor Pricing | Float | Competitor's price |
| Seasonality | String | Season |

---

## Files

- `retail_store_inventory.csv` — raw dataset (team-modified version)
- `DATASET-SOURCE.md` — this file
