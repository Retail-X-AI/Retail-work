# M06-01 — System Architecture Design

## 1. Document Purpose

This document defines the proposed logical architecture for Retail-X-AI, an
AI-powered inventory demand forecasting and smart restocking system intended
to support local spaza shop owners and managers.

The design translates the system boundary and processes described in the M05
system context diagram and data-flow diagrams into logical component layers,
responsibilities, data interactions, and design constraints.

**Architecture diagram:** `diagrams/architecture/M06-01-system-architecture.md`

## 2. Architecture Approach

A layered logical architecture is proposed to separate user interaction,
request coordination, business capabilities, AI/ML processing, and data storage.

The separation is intended to make component responsibilities easier to
understand, test, maintain, and evolve. It does not require each logical
component to run as a separate deployable service.

The architecture remains technology-neutral until implementation and deployment
decisions are agreed and documented.

## 3. Architecture Layers and Responsibilities

### 3.1 Presentation Layer

Responsibilities:

- Present sales and inventory information.
- Display forecasts, analytical results, stockout-risk alerts, and restocking
  recommendations.
- Provide the interface for inventory-related questions and AI-assisted requests.
- Present missing-data limitations and relevant warnings clearly.

The presentation layer must not be treated as the authoritative source for
business rules or stored inventory values.

### 3.2 Application Layer

Responsibilities:

- Coordinate requests between the interface and domain services.
- Validate request structure and required inputs.
- Enforce authentication and authorization at appropriate entry points.
- Return consistent results and understandable error responses.

Authorization must also be enforced at protected operations and data boundaries;
the interface alone is not a security control.

### 3.3 Domain Services Layer

| Component | Responsibility |
|---|---|
| Sales and Inventory Management | Record and maintain product, sales, and inventory information. |
| Retail Data Analysis | Analyse suitable sales and inventory information and make analytical results available. |
| Demand Forecasting | Generate forecasts using an approved target, data preparation process, and model. |
| Stockout-Risk Assessment | Assess risk using available inventory and relevant demand information. |
| Restocking Recommendations | Suggest replenishment quantities based on available, verified inputs. |
| Dashboard and Reporting | Assemble sales, inventory, forecast, recommendation, and alert information for presentation. |
| AI Assistant Orchestration | Interpret requests, retrieve relevant information, and coordinate grounded responses. |

These are logical responsibilities. Their eventual implementation boundaries
may change after detailed design and technical decisions.

### 3.4 AI / ML Capabilities

The AI/ML area covers data preparation, feature selection, forecasting, and
response generation.

The initial demand-forecasting target is `Units Sold`, as documented in M05-03.
Potential leakage fields identified in the analysis must be excluded from the
initial forecasting inputs unless the data-analysis decisions are formally
reviewed and revised. A field used for stock monitoring is not automatically
an appropriate forecasting feature.

AI assistant responses must be grounded in information retrieved from approved
system data or other explicitly approved sources. Unavailable values must be
identified as unknown rather than invented.

If an external model or AI provider is selected, the integration must be
reviewed for privacy, security, data handling, availability, and cost before use.
No particular provider is assumed by this design.

### 3.5 Logical Data Layer

The design carries forward the logical data stores from M05:

| ID | Data store | Purpose |
|---|---|---|
| D1 | Product Data | Product identifiers and related product information. |
| D2 | Sales and Inventory Data | Recorded sales and inventory information. |
| D3 | Forecast and Analytics Data | Forecast outputs and analytical results. |
| D4 | Recommendations and Alerts | Stockout-risk alerts and restocking recommendations. |

These are logical data categories, not a final physical database schema.
Database tables, relationships, retention, migrations, and transaction
boundaries must be established during database design.

### 3.6 External Data Inputs

The historical retail dataset supplies records for data preparation, analysis,
and forecasting. Imported data must be checked for required fields, valid
values, consistency, and suitability before being used.

The architecture must not assume that the selected dataset contains supplier
lead times, expiry dates, or customer profiles. If a feature depends on
unavailable information, the system must request a verified input or use an
approved additional source.

## 4. Principal Information Flows

1. A shop owner or manager uses the interface to enter information or request
   sales, inventory, forecasting, or assistant functionality.
2. The application layer validates the request and checks authorization.
3. Domain services read or update the appropriate logical data stores.
4. Historical retail records are prepared and analysed before they are used
   for forecasting.
5. Forecast results are made available to stockout-risk assessment,
   recommendations, and reporting.
6. The AI assistant retrieves relevant product, sales, inventory, forecast,
   or recommendation information before responding.
7. The dashboard presents current system information and generated outputs.
8. The shop owner or manager reviews recommendations and remains responsible
   for purchasing and restocking decisions.

## 5. Security and Data Protection

The architecture must support the following design requirements:

- Authenticate users where required by the approved access model.
- Authorize protected actions and restrict access to data appropriately.
- Validate imported records and user-supplied values.
- Protect credentials and other secrets; do not commit them to the repository.
- Avoid exposing sensitive records in error messages, logs, or AI prompts.
- Apply appropriate transport and storage protections once the deployment
  environment and data classification are established.
- Record relevant errors and operational events without unnecessarily logging
  sensitive data.
- Review external AI/model integrations before transmitting project or user data.

The specific identity provider, permissions model, encryption configuration,
audit requirements, and deployment controls remain decisions for detailed
security and deployment design.

## 6. Reliability and Maintainability

The design should support:

- Clear separation of component responsibilities.
- Validation and understandable handling of missing or invalid data.
- Testing of domain logic independently of the presentation layer.
- Monitoring of failed imports, forecasting failures, and unavailable
  dependencies once implementation choices are known.
- Reproducible forecasting inputs and documented model assumptions.
- Clear communication when forecasts or recommendations cannot be produced
  reliably from available data.

## 7. Scope and Assumptions

This document defines a logical architecture. It does not claim that all
components have already been implemented, integrated, or deployed.

The following remain to be confirmed during subsequent design and implementation:

- Technology stack and deployment topology.
- Physical database schema and persistence technology.
- Authentication provider and detailed role permissions.
- Forecast model implementation and evaluation thresholds.
- AI assistant implementation and whether an external provider is required.
- Data-import mechanism, scheduling, and failure-recovery behaviour.
- Supplier lead-time and expiry-data sources, if those features are approved.

The shop owner or manager retains final authority over restocking and purchase
decisions; recommendations are decision support, not automatic purchase orders.

## 8. Traceability to Existing Analysis

| Existing artefact | Architecture contribution |
|---|---|
| M05-01 System Context Diagram | Defines the system boundary, user, and historical dataset. |
| M05-02 DFD Level 0 | Defines major processes, logical data stores, and high-level data flows. |
| M05-03 DFD Level 1 | Refines data preparation, forecasting, risk assessment, restocking, AI assistant, and reporting processes. |
| M04 use-case artefacts and requirements | Provide behavioural requirements to be checked during detailed design. |
| Data-analysis documentation | Remains the source of truth for dataset profiling, forecasting target, and leakage decisions. |

The repository currently contains placeholder-only activity-diagram and
sequence-diagram folders. Those artefacts should be completed or their status
confirmed separately; this architecture does not claim to be verified against
diagrams that are not present.

## 9. Verification Checklist

- [ ] Confirm the diagram and description agree with M05-01, M05-02, and M05-03.
- [ ] Confirm all four logical data stores are represented consistently.
- [ ] Confirm the forecasting target and leakage limitations match data analysis.
- [ ] Confirm unavailable supplier lead times and expiry dates are not assumed.
- [ ] Confirm optional external AI integration is not presented as a decided dependency.
- [ ] Review Mermaid syntax and render the diagram in a compatible viewer.
- [ ] Obtain team review before merging.
