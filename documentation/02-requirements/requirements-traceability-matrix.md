# M04-05: Requirements Traceability Matrix

## 1. Purpose

This matrix links the functional requirements of Retail-X-AI to the Python components responsible for implementing them.

## 2. Traceability Matrix

| Requirement ID | Functional Requirement | Related System Component |
|---|---|---|
| FR-01 | Load and Prepare Retail Data | CSV data loading and preparation |
| FR-02 | Analyse Historical Demand | Data analysis and feature engineering |
| FR-03 | Generate Demand Estimates | Ridge Regression forecasting and model evaluation |
| FR-04 | Analyse Inventory and Restocking Requirements | Restocking calculation component |
| FR-05 | Identify Potential Stockout Risks | Stockout detection component |
| FR-06 | Perform Additional AI-Based Retail Analysis | K-Means clustering, Isolation Forest and model comparison |
| FR-07 | Recommend Suppliers | Supplier recommendation component |
| FR-08 | Provide a Natural-Language Chatbot | Chatbot intent classification and conversation handlers |

## 3. Implementation Traceability

### FR-01: Load and Prepare Retail Data

The requirement is supported by the Python data-loading and preparation components responsible for reading and preparing the available retail dataset.

### FR-02: Analyse Historical Demand

The requirement is supported by the data analysis and feature engineering components that prepare historical retail information for analytical processing.

### FR-03: Generate Demand Estimates

The requirement is supported by the implemented Ridge Regression forecasting model and its evaluation results.

### FR-04: Analyse Inventory and Restocking Requirements

The requirement is supported by the restocking calculation component, which calculates suggested reorder quantities using configured assumptions.

### FR-05: Identify Potential Stockout Risks

The requirement is supported by the stockout detection component, which identifies potential risks using available inventory and demand information.

### FR-06: Perform Additional AI-Based Retail Analysis

The requirement is supported by the implemented clustering, anomaly detection and forecasting model comparison components.

### FR-07: Recommend Suppliers

The requirement is supported by the supplier recommendation component, which uses rule-based scoring based on configured supplier criteria.

### FR-08: Provide a Natural-Language Chatbot

The requirement is supported by the chatbot intent classifier and conversation handlers.

## 4. Scope and Data Limitations

The matrix reflects the implemented Python project.

The system does not include a graphical dashboard, live POS integration, live supplier integration, automatic purchasing or expiry-date monitoring.

Forecasting and restocking results must be interpreted according to the available dataset, model evaluation results and configured assumptions.

## 5. Conclusion

All eight functional requirements are linked to corresponding system components. This matrix provides traceability between the documented requirements and the implemented Retail-X-AI functionality.