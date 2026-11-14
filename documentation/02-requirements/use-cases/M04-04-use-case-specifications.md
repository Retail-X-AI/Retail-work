# M04-04: Use Case Specifications

## 1. Purpose

This document describes the main system use cases for Retail-X-AI. The use cases reflect the implemented Python components for retail data preparation, demand analysis, forecasting, inventory recommendations, supplier analysis and chatbot interaction.

## 2. System Users

The system is designed to support shop owners and managers through its analytical outputs and chatbot functionality.

The current implementation processes available retail data through Python components. It does not provide a graphical dashboard or browser-based interface.

## 3. Use Case Overview

| Use Case ID | Use Case | Related Requirement |
|---|---|---|
| UC-01 | Load and Prepare Retail Data | FR-01 |
| UC-02 | Analyse Historical Demand | FR-02 |
| UC-03 | Generate Demand Estimates | FR-03 |
| UC-04 | Analyse Inventory and Restocking Requirements | FR-04 |
| UC-05 | Identify Potential Stockout Risks | FR-05 |
| UC-06 | Perform Additional AI-Based Retail Analysis | FR-06 |
| UC-07 | Recommend Suppliers | FR-07 |
| UC-08 | Interact with Natural-Language Chatbot | FR-08 |

---

## UC-01: Load and Prepare Retail Data

**Goal**

Load and prepare the available retail dataset for analysis and model processing.

**System Input**

Available retail CSV dataset.

**Main Flow**

1. The data-loading component locates the available dataset.
2. The system reads the dataset.
3. The system processes the available columns and records.
4. Data preparation and cleaning operations are performed.
5. Prepared data becomes available to the analytical components.

**Alternative Flows**

- If the dataset cannot be located, the loading process reports the problem.
- If required columns are missing, the system handles the unsuitable input appropriately.
- Missing or invalid values are handled according to the implemented preparation logic.

**Postcondition**

The available retail data is prepared for subsequent analysis.

**Related Requirement:** FR-01.

---

## UC-02: Analyse Historical Demand

**Goal**

Analyse historical retail demand using the available sales information.

**Main Flow**

1. The system accesses the prepared retail dataset.
2. Historical sales information is examined.
3. Relevant demand-related features are prepared.
4. Historical patterns are made available for forecasting and inventory analysis.

**Alternative Flows**

- If required historical information is unavailable, the system cannot perform the affected analysis.
- Unsuitable data is handled according to the implemented preparation logic.

**Postcondition**

Historical demand information is available for further analytical processing.

**Related Requirement:** FR-02.

---

## UC-03: Generate Demand Estimates

**Goal**

Generate demand estimates using the implemented forecasting model.

**Main Flow**

1. The forecasting component receives prepared historical data.
2. The system processes the required forecasting features.
3. Ridge Regression generates demand estimates.
4. The model is evaluated using historical test data.
5. Applicable evaluation metrics are calculated.
6. Forecasting results are made available for analysis.

**Alternative Flows**

- If required data is unavailable, forecasting cannot proceed for the affected records.
- If model processing fails, the system reports the failure.
- Historical predictions are not presented as confirmed future demand.

**Postcondition**

Demand estimates and applicable model evaluation results are produced.

**Related Requirement:** FR-03.

---

## UC-04: Analyse Inventory and Restocking Requirements

**Goal**

Calculate suggested reorder quantities using the implemented replenishment logic.

**Main Flow**

1. The restocking component receives the available inventory and demand information.
2. The system applies the configured replenishment assumptions.
3. Suggested reorder quantities are calculated.
4. Restocking statuses are assigned.
5. Recommendations are made available for inventory decision support.

**Alternative Flows**

- If required information is unavailable, the system identifies the limitation.
- If configured assumptions are used, they are distinguished from verified supplier information.
- Recommendations are not treated as completed purchase orders.

**Postcondition**

Restocking calculations and recommendations are produced using the implemented method.

**Related Requirement:** FR-04.

---

## UC-05: Identify Potential Stockout Risks

**Goal**

Identify potential stockout risks using available retail information.

**Main Flow**

1. The stockout detection component receives the available data.
2. The system processes relevant inventory and demand information.
3. Potential stockout risks are identified.
4. Risk statuses are generated.
5. Results are made available for analysis.

**Alternative Flows**

- If required inventory information is unavailable, the system identifies the limitation.
- A risk flag is not treated as proof that an actual stockout occurred.

**Postcondition**

Potential stockout-risk results are generated.

**Related Requirement:** FR-05.

---

## UC-06: Perform Additional AI-Based Retail Analysis

**Goal**

Perform additional machine learning analysis on the available retail dataset.

**Main Flow**

1. The system prepares the required analytical data.
2. K-Means clustering groups records according to the implemented features.
3. Isolation Forest identifies unusual data patterns.
4. Forecasting models are compared using applicable evaluation metrics.
5. Analytical results are made available for interpretation.

**Alternative Flows**

- If the required input data is unsuitable, the affected analysis cannot proceed.
- Model results are interpreted according to their evaluation metrics and limitations.

**Postcondition**

Additional machine learning analysis results are produced.

**Related Requirement:** FR-06.

---

## UC-07: Recommend Suppliers

**Goal**

Generate supplier recommendations using the implemented rule-based scoring method.

**Main Flow**

1. The supplier recommendation component receives the available supplier information.
2. The system evaluates the configured supplier criteria.
3. Lead time, minimum order quantity and supply frequency are considered.
4. Supplier scores are calculated using the implemented weighting method.
5. Recommendations are generated for comparison.

**Alternative Flows**

- If supplier information is incomplete, the system handles the missing information according to the implemented logic.
- Recommendation scores are treated as comparative scores, not probabilities.
- Recommendations do not represent confirmed supplier orders.

**Postcondition**

Supplier recommendations are generated using the available information.

**Related Requirement:** FR-07.

---

## UC-08: Interact with Natural-Language Chatbot

**Goal**

Allow users to submit natural-language requests supported by the implemented Python chatbot.

**Primary Actor**

Shop Owner / Manager / User.

**Trigger**

The user submits a supported text request to the chatbot.

**Main Flow**

1. The user submits a text request.
2. The chatbot processes the request.
3. The intent classifier identifies the supported intent.
4. The relevant conversation handler processes the request.
5. The chatbot generates a response.
6. The response is returned to the user.

**Alternative Flows**

- If the request cannot be classified, the chatbot handles the unsupported intent.
- If required information is unavailable, the chatbot must not invent a response.
- Requests outside the implemented functionality are not treated as supported capabilities.

**Postcondition**

The chatbot returns a response for supported requests.

**Related Requirement:** FR-08.

---

## 4. Implementation Boundaries

The use cases describe the implemented Python-based system. They do not imply the existence of:

- A graphical dashboard or browser-based interface.
- Live POS integration.
- Live supplier integration.
- Automatic purchasing.
- Live inventory synchronisation.
- Implemented expiry-date monitoring.

## 5. Conclusion

The eight use cases correspond to the eight functional requirements of Retail-X-AI. They describe the main data-processing, analytical, machine learning, recommendation and chatbot functions within the current project scope.