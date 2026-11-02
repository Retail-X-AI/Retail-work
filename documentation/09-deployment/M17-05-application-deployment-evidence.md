# M17-05 - Application and Deployment Evidence

**Issue:** #91
**Milestone:** M17 - Documentation & Evidence
**Date:** 2 November 2026
**Project:** Retail-X-AI

## 1. Purpose

This document consolidates the deployment documentation and validation evidence for Retail-X-AI. It references the completed M16-03 and M16-04 work without duplicating their detailed reports.

## 2. Deployment Scope

Deployment was performed and validated in a local Windows environment.

Application startup command: `python -m streamlit run app.py`

Local address: http://localhost:8501

No cloud hosting, public production URL, SSL deployment or production release pipeline was tested.

## 3. Deployment Documentation

The following documents provide supporting deployment evidence:

1. `deployment/documentation/M16-03-deployment-guide.md` - Local Windows deployment procedure.
2. `documentation/09-deployment/M16-03-deployment-evidence.md` - M16-03 supporting evidence.
3. `deployment/M16-04-deployment-validation.md` - M16-04 validation summary.
4. `testing/results/M16-04-deployment-validation-results.md` - Detailed M16-04 results.
5. `documentation/08-testing/M17-05-application-testing-evidence.md` - Consolidated application and testing evidence.

## 4. Deployment Verification

| Verification | Result |
|---|---|
| Local Streamlit startup | PASS |
| Dashboard browser access | PASS |
| Sales Analysis | PASS |
| AI Forecasting | PASS |
| Smart Restocking | PASS |
| Inventory Alerts | PASS |
| AI Chatbot | PASS |
| Model Performance | PASS |
| Python application compilation | PASS |
| Python dependency check | PASS |
| SQLite integrity check | PASS |

## 5. Database Evidence

The SQLite database was inspected using a read-only connection.

Results:
- Database file exists.
- Integrity check returned `ok`.
- Two database tables were present.
- 73,100 inventory records were present.
- Five stores and twenty products were present.
- Zero foreign key violations were reported.

Screenshot:
`documentation/08-testing/results/M16-04-SQLite-Database-Verification.png`

## 6. Application Behaviour and Limitations

The application was visually checked across all seven pages.

Store filtering was tested using S004, S005 and All Stores. The Dashboard, Sales Analysis, AI Forecasting, Smart Restocking and Inventory Alerts responded to store selection.

The Model Performance page did not respond to the global store filter. This limitation is documented in the M16-04 validation results.

The chatbot returned historical advisory recommendations dated 1 January 2024. These are not live purchase orders or current purchasing instructions.

The AI output audit reported that all historical reorder records were classified as `REORDER_NOW` and all stockout records as `STOCKOUT_RISK`. These distributions require review before operational use.

The Model Performance dashboard displayed MAE 87.18 and RMSE 106.06 for its dashboard-labelled Random Forest metrics, and MAE 8.26 and RMSE 9.96 for Dataset Forecast. These values come from `retailai_model_evaluation.csv`.

They are separate from the canonical Ridge Regression temporal holdout results documented in `documentation/07-ai/M17-04-ai-model-evidence.md` (MAE 88.453325 and RMSE 107.996727 across 11,000 test records). The provenance and calculation differences have not been reconciled. The figures must not be treated as interchangeable or combined. The dashboard values are recorded here only as observed application output.


## 7. Supporting Test Evidence

Refer to:
- `documentation/08-testing/M17-05-application-testing-evidence.md`
- `testing/results/M15-02-functional-test-results.md`
- `testing/results/M15-03-ai-validation-report.md`
- `testing/results/M15-06-performance-integration-results.md`
- `testing/results/M16-04-deployment-validation-results.md`

The detailed testing report records 108 passing tests, one skipped test and 37 passing chatbot subtests across individually executed test groups.

The combined pytest collection issue is also documented.

## 8. Final Deployment Assessment

The local deployment procedure is documented and the Streamlit application was successfully launched and manually inspected.

The database verification and application checks passed.

Known application, AI-output and automated test limitations are retained in the supporting evidence.

This index does not claim a cloud or production deployment.

**Issue:** M17-05 (#91)
**Evidence status:** Prepared for final review.
