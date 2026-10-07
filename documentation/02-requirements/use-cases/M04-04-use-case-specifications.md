# M04-04 — Use Case Specifications

## 1. Purpose

This document defines the main use cases for the Retail-X-AI system based on the approved functional requirements.

Retail-X-AI is an AI-powered inventory demand forecasting and smart restocking system for local spaza shops. The use cases describe how the Shop Owner / Manager interacts with the system to capture retail data, obtain forecasts, receive restocking recommendations, identify products requiring attention, use the AI assistant, and view inventory information.

## 2. Primary Actor

**Shop Owner / Manager / User**

The primary actor uses Retail-X-AI to manage and understand sales and inventory information and to support inventory decisions.

## 3. Use Case Overview

| Use Case ID | Use Case | Related Requirement |
|---|---|---|
| UC-01 | Capture Sales and Stock Data | FR-01 |
| UC-02 | Generate Demand Forecast | FR-02 |
| UC-03 | Calculate Recommended Reorder Quantities | FR-03 |
| UC-04 | Identify Slow-Moving and Near-Expiry Products | FR-04 |
| UC-05 | Interact with Natural-Language Chatbot | FR-05 |
| UC-06 | View Interactive Dashboard | FR-06 |

---

# UC-01 — Capture Sales and Stock Data

## Goal

Allow the Shop Owner / Manager / User to provide sales and stock information to Retail-X-AI for storage, analysis, forecasting, and inventory management.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user needs to add or update retail sales and stock information.

## Preconditions

- Retail-X-AI is available.
- The user has access to the data input function.
- Data is available through CSV, manual entry, or a supported POS export.

## Main Flow

1. The user opens the data capture function.
2. The user selects a supported input method.
3. The user provides sales and stock data.
4. Retail-X-AI validates the supplied data.
5. The system stores the valid data.
6. The system confirms successful data capture.
7. The captured data becomes available for analysis and forecasting.

## Alternative / Exception Flows

- If required data is missing, the system identifies the invalid or incomplete information.
- If the supplied file has an unsupported format, the system informs the user.
- If validation fails, the system does not process the invalid records until the issue is corrected.

## Postconditions

- Valid sales and stock data is stored.
- The data is available for subsequent analysis and forecasting.

## Related Requirement

**FR-01 — Capture Sales and Stock Data**

---

# UC-02 — Generate Demand Forecast

## Goal

Generate an estimate of future product demand using available historical sales data.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user requests a demand forecast or the system processes available data for forecasting.

## Preconditions

- Historical sales data is available.
- The data required for forecasting has been validated.
- The forecasting process is available.

## Main Flow

1. The user selects a product, product category, or forecasting view.
2. Retail-X-AI retrieves relevant historical sales data.
3. The system prepares the data for forecasting.
4. The forecasting component analyses historical demand patterns.
5. The system generates a demand forecast.
6. The forecast is presented to the user.

## Alternative / Exception Flows

- If insufficient historical data is available, the system informs the user that a reliable forecast cannot be generated.
- If data validation fails, the system requests corrected data.
- If forecasting fails, the system reports that the forecast could not be generated.

## Postconditions

- A demand forecast is generated when sufficient valid data is available.
- Forecast information is available to support inventory decisions.

## Related Requirement

**FR-02 — Generate Demand Forecasts**

---

# UC-03 — Calculate Recommended Reorder Quantities

## Goal

Provide a recommended quantity to reorder based on forecasted demand and current inventory information.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user requests a restocking recommendation or the system identifies a need for replenishment.

## Preconditions

- Product information is available.
- Current stock information is available.
- Forecast information is available or can be generated.
- Any required additional replenishment information is available.

## Main Flow

1. The user selects a product or reviews a restocking recommendation.
2. Retail-X-AI retrieves the relevant stock level.
3. The system retrieves or generates the expected demand.
4. The system evaluates the available replenishment information.
5. The system calculates a recommended reorder quantity.
6. The recommendation is presented to the user.

## Alternative / Exception Flows

- If current stock information is unavailable, the system requests updated stock information.
- If forecast information is unavailable, the system attempts to generate or retrieve the required forecast.
- If required replenishment information is unavailable, the system identifies the missing information and avoids presenting an unsupported recommendation.

## Postconditions

- A reorder recommendation is produced when sufficient information is available.
- The recommendation can be used by the user to support purchasing decisions.

## Related Requirement

**FR-03 — Calculate Recommended Reorder Quantities**

---

# UC-04 — Identify Slow-Moving and Near-Expiry Products

## Goal

Identify products that require attention because they have low sales movement or are approaching expiry.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user requests product attention information or the system performs an analysis of products requiring attention.

## Preconditions

- Product and sales information is available.
- Where expiry monitoring is required, valid expiry information must be available to the system.

## Main Flow

1. The user opens the product attention or alerts function.
2. Retail-X-AI analyses available product sales and inventory information.
3. The system identifies products with slow sales movement.
4. Where expiry information is available, the system checks products approaching expiry.
5. The system generates appropriate alerts.
6. The alerts are presented to the user.

## Alternative / Exception Flows

- If insufficient sales information is available, slow-moving analysis may not be possible.
- If expiry information is unavailable, expiry-based alerts cannot be generated.
- The system clearly distinguishes unavailable expiry information from products that are confirmed to be near expiry.

## Postconditions

- Slow-moving products are identified where sufficient data is available.
- Near-expiry products are identified only where valid expiry information is available.
- Relevant alerts are presented to the user.

## Related Requirement

**FR-04 — Identify Slow-Moving and Near-Expiry Products**

---

# UC-05 — Interact with Natural-Language Chatbot

## Goal

Allow the Shop Owner / Manager / User to ask questions about inventory and sales information using natural language.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user submits a question or request to the AI chatbot.

## Preconditions

- The chatbot is available.
- Relevant retail information is available to the system.

## Main Flow

1. The user opens the AI assistant.
2. The user enters a natural-language question.
3. Retail-X-AI processes the user's request.
4. The system identifies the relevant information or function.
5. The system retrieves or calculates the required information.
6. The chatbot provides a response in understandable language.

## Example Queries

- "What is the current stock level?"
- "Which products are likely to have high demand?"
- "Which products should I reorder?"
- "What are my slow-moving products?"
- "Which products need attention?"

## Alternative / Exception Flows

- If the chatbot cannot understand the request, it asks the user to rephrase the question.
- If required data is unavailable, the chatbot explains that the information cannot currently be provided.
- If a request is outside the supported system functions, the chatbot informs the user.

## Postconditions

- The user receives an understandable response where the required information is available.
- The interaction may provide information needed for inventory decision-making.

## Related Requirement

**FR-05 — Provide a Natural-Language Chatbot**

---

# UC-06 — View Interactive Dashboard

## Goal

Allow the Shop Owner / Manager / User to view important sales, inventory, forecasting, recommendation, and alert information in one interface.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user opens the Retail-X-AI dashboard.

## Preconditions

- The system is available.
- Relevant sales, inventory, forecasting, or recommendation information is available.

## Main Flow

1. The user opens the dashboard.
2. Retail-X-AI retrieves the available relevant information.
3. The dashboard displays sales trends.
4. The dashboard displays current stock levels.
5. The dashboard displays demand predictions.
6. The dashboard displays reorder recommendations.
7. The dashboard displays relevant stock alerts.
8. The user reviews the information to support inventory decisions.

## Alternative / Exception Flows

- If a data source is unavailable, the dashboard indicates that the affected information is unavailable.
- If no forecast is available, the forecast section displays an appropriate unavailable state.
- If no alerts are currently applicable, the dashboard indicates that there are no current alerts.

## Postconditions

- The user can view relevant retail information.
- The displayed information supports inventory management and purchasing decisions.

## Related Requirement

**FR-06 — Display an Interactive Dashboard**

---

# 4. Use Case Relationships

The use cases support the Retail-X-AI workflow:

**UC-01 Capture Sales and Stock Data**  
→ provides data for  
**UC-02 Generate Demand Forecast**  
→ supports  
**UC-03 Calculate Recommended Reorder Quantities**

Sales and inventory analysis also supports:

**UC-04 Identify Slow-Moving and Near-Expiry Products**

The outputs from these functions can be presented through:

**UC-06 View Interactive Dashboard**

The user can also access relevant information through:

**UC-05 Interact with Natural-Language Chatbot**

## 5. Traceability Summary

| Functional Requirement | Use Case |
|---|---|
| FR-01 | UC-01 |
| FR-02 | UC-02 |
| FR-03 | UC-03 |
| FR-04 | UC-04 |
| FR-05 | UC-05 |
| FR-06 | UC-06 |

## 6. Data Limitation Note

The current Retail-X-AI team dataset contains sales, inventory, product, pricing, discount, weather, holiday/promotion, competitor pricing, and seasonality information.

It does **not** directly contain supplier lead-time or product-expiry-date fields.

Therefore:

- FR-03 identifies supplier lead time as a business input that may require additional data or user input.
- FR-04 identifies expiry monitoring as a system requirement, but expiry-based analysis requires expiry information that is not present in the current dataset.
- The system must not represent unavailable expiry or supplier information as if it were present in the current dataset.

This distinction will be considered during subsequent system design, database design, and implementation.

## 7. Verification

The six use cases were derived from the six functional requirements documented in the Retail-X-AI requirements specification.

Each functional requirement has a corresponding use case, providing a direct basis for requirements traceability in M04-05.