# M04-04 — Use Case Specifications

## 1. Purpose

This document defines the main use cases for the Retail-X-AI system based on the approved functional requirements.

Retail-X-AI is an AI-powered inventory demand forecasting and smart restocking system for local spaza shops. The use cases describe how the Shop Owner / Manager interacts with the system to capture retail data, obtain demand forecasts, receive restocking recommendations, identify products requiring attention, use the AI assistant, and view inventory information.

The use cases provide a clear description of how users interact with Retail-X-AI and provide a basis for requirements traceability, system analysis, system design, and subsequent implementation.

## 2. Primary Actor

**Shop Owner / Manager / User**

The primary actor uses Retail-X-AI to manage and understand sales and inventory information and to support inventory, purchasing, and grocery-planning decisions.

## 3. Use Case Overview

| Use Case ID | Use Case | Related Requirement |
|---|---|---|
| UC-01 | Capture Sales and Stock Data | FR-01 |
| UC-02 | Generate Demand Forecast | FR-02 |
| UC-03 | Calculate Recommended Reorder Quantities | FR-03 |
| UC-04 | Identify Slow-Moving and Near-Expiry Products | FR-04 |
| UC-05 | Interact with Natural-Language AI Assistant | FR-05 |
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

Generate an estimate of future product demand using available historical sales data and relevant retail information.

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
2. Retail-X-AI retrieves relevant historical sales and inventory data.
3. The system prepares the data for forecasting.
4. The forecasting component analyses historical demand patterns.
5. The system generates a demand forecast.
6. The forecast is stored or made available for inventory decision support.
7. The forecast is presented to the user.

## Alternative / Exception Flows

- If insufficient historical data is available, the system informs the user that a reliable forecast cannot be generated.
- If data validation fails, the system requests corrected data.
- If forecasting fails, the system reports that the forecast could not be generated.

## Postconditions

- A demand forecast is generated when sufficient valid data is available.
- Forecast information is available to support inventory and purchasing decisions.

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
7. The user can use the recommendation to support a purchasing decision.

## Alternative / Exception Flows

- If current stock information is unavailable, the system requests updated stock information.
- If forecast information is unavailable, the system attempts to generate or retrieve the required forecast.
- If required replenishment information is unavailable, the system identifies the missing information and avoids presenting an unsupported recommendation.
- If supplier lead-time information is unavailable, the system must not assume a supplier lead time that has not been provided.

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

The user requests product-attention information or the system performs an analysis of products requiring attention.

## Preconditions

- Product and sales information is available.
- Where expiry monitoring is required, valid expiry information must be available to the system.

## Main Flow

1. The user opens the product-attention or alerts function.
2. Retail-X-AI analyses available product sales and inventory information.
3. The system identifies products with slow sales movement.
4. Where expiry information is available, the system checks products approaching expiry.
5. The system generates appropriate alerts.
6. The alerts are presented to the user.

## Alternative / Exception Flows

- If insufficient sales information is available, slow-moving analysis may not be possible.
- If expiry information is unavailable, expiry-based alerts cannot be generated.
- The system clearly distinguishes unavailable expiry information from products that are confirmed to be near expiry.
- The system must not identify a product as near expiry without valid expiry information.

## Postconditions

- Slow-moving products are identified where sufficient data is available.
- Near-expiry products are identified only where valid expiry information is available.
- Relevant alerts are presented to the user.

## Related Requirement

**FR-04 — Identify Slow-Moving and Near-Expiry Products**

---

# UC-05 — Interact with Natural-Language AI Assistant

## Goal

Allow the Shop Owner / Manager / User to interact with Retail-X-AI using natural language to obtain inventory information, sales insights, restocking guidance, product suggestions, grocery planning assistance, and purchasing decision support.

## Primary Actor

Shop Owner / Manager / User

## Trigger

The user submits a natural-language question, request, or planning task to the AI assistant.

## Preconditions

- The AI assistant is available.
- Relevant product, sales, inventory, forecast, recommendation, or pricing information is available where required.
- The user has access to the AI assistant.

## Main Flow

1. The user opens the AI assistant.
2. The user enters a natural-language question or request.
3. Retail-X-AI processes the user's request.
4. The system identifies the relevant information, task, or decision-support requirement.
5. The system retrieves available product, sales, inventory, forecast, recommendation, or pricing information where applicable.
6. The system generates a response based on the available information.
7. The AI assistant presents the response in understandable language.
8. The user can ask a follow-up question or refine the request.

## Supported Examples

The user may ask questions such as:

- "What is the current stock level?"
- "Which products are likely to have high demand?"
- "Which products should I reorder?"
- "What are my slow-moving products?"
- "Which products need attention?"
- "Create a grocery list for my household."
- "Help me plan my groceries for the week."
- "Suggest healthy food options for my grocery list."
- "I have R1,500. What groceries should I prioritise?"
- "Which products should I buy first within my budget?"
- "Compare these products and help me decide which one to purchase."

## Alternative / Exception Flows

- If the assistant cannot understand the request, it asks the user to rephrase or clarify the question.
- If required retail data is unavailable, the assistant explains that the requested information cannot currently be confirmed.
- If pricing or product information is unavailable, the assistant must not invent prices or product details.
- If the requested information is outside