\# M02-06 — Dataset Limitations and Assumptions



\*\*Issue:\*\* M02-06

\*\*Analyst:\*\* Khanyisile Skhulile

\*\*Date:\*\* 2026-10-02

\*\*Source file:\*\* `dataset/raw/retail\_store\_inventory.csv`

\*\*Depends on:\*\* M02-01, M02-02, M02-03, M02-04, M02-05



\---



\## Purpose



This document records the \*\*known limitations\*\* of the raw retail

inventory dataset and the \*\*assumptions\*\* the Retail-X-AI team is

making when using it. Recording these honestly protects the project

from overstating results and helps reviewers and future analysts

interpret findings correctly.



\---



\## 1. Dataset Overview (Recap)



\- \*\*Source:\*\* Kaggle — synthetic retail store inventory dataset

\- \*\*Rows:\*\* \~73,100

\- \*\*Columns:\*\* 15

\- \*\*Date range:\*\* 2022-01-01 → 2022-09-30 (9 months)

\- \*\*Stores:\*\* 5 (S001 – S005)

\- \*\*Products:\*\* 20 (P0001 – P0020)

\- \*\*Categories:\*\* 5 (Groceries, Toys, Electronics, Furniture, Clothing)

\- \*\*Regions:\*\* 4 (North, South, East, West)

\- \*\*Granularity:\*\* one row per (Date, Store ID, Product ID)



See `DATASET-SOURCE.md` (M02-01) and `M02-02-profiling-results.md` for details.



\---



\## 2. Limitations



\### 2.1 Data Origin



\- \*\*Synthetic data.\*\* The dataset was generated, not collected from a

&#x20; real retailer. Statistical patterns may be artificially clean and

&#x20; may not reflect the noise, seasonality, or irregularity of real

&#x20; retail operations.

\- \*\*No real-world anomalies.\*\* Events like supplier strikes, system

&#x20; outages, or sudden demand shocks are unlikely to be present.



\### 2.2 Scope



\- \*\*Only 9 months of history.\*\* No year-over-year comparison is

&#x20; possible, and long-term seasonality cannot be established.

\- \*\*Only 5 stores.\*\* Too few for regional or store-level modelling

&#x20; that generalises.

\- \*\*Only 20 products.\*\* Too few for category-level or SKU-level deep

&#x20; learning approaches.

\- \*\*No supplier, warehouse, or logistics data.\*\* Supply-chain

&#x20; analysis is out of scope.



\### 2.3 Field-Level Limitations



\- \*\*No product expiry dates.\*\* Expiry analysis (a listed use case)

&#x20; is \*\*not supported\*\* by this dataset.

\- \*\*No cost / purchase price.\*\* Only selling price is present, so

&#x20; gross margin and profitability analyses are impossible.

\- \*\*`Demand Forecast` contains 673 negative values.\*\* Demand cannot

&#x20; be negative; this column is currently unusable as either a feature

&#x20; or a target until cleaned (see M02-03, M02-05).

\- \*\*`Holiday/Promotion` is binary.\*\* The dataset does not distinguish

&#x20; between a holiday and a promotion — both are encoded as `1`.

\- \*\*`Inventory Level` granularity is unclear.\*\* If it represents

&#x20; end-of-day stock, it carries a mild leakage risk (see M02-05).



\### 2.4 Quality Limitations



\- \*\*No missing values.\*\* Confirmed by M02-03 — but on synthetic data,

&#x20; this "cleanliness" is suspicious rather than reassuring; real data

&#x20; almost always has gaps.

\- \*\*No duplicates.\*\* Confirmed by M02-03.



\---



\## 3. Assumptions



The following assumptions are being made by the Retail-X-AI team

when using this dataset. If any of these assumptions is later

invalidated, the affected analyses must be revisited.



\### 3.1 Data Integrity



\- The `Date` column is treated as \*\*accurate and complete\*\* for every row.

\- `Store ID` and `Product ID` are treated as \*\*stable identifiers\*\*

&#x20; that do not change meaning over time.

\- The synthetic data is assumed \*\*representative enough\*\* to

&#x20; demonstrate forecasting, stockout detection, and slow-moving

&#x20; analysis techniques — but \*\*not\*\* to make real business claims.



\### 3.2 Modelling



\- \*\*Forecasting target:\*\* `Units Sold` (see M02-05).

\- \*\*Leakage exclusions:\*\* `Demand Forecast`, `Units Ordered`, and

&#x20; `Inventory Level` are excluded as model inputs.

\- \*\*Time-based train/test split\*\* will be used (never random).

\- \*\*Daily granularity\*\* is sufficient for demand forecasting.

\- Negative `Demand Forecast` values will be cleaned in a later

&#x20; milestone before that column is used anywhere.



\### 3.3 Business Context



\- Prices are assumed to be in a \*\*single, unstated currency\*\*.

\- Discounts encoded as `0` mean \*\*no discount applied\*\*.

\- Weather is assumed to be \*\*recorded at the store's location\*\*, not

&#x20; a central region.

\- Store and product identifiers (`S001`, `P0001`) are treated as

&#x20; \*\*opaque\*\* — no external mapping is assumed.



\### 3.4 Scope



\- The dataset is assumed to represent the \*\*entire\*\* retail operation

&#x20; for the given period (no external stores or products missing).

\- There is assumed to be \*\*no hidden censoring\*\* — i.e. stockouts

&#x20; that prevented sales are not silently missing from `Units Sold`.



\---



\## 4. Impact on Downstream Work



| Area | Impact |

|------|--------|

| Demand forecasting | Possible, but on synthetic data — results are illustrative |

| Stockout detection | Possible — uses `Inventory Level` + `Units Sold` |

| Slow-moving SKU analysis | Possible — uses `Product ID` + `Units Sold` over time |

| Expiry analysis | ❌ Not supported — no expiry column |

| Profitability / margin | ❌ Not supported — no cost price |

| Supplier analysis | ❌ Not supported — no supplier data |

| Cross-year seasonality | ❌ Not supported — only 9 months of data |



\---



\## 5. Recommendations



1\. \*\*Flag this document\*\* in every downstream analysis that uses

&#x20;  the raw dataset.

2\. \*\*Clean `Demand Forecast`\*\* before any model that relies on it.

3\. \*\*Avoid real-world claims\*\* — frame findings as demonstrations

&#x20;  of method, not predictions for a real retailer.

4\. \*\*Revisit this document\*\* if the dataset is replaced or extended

&#x20;  with real data.

5\. \*\*Track assumptions in version control\*\* — any change to these

&#x20;  assumptions should be a new commit and ideally a new issue.



\---



\## 6. References



\- `dataset/raw/DATASET-SOURCE.md` — data source (M02-01)

\- `documentation/03-data-analysis/M02-02-profiling-results.md` — profile

\- `documentation/03-data-analysis/M02-03-data-quality-results.md` — quality

\- `documentation/03-data-analysis/M02-04-data-dictionary.md` — dictionary

\- `documentation/03-data-analysis/M02-05-target-and-leakage.md` — target \& leakage

