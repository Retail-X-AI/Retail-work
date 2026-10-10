# M06-01 — Retail-X-AI Logical System Architecture

## Purpose

This diagram describes the proposed logical architecture of Retail-X-AI.
It separates user-facing functionality, application coordination, domain
services, AI/ML capabilities, data storage, and external data inputs.

The diagram is technology-neutral. It describes component responsibilities
and logical interactions rather than a confirmed deployment or technology stack.

## Architecture Diagram

```mermaid
flowchart TB
    USER["Shop Owner / Manager"]

    subgraph PRESENTATION["1. Presentation Layer"]
        UI["Web or Application Interface"]
        DASH["Dashboard and Alerts UI"]
        CHAT["Conversational Assistant UI"]
    end

    subgraph APPLICATION["2. Application Layer"]
        API["Application API / Request Coordination"]
        AUTH["Authentication and Access Control"]
        VALIDATE["Input Validation"]
    end

    subgraph SERVICES["3. Domain Services Layer"]
        SALES["Sales and Inventory Management"]
        ANALYTICS["Retail Data Analysis"]
        FORECAST["Demand Forecasting"]
        RISK["Stockout-Risk Assessment"]
        RESTOCK["Restocking Recommendations"]
        REPORT["Dashboard and Reporting"]
        ASSIST["AI Assistant Orchestration"]
    end

    subgraph AIML["4. AI / ML Capabilities"]
        PREP["Data Preparation and Feature Selection"]
        MODEL["Forecast Model"]
        RESPONSE["Grounded Response Generation"]
    end

    subgraph DATA["5. Logical Data Layer"]
        PRODUCT[("D1 Product Data")]
        INVENTORY[("D2 Sales and Inventory Data")]
        RESULTS[("D3 Forecast and Analytics Data")]
        ALERTS[("D4 Recommendations and Alerts")]
    end

    DATASET[("External Historical Retail Dataset")]
    OPERATOR["External Model or AI Provider, if approved"]

    USER --> UI
    UI --> DASH
    UI --> CHAT

    DASH --> API
    CHAT --> API
    API --> AUTH
    AUTH --> VALIDATE
    VALIDATE --> SALES
    VALIDATE --> ANALYTICS
    VALIDATE --> FORECAST
    VALIDATE --> RISK
    VALIDATE --> RESTOCK
    VALIDATE --> REPORT
    VALIDATE --> ASSIST

    DATASET --> SALES
    SALES <--> PRODUCT
    SALES <--> INVENTORY

    PRODUCT --> ANALYTICS
    INVENTORY --> ANALYTICS
    ANALYTICS --> RESULTS

    INVENTORY --> PREP
    RESULTS --> PREP
    PREP --> MODEL
    MODEL --> RESULTS

    INVENTORY --> RISK
    RESULTS --> RISK
    RISK --> ALERTS

    INVENTORY --> RESTOCK
    RESULTS --> RESTOCK
    ALERTS --> RESTOCK
    RESTOCK --> ALERTS

    INVENTORY --> REPORT
    RESULTS --> REPORT
    ALERTS --> REPORT
    REPORT --> DASH

    PRODUCT --> ASSIST
    INVENTORY --> ASSIST
    RESULTS --> ASSIST
    ALERTS --> ASSIST
    ASSIST --> RESPONSE
    RESPONSE --> CHAT
    RESPONSE -. "Optional integration; approval required" .-> OPERATOR

    AUTH -. "Cross-cutting security" .-> API
    AUTH -. "Access restrictions" .-> DATA
```

## Interpretation

- The presentation layer provides dashboard, alert, and conversational interfaces.
- The application layer coordinates requests, validates inputs, and applies access
  controls before protected operations are performed.
- Domain services manage sales and inventory, analysis, forecasting, stockout
  assessment, restocking recommendations, reporting, and AI-assisted requests.
- AI/ML capabilities prepare suitable data, generate forecasts, and support
  responses grounded in retrieved system information.
- The logical data layer holds the four data-store categories identified in M05.
- The historical retail dataset is an external input. Any external model or AI
  provider is optional and requires an approved integration decision.

## Important Boundaries

This is a logical component view, not a deployment diagram. It does not specify
a programming language, web framework, cloud platform, database product, model
provider, network topology, or physical server arrangement.
