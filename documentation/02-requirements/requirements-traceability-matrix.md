# M04-05 — Requirements Traceability Matrix

## 1. Purpose

The Requirements Traceability Matrix (RTM) provides a clear link between the functional requirements of Retail-X-AI and the corresponding use cases and verification activities.

The matrix is used to confirm that each functional requirement has been documented, linked to a system function, and assigned a method for verification.

Retail-X-AI is an AI-powered inventory demand forecasting and smart restocking system designed for local spaza shops.

## 2. Traceability Matrix

| Requirement ID | Functional Requirement | Related Use Case | Verification Method | Evidence |
|---|---|---|---|---|
| FR-01 | Capture Sales and Stock Data | UC-01 — Capture Sales and Stock Data | Functional testing of CSV upload, manual entry and supported POS data input | UC-01 specification; input/data capture testing |
| FR-02 | Generate Demand Forecasts | UC-02 — Generate Demand Forecast | Test forecasting using historical sales data and verify that forecast results are presented to the user | UC-02 specification; forecasting test results |
| FR-03 | Calculate Recommended Reorder Quantities | UC-03 — Calculate Recommended Reorder Quantities | Test reorder calculations using forecasted demand and available stock information | UC-03 specification; reorder calculation testing |
| FR-04 | Identify Slow-Moving and Near-Expiry Products | UC-04 — Identify Slow-Moving and Near-Expiry Products | Test identification rules and verify that alerts are generated for products requiring attention | UC-04 specification; alert testing |
| FR-05 | Provide a Natural-Language Chatbot | UC-05 — Interact with Natural-Language Chatbot | Test natural-language questions and verify that understandable responses are returned | UC-05 specification; chatbot testing |
| FR-06 | Display an Interactive Dashboard | UC-06 — View Interactive Dashboard | Test dashboard display and verify that required sales, stock, forecast, reorder and alert information is shown | UC-06 specification; dashboard testing |

## 3. Detailed Traceability

### FR-01 — Capture Sales and Stock Data

**Requirement:**  
The system shall allow users to capture and store past sales and stock data through CSV uploads, manual data entry and simple POS data exports.

**Use Case:**  
UC-01 — Capture Sales and Stock Data

**Traceability:**  
FR-01 → UC-01 → Data capture and validation testing

**Verification:**  
The system will be tested to confirm that supported sales and stock data can be captured and stored correctly.

---

### FR-02 — Generate Demand Forecasts

**Requirement:**  
The system shall generate demand forecasts for individual products or product categories using available historical sales data.

**Use Case:**  
UC-02 — Generate Demand Forecast

**Traceability:**  
FR-02 → UC-02 → Forecast generation testing

**Verification:**  
The forecasting function will be tested using historical sales data to confirm that forecast results are generated and presented to the user.

---

### FR-03 — Calculate Recommended Reorder Quantities

**Requirement:**  
The system shall calculate recommended reorder quantities using forecasted demand, current stock levels and supplier lead time.

**Use Case:**  
UC-03 — Calculate Recommended Reorder Quantities

**Traceability:**  
FR-03 → UC-03 → Reorder calculation testing

**Verification:**  
The reorder recommendation process will be tested using available demand and stock information.

**Data limitation:**  
The current team dataset does not contain a supplier lead-time field. Supplier lead time must therefore be provided through additional system input or another approved data source if it is required for the implemented reorder calculation.

---

### FR-04 — Identify Slow-Moving and Near-Expiry Products

**Requirement:**  
The system shall identify products that are slow-moving or approaching their expiry date and generate alerts when products require attention.

**Use Case:**  
UC-04 — Identify Slow-Moving and Near-Expiry Products

**Traceability:**  
FR-04 → UC-04 → Slow-moving and expiry-alert testing

**Verification:**  
The system will be tested to confirm that slow-moving products can be identified and that applicable alerts can be generated.

**Data limitation:**  
The current team dataset does not contain product expiry-date information. Expiry monitoring therefore requires additional expiry-date information to be captured or supplied to the system.

---

### FR-05 — Provide a Natural-Language Chatbot

**Requirement:**  
The system shall provide a natural-language chatbot that allows users to ask questions about stock and sales information.

**Use Case:**  
UC-05 — Interact with Natural-Language Chatbot

**Traceability:**  
FR-05 → UC-05 → Chatbot interaction testing

**Verification:**  
The chatbot will be tested using representative natural-language questions about stock levels, demand forecasts, recommended orders and other supported information.

---

### FR-06 — Display an Interactive Dashboard

**Requirement:**  
The system shall provide an interactive dashboard displaying relevant inventory and forecasting information.

**Use Case:**  
UC-06 — View Interactive Dashboard

**Traceability:**  
FR-06 → UC-06 → Dashboard functional testing

**Verification:**  
The dashboard will be tested to confirm that sales trends, stock levels, demand predictions, reorder recommendations and stock alerts can be displayed to users.

## 4. Requirement Coverage

| Requirement | Use Case Linked | Verification Defined | Coverage Status |
|---|---|---|---|
| FR-01 | UC-01 | Yes | Covered |
| FR-02 | UC-02 | Yes | Covered |
| FR-03 | UC-03 | Yes | Covered with data limitation |
| FR-04 | UC-04 | Yes | Covered with data limitation |
| FR-05 | UC-05 | Yes | Covered |
| FR-06 | UC-06 | Yes | Covered |

All six functional requirements have corresponding use cases and defined verification approaches.

## 5. Data and Scope Considerations

The current team dataset contains sales, inventory, product, pricing, discount, weather, holiday/promotion, competitor pricing and seasonality information.

The dataset does not directly contain:

- Supplier lead-time information.
- Product expiry dates.
- Customer profiles.

Therefore, the requirements and system design must not represent these unavailable dataset fields as if they are already present.

FR-03 may require supplier lead time to be provided through additional system input or another approved data source.

FR-04 requires expiry-date information if actual near-expiry monitoring is implemented.

## 6. Traceability Relationships

The main requirements traceability chain is:

**Functional Requirement → Use Case → System Function → Verification**

This provides a basis for progressing from requirements engineering into system analysis, system design, implementation and testing.

## 7. Verification

The matrix has been checked against:

- `documentation/02-requirements/Requirements Engineering.md`
- `documentation/02-requirements/use-cases/M04-04-use-case-specifications.md`

The six functional requirements FR-01 to FR-06 are represented in the matrix and linked to UC-01 to UC-06 respectively.
