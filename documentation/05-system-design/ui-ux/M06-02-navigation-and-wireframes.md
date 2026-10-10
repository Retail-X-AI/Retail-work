# M06-02 — Navigation and Wireframe Specification

## 1. Purpose
Define the proposed navigation structure and low-fidelity screen layouts for Retail-X-AI. These are design artefacts for review, not a claim that the application has already been implemented.

## 2. Intended user
The primary user is the Shop Owner / Manager. The interface should make everyday stock management and inventory decisions understandable without requiring technical knowledge.

## 3. Screen inventory

| Screen ID | Screen | Main purpose | Related use case |
|---|---|---|---|
| UI-01 | Dashboard | Overview of inventory, forecast availability, recommendations, and alerts | UC-06 |
| UI-02 | Data Capture | Enter stock and sales data manually or import a supported file | UC-01 |
| UI-03 | Demand Forecasts | Select a product/category and inspect available forecasts | UC-02 |
| UI-04 | Restocking | Review reorder recommendations and their data basis | UC-03 |
| UI-05 | Product Alerts | Review slow-moving products and verified expiry alerts | UC-04 |
| UI-06 | AI Assistant | Ask inventory, forecasting, restocking, and grocery-planning questions | UC-05 |

## 4. Shared layout
The proposed desktop layout uses:
- A top bar containing the Retail-X-AI identity and current page title.
- A persistent left navigation menu.
- A central content area with clear headings and grouped information.
- Status messages near the information or action they describe.
- A consistent return path through the main navigation.

Responsive behaviour, authentication screens, and mobile-specific layouts require further design decisions and are not asserted by these desktop wireframes.

## 5. Screen requirements

### UI-01 — Dashboard
Show an overview of available inventory information, forecast summaries, reorder items, and product alerts. Any summary metric must come from real available data. When data has not been supplied or calculated, display an explicit empty state such as “No data available yet” rather than sample values that could be mistaken for real shop data.

Primary actions: Capture Data, View Forecasts, Review Restocking, View Alerts, Ask AI Assistant.

### UI-02 — Data Capture
Offer manual entry and file import for supported CSV or POS-export data. Show the selected method, required fields, validation feedback, and a confirmation after successful saving. Unsupported formats and incomplete records must be explained. Invalid records must not be presented as successfully saved.

### UI-03 — Demand Forecasts
Allow selection of a product or category and show the forecast only when sufficient validated historical data is available. Clearly label the forecast period and units when those details are available. If data is insufficient or forecasting fails, explain the issue and provide a route back to data capture.

### UI-04 — Restocking
Show product, current stock, forecast/demand basis, and recommended reorder quantity when each value is available. Identify missing information. Do not assume supplier lead times or show an unsupported recommendation.

### UI-05 — Product Alerts
Separate slow-moving alerts from expiry alerts. Only show near-expiry status when valid expiry information is available. If expiry data is unavailable, say it cannot be confirmed; do not imply the product is safe or near expiry.

### UI-06 — AI Assistant
Provide a conversation history area, a text input, and a send action. Suggested prompts may include “Which products should I reorder?” and “What is my current stock level?” Responses must be grounded in available data. If prices, stock, or other requested information are unavailable, the assistant must say so. Support follow-up questions and clarification when a request is ambiguous.

## 6. Navigation and interaction rules
1. The Dashboard is the central entry point to the main functions.
2. Each main screen remains reachable from persistent navigation.
3. A successful data save returns the user to a useful next step or offers a return to the Dashboard.
4. Validation errors keep the user in the relevant workflow so they can correct the data.
5. Missing data is an explicit state, not a fabricated value.
6. A forecast may lead to Restocking, but a recommendation is only displayed when its required information is available.
7. The AI Assistant supports follow-up questions without forcing the user to restart the conversation.

## 7. Traceability
- UC-01 → UI-02
- UC-02 → UI-03
- UC-03 → UI-04
- UC-04 → UI-05
- UC-05 → UI-06
- UC-06 → UI-01

## 8. Artefacts
- Navigation flow: `diagrams/ui-ux/M06-02-navigation-flow.md`
- Visual wireframes: `diagrams/ui-ux/M06-02-wireframes.svg`
- This specification: `documentation/05-system-design/ui-ux/M06-02-navigation-and-wireframes.md`

## 9. Verification checklist
- [ ] All six approved use cases map to a screen.
- [ ] Main navigation links all six functions.
- [ ] Data validation and correction paths are represented.
- [ ] Forecast and restocking empty/error states are documented.
- [ ] Expiry alerts require valid expiry data.
- [ ] AI responses do not invent unavailable prices or inventory facts.
- [ ] SVG opens in a browser and its text and layout are legible.
- [ ] The diagrams render in GitHub.
