# M17-05 - Application and Testing Evidence

**Issue:** #91
**Milestone:** M17 - Documentation & Evidence
**Date:** 2 November 2026
**Repository:** Retail-X-AI

## 1. Purpose

This document consolidates the application and testing evidence for Retail-X-AI. It references previously completed testing milestones and records the results of the M16-04 deployment validation.

It does not replace the original test plan or the detailed milestone reports.

## 2. Test Environment

| Component | Verified environment |
|---|---|
| Operating system | Windows |
| Python | 3.11.9 |
| Streamlit | 1.63.0 |
| Pytest | 9.2.0 |
| Database | SQLite |
| Application entry point | app.py |
| Local application URL | http://localhost:8501 |

Pytest was installed into the active virtual environment for testing. It was not added to requirements.txt.

## 3. Manual Application Testing

All seven application pages were opened and visually inspected in a browser.

| Page | Validation performed | Result |
|---|---|---|
| Dashboard | Business overview, figures, alerts and sales trend | PASS |
| Sales Analysis | Sales metrics, product selector and sales trend | PASS |
| AI Forecasting | Forecast records, error metrics and actual-versus-forecast chart | PASS |
| Smart Restocking | Recommendation table, order quantities and urgent items | PASS |
| Inventory Alerts | Severity filters, alert table and active alerts | PASS |
| AI Chatbot | Interface and an inventory question were tested | PASS |
| Model Performance | Model metrics, product comparison and error chart | PASS |

## 4. Store Filter Testing

The global Store Filter was tested with S004, S005 and All Stores.

Results:
- S004 updated Dashboard, Sales Analysis, AI Forecasting, Smart Restocking and Inventory Alerts.
- S005 updated the Dashboard figures.
- All Stores restored the overall Dashboard figures.
- S004 Active Alerts showed records belonging to S004.

**Known limitation:** Model Performance did not change when the global store filter was changed. Its metrics and product comparison remained unchanged.

## 5. Key Manual Results

### Dashboard - All Stores

| Metric | Result |
|---|---:|
| Stores | 5 |
| Products | 20 |
| Units sold | 9,975,582 |
| Estimated revenue | R550,228,884.91 |
| Critical alerts | 6 |
| High alerts | 17 |
| Medium alerts | 31 |
| Low alerts | 10 |

### Dashboard - S004

| Metric | Result |
|---|---:|
| Stores | 1 |
| Products | 20 |
| Units sold | 1,979,245 |
| Estimated revenue | R108,947,413.59 |

### Dashboard - S005

| Metric | Result |
|---|---:|
| Stores | 1 |
| Products | 20 |
| Units sold | 2,010,176 |
| Estimated revenue | R111,713,826.32 |

### Smart Restocking - All Stores

- Items to restock: 100
- Units to order: 26,189
- Urgent items: 23

### Smart Restocking - S004

- Items to restock: 20
- Units to order: 5,723
- Urgent items: 8

### AI Forecasting

The forecasting page displayed 110 records for the selected store and product.

For the S004/P0001 selection:
- MAE: 92.14 units
- RMSE: 113.68 units

The page identifies the displayed predictions as rolling one-step-ahead historical holdout predictions, not a new seven-day future forecast.

### AI Chatbot

The chatbot processed:

"What should S004 reorder?"

It returned five historical advisory recommendations dated 1 January 2024. No purchase order was created.

These recommendations must not be interpreted as live purchasing instructions.

### Model Performance

The dashboard displayed the following overall metrics, sourced from the root-level `retailai_model_evaluation.csv` file:

- Dashboard-labelled Random Forest MAE: 87.18
- Dashboard-labelled Random Forest RMSE: 106.06
- Dataset Forecast MAE: 8.26
- Dataset Forecast RMSE: 9.96

The dashboard displays the `Our_Model_MAE` and `Our_Model_RMSE` columns under the labels Random Forest MAE and Random Forest RMSE, respectively.

**Important distinction from the canonical model evaluation:** The M17-04 AI evidence documents the Ridge Regression temporal holdout evaluation with MAE 88.453325 and RMSE 107.996727 across 11,000 test records. These are separate evaluation outputs. The provenance and calculation differences between the dashboard CSV metrics and the canonical Ridge holdout metrics have not yet been reconciled. They must not be treated as interchangeable or combined.

For the canonical model evaluation, refer to `documentation/07-ai/M17-04-ai-model-evidence.md`. The figures above are recorded only as the metrics displayed by the application during manual testing.

The store-filter limitation is recorded in Section 4.

## 6. Automated Test Execution

The following test groups were executed individually.

| Test group | Passed | Skipped |
|---|---:|---:|
| Restocking integration | 2 | 0 |
| M15-06 integration | 4 | 0 |
| M15-06 performance | 3 | 0 |
| Dashboard functional | 2 | 0 |
| Database service | 5 | 0 |
| Chatbot tests | 55 | 1 |
| M15-03 AI validation | 6 | 0 |
| Reorder recommendations | 8 | 0 |
| Restocking scenarios | 9 | 0 |
| Stockout detection | 14 | 0 |
| **Total** | **108** | **1** |

The chatbot test run additionally reported 37 passing subtests.

### Full-suite collection limitation

The command:

`python -m pytest -q`

encountered three test collection errors involving conflicting Python imports of the module name `recommendations`.

The affected test groups passed when run individually. The combined collection conflict remains unresolved and should be addressed in future test maintenance.

## 7. Database Verification

The database verification screenshot is saved at:

`documentation/08-testing/results/M16-04-SQLite-Database-Verification.png`

The read-only SQLite verification recorded:

| Check | Result |
|---|---:|
| Database file exists | True |
| Integrity check | ok |
| Database tables | 2 |
| Inventory records | 73,100 |
| Stores | 5 |
| Products | 20 |
| Foreign key violations | 0 |

The duplicate SQL statement discovered during M16-04 was removed from database/sqlite_schema.sql. The database tests passed again after the correction.

## 8. AI Output Audit

The saved AI output validation returned:

**PASS_WITH_WARNINGS**

The audit confirmed valid schemas, numeric values, dates, forecast metrics, unique keys, record alignment and consistency with saved metadata.

Two warnings remain:
- 100% of historical reorder records were classified as REORDER_NOW.
- 100% of historical stockout records were classified as STOCKOUT_RISK.

These historical output distributions require review before operational use.

The detailed AI validation evidence remains available in the existing M15-03 reports and M17-04 AI/model evidence.

## 9. Original Test Plan Coverage

The original M15-01 test cases are assessed below using the evidence collected.

| Test ID | Feature | Evidence status |
|---|---|---|
| TC01 | Product Management | Not verified |
| TC02 | Inventory updates | Not verified as a separate update operation |
| TC03 | Sales Recording | Not verified |
| TC04 | Demand Forecasting | Partially verified |
| TC05 | Low Stock Alerts | Verified through displayed alerts and related tests |
| TC06 | Restocking | Verified through recommendation pages and automated tests |
| TC07 | Expiry Monitoring | Not verified |
| TC08 | Slow Moving Products | Not verified |
| TC09 | Dashboard | Verified |
| TC10 | AI Chatbot | Verified, with historical-response limitation |
| TC11 | Data Validation | Partially verified through database tests |
| TC12 | Security | Not verified |

Not-tested items are explicitly identified rather than being marked as passed.

## 10. Existing Supporting Evidence

The following reports are retained and referenced:

- `testing/results/M15-02-functional-test-results.md`
- `testing/results/M15-03-ai-validation-report.md`
- `testing/results/M15-03-ai-validation-results.json`
- `testing/results/M15-06-performance-integration-results.md`
- `testing/results/M16-04-deployment-validation-results.md`
- `testing/results/m15-04_test_results.png`
- `documentation/08-testing/results/M16-04-SQLite-Database-Verification.png`
- `documentation/07-ai/M17-04-ai-model-evidence.md`

## 11. Final Assessment

The Retail-X-AI application was successfully launched locally and all seven application pages were visually inspected.

A total of 108 automated tests passed, one was skipped, and 37 chatbot subtests passed across the individually executed test groups.

Known limitations, skipped tests, incomplete original test-plan cases and AI output warnings have been documented.

This evidence demonstrates the checks actually performed. It does not claim that every original test case passed or that the application has been deployed to a production or cloud environment.

**Issue:** M17-05 (#91)
**Evidence status:** Prepared for final review.
