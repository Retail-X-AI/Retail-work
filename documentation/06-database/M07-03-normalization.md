# M07-03 — Normalize Database Design

**Issue ID:** M07-03
**Milestone:** M07 — Database Design
**Assignee:** @KhanyisileSkhulile614
**Dependency:** M07-02 (ERD)
**Repository Location:** `documentation/06-database/`

---

## 1. Objective

Normalize the Retail-X-AI database schema to **Third Normal Form (3NF)** to:

- Eliminate data redundancy
- Remove partial and transitive dependencies
- Ensure data integrity
- Provide evidence-based normalization documentation

---

## 2. Source Data

The normalization was performed using the dataset:

- `retail_store_inventory.csv` (sample of Retail-X-AI inventory and sales data)
- ERD from M07-02

### Unnormalized (UNF) Flat Table Structure

| Date | Store ID | Product ID | Category | Region | Inventory Level | Units Sold | Units Ordered | Demand Forecast | Price | Discount | Weather Condition | Holiday/Promotion | Competitor Pricing | Seasonality |
|------|----------|------------|----------|--------|-----------------|------------|---------------|-----------------|-------|----------|-------------------|-------------------|--------------------|-------------|

### Problems Identified in UNF

1. **Repeating groups** — `Category` and `Region` repeat on every row.
2. **Redundant data** — same category/region stored many times.
3. **Mixed concerns** — descriptive attributes (Category, Region, Season) mixed with transactional facts.
4. **No separation** of dimensions (store, product, date) and facts (sales, inventory).

---

## 3. Normalization Steps

### 3.1 First Normal Form (1NF)

**Rule:** All attributes must be atomic; no repeating groups.

**Action:**
- Ensured each attribute holds a single value.
- Defined the fact table at the grain: **one row per (Date, Store, Product)**.
- Introduced a surrogate key `Record_ID` for the fact table.

**Result:**  1NF achieved.

---

### 3.2 Second Normal Form (2NF)

**Rule:** No partial dependencies on a composite key.

Composite key on the fact table: `(Date_ID, Store_ID, Product_ID)`

**Partial dependencies removed:**

| Partial Dependency | Moved To |
|--------------------|----------|
| `Store_ID → Store_Name` | `STORE` |
| `Product_ID → Product_Name, Unit_Price, Discount, Category_ID` | `PRODUCT` |
| `Date_ID → Full_Date, Day, Month, Year, Season` | `DATE_DIM` |

**Result:**  2NF achieved.

---

### 3.3 Third Normal Form (3NF)

**Rule:** No transitive dependencies (non-key → non-key).

**Transitive dependencies removed:**

| Transitive Dependency | Moved To |
|------------------------|----------|
| `Product_ID → Category_ID → Category_Name` | `CATEGORY` (Category_Name moved here) |
| `Store_ID → Region_ID → Region_Name` | `REGION` (Region_Name moved here) |

**Justified denormalization (documented exception):**

- `DATE_DIM` keeps `Day, Month, Year, Season` as derived attributes for analytics performance. This is a **controlled denormalization** for reporting/forecasting use cases.

**Result:**  3NF achieved.

---

## 4. Functional Dependency Analysis

| Table | Functional Dependencies |
|-------|--------------------------|
| CATEGORY | `Category_ID → Category_Name` |
| REGION | `Region_ID → Region_Name` |
| STORE | `Store_ID → Store_Name, Region_ID` |
| PRODUCT | `Product_ID → Product_Name, Unit_Price, Discount, Category_ID` |
| DATE_DIM | `Date_ID → Full_Date, Day, Month, Year, Season` |
| INVENTORY_RECORD | `Record_ID → Date_ID, Store_ID, Product_ID, Inventory_Level, Units_Sold, Units_Ordered, Demand_Forecast, Competitor_Pricing, Weather_Condition, Holiday_Promotion, Seasonality` |

---

## 5. Final Normalized Schema (3NF)

```mermaid
erDiagram
    CATEGORY {
        int Category_ID PK
        string Category_Name
    }
    REGION {
        int Region_ID PK
        string Region_Name
    }
    STORE {
        string Store_ID PK
        int Region_ID FK
        string Store_Name
    }
    PRODUCT {
        string Product_ID PK
        int Category_ID FK
        string Product_Name
        decimal Unit_Price
        decimal Discount
    }
    DATE_DIM {
        int Date_ID PK
        date Full_Date
        int Day
        int Month
        int Year
        string Season
    }
    INVENTORY_RECORD {
        int Record_ID PK
        int Date_ID FK
        string Store_ID FK
        string Product_ID FK
        int Inventory_Level
        int Units_Sold
        int Units_Ordered
        decimal Demand_Forecast
        decimal Competitor_Pricing
        string Weather_Condition
        boolean Holiday_Promotion
        string Seasonality
    }

    REGION ||--|{ STORE : contains
    CATEGORY ||--|{ PRODUCT : categorizes
    STORE ||--|{ INVENTORY_RECORD : records
    PRODUCT ||--|{ INVENTORY_RECORD : recorded_in
    DATE_DIM ||--|{ INVENTORY_RECORD : occurs_on