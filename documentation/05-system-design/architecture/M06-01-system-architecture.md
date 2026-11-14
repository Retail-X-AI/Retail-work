# M06-01: System Architecture Design

## 1. Document Purpose

This document describes the logical architecture of Retail-X-AI, an AI-powered inventory demand forecasting and smart restocking system intended to support local spaza shops and small retailers.

It explains the main system components, their responsibilities, data interactions, and technical constraints.

The architecture distinguishes between the original logical design and the components included in the current Python-based implementation.

## 2. Architecture Approach

Retail-X-AI uses a layered logical architecture to separate data management, application services, AI and machine learning processing, and decision-support functionality.

The architecture is intended to make the system easier to understand, test, maintain, and extend.

The current implementation primarily uses Python, SQLite, pandas, and machine learning libraries.

A graphical user interface, browser-based dashboard, Streamlit application, and HTML frontend are outside the current project scope.

## 3. Architecture Layers and Responsibilities

### 3.1 Presentation Layer

A graphical presentation layer is outside the scope of the current project implementation.

The project does not include a browser-based dashboard, Streamlit application, or HTML frontend.

The current Python-based chatbot provides message processing through its assistant implementation. AI outputs and analytical results are generated and stored through the project's Python components.

The original logical presentation layer is retained as an architectural concept and must not be interpreted as an implemented deliverable.

### 3.2 Application Layer

The application layer contains Python services that coordinate access to database records, forecasting results, and restocking recommendations.

Its responsibilities include:

- Providing access to inventory and product information.
- Retrieving saved forecasting results.
- Providing restocking recommendation information.
- Coordinating chatbot requests with relevant Python services.
- Handling invalid inputs and unavailable data.
- Supporting database operations through the relevant service modules.

The current implementation uses Python modules and service functions rather than a browser-based HTTP API.

### 3.3 Domain Services Layer

| Component | Responsibility |
|---|---|
| Database Management | Store and retrieve inventory, product, spoilage, and damage records. |
| Data Analysis | Examine historical retail data and identify relevant patterns and limitations. |
| Demand Forecasting | Prepare forecasting inputs, train models, evaluate results, and generate saved forecast outputs. |
| Stockout Detection | Identify historical stockout-risk conditions using available inventory and demand information. |
| Restocking Recommendations | Calculate suggested replenishment quantities using configured assumptions. |
| Supplier Recommendations | Rank available supplier options using defined scoring criteria. |
| AI Chatbot | Interpret user messages and retrieve relevant information through supported intents and handlers. |
| Reporting and Validation | Validate saved AI outputs and produce evaluation evidence. |

These responsibilities are implemented through Python modules and supporting database services.

### 3.4 AI and Machine Learning Capabilities

The AI and machine learning components support data preparation, feature engineering, forecasting, anomaly detection, clustering, restocking analysis, and chatbot intent classification.

The forecasting target is Units Sold.

The selected forecasting model uses Ridge Regression. Evaluation is performed using chronological training and testing data.

The current forecasting results represent historical one-step-ahead evaluation rather than verified predictions for future trading days.

The project also evaluates Random Forest and XGBoost models for comparison. Their results are retained as model comparison evidence.

KMeans is used for clustering analysis, while Isolation Forest supports anomaly detection.

The chatbot uses an intent classification model to identify user requests and route them to appropriate handlers.

AI responses must be based on available project data. Missing information must be identified rather than invented.

Important limitations include:

- The supplied dataset is a generic retail dataset rather than actual transaction records from South African spaza shops.
- Supplier performance cannot be established reliably without historical supplier delivery information.
- Restocking calculations use configured lead-time and safety-stock assumptions.
- Stockout-risk flags do not establish that an actual stockout occurred.
- Supplier recommendations use rule-based scoring and are not probability predictions.

### 3.5 Logical Data Layer

The system uses SQLite for database storage and CSV files for historical datasets and generated analytical outputs.

| Data category | Purpose |
|---|---|
| Product Data | Store product identifiers and generated SKU codes. |
| Inventory Data | Store historical inventory, sales, and ordering information. |
| Forecast Data | Store forecasting results and evaluation information. |
| Restocking Data | Store reorder recommendations and related calculations. |
| Stockout Data | Store historical stockout detection and risk results. |
| Spoilage and Damage Data | Record product spoilage and damage information. |
| Chatbot Data | Store training examples and the trained intent classification model. |

The database schema defines the relationships and constraints used by the SQLite implementation.

CSV datasets and generated outputs are maintained separately from the database where appropriate.

### 3.6 External Data Inputs

The historical retail dataset provides the records used for data preparation, analysis, and forecasting.

The canonical dataset is:

`dataset/raw/retail_store_inventory.csv`

Imported records are checked for required fields, missing values, valid numeric values, and applicable constraints.

The dataset does not provide verified supplier delivery histories, actual supplier lead times, or customer profiles.

Features that depend on unavailable information must be treated as limitations or require additional verified data.

## 4. Principal Information Flows

1. Historical retail records are loaded from the canonical CSV dataset.
2. The data preparation process validates and prepares the records.
3. Prepared data is passed to the relevant analysis and machine learning components.
4. Forecasting models generate historical evaluation outputs.
5. Stockout detection and restocking components process the available inventory and forecasting information.
6. Results are saved as CSV outputs or stored in the SQLite database, depending on the component.
7. The Python chatbot processes user messages and retrieves relevant information through its supported handlers.
8. Testing and validation components examine the generated outputs and record evidence.
9. Shop owners or managers can use the resulting information as decision support. Purchasing and restocking decisions remain their responsibility.

## 5. Security and Data Protection

The architecture considers the following security requirements:

- Validate imported records and user-provided values.
- Protect database integrity through appropriate constraints and transactions.
- Keep credentials and sensitive configuration information outside committed source code.
- Avoid exposing sensitive information in error messages and logs.
- Handle database errors and invalid requests appropriately.
- Review external model integrations before transmitting project or user information.

The current project does not claim to implement a complete production authentication, authorization, or deployment security environment.

## 6. Reliability and Maintainability

The system should support:

- Separation of data preparation, database operations, AI processing, and business logic.
- Reproducible data preparation and model evaluation.
- Validation of saved forecasting and restocking outputs.
- Automated testing of database, AI, integration, and performance functionality.
- Clear handling of invalid inputs and missing data.
- Documented assumptions and limitations.
- Testing of individual components independently.

The project includes automated tests for database services, chatbot functionality, forecasting integration, restocking recommendations, stockout detection, and performance.

## 7. Scope and Assumptions

This document describes the architecture of the current Python-based AI project and its logical design.

The following are outside the current implementation scope:

- Browser-based dashboards.
- Streamlit applications.
- HTML, CSS, and JavaScript frontend interfaces.
- Browser-based chatbot interfaces.
- Live point-of-sale integration.
- Live supplier system integration.
- Automatic purchasing or ordering.

The project uses historical retail data and does not claim to represent live operations at actual spaza shops.

Forecasting, stockout detection, supplier recommendations, and restocking calculations are decision-support functions. Their results must be interpreted according to the documented data limitations and assumptions.

## 8. Traceability to Existing Analysis

| Existing artefact | Architecture contribution |
|---|---|
| M05-01 System Context Diagram | Defines the system boundary and external inputs. |
| M05-02 DFD Level 0 | Defines the major processes and high-level information flows. |
| M05-03 DFD Level 1 | Refines data preparation, forecasting, risk assessment, restocking, and chatbot processes. |
| M04 Use Case Artefacts | Provide the original behavioural requirements for the system. |
| Data Analysis Documentation | Provides dataset profiling, forecasting target, feature selection, and leakage analysis. |
| AI Model Evaluation Evidence | Records model performance and the limitations of the selected models. |
| Testing Documentation | Provides evidence of database, AI, integration, and performance testing. |

## 9. Verification Checklist

- [ ] Confirm that the architecture agrees with the available M05 diagrams.
- [ ] Confirm that the logical data categories match the current database and output files.
- [ ] Confirm that forecasting assumptions match the data analysis documentation.
- [ ] Confirm that unavailable supplier and customer information is not presented as available.
- [ ] Confirm that the chatbot description matches the current Python implementation.
- [ ] Confirm that graphical interfaces and browser APIs are not presented as current deliverables.
- [ ] Review the architecture for consistency with the actual source code.
- [ ] Obtain team review before final submission.