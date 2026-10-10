# M06-02 — Navigation and Dark-Mode Wireframes

## Purpose

Define a consistent desktop information architecture for Retail-X and provide visual wireframes for the main inventory workflows, demand forecasting, restocking, alerts and AI chatbot. These are **design artefacts**, not implemented application screens.

## Visual direction

- Black / near-black page background (`#07090D`) with dark charcoal panels (`#10151D`, `#151C26`).
- White primary text, muted grey supporting labels, and teal / blue / amber / red accents for status and charts.
- Consistent left sidebar across all screens: Dashboard, Inventory, Forecasting, Restocking, Alerts, AI Chatbot. The selected destination is highlighted.
- Readable contrast, restrained accents, consistent cards and clear separation between content areas.

## Screen definitions

### UI-01 — Dashboard

Purpose: the starting point for an at-a-glance view of retail operations. Includes KPI placeholders, an observed-versus-projected demand trend, attention items and quick actions into data capture / inventory, forecasting and the AI chatbot. KPIs remain blank until connected data supplies them.

### UI-02 — Inventory

Purpose: find products and review current stock, reorder thresholds and data freshness. Includes search, filters and a structured inventory table. Missing quantities and thresholds are shown as unknown rather than estimated or invented.

### UI-03 — Forecasting

Purpose: review historical demand and predicted demand in one view. Includes product/category and horizon selectors, forecast summary fields, a chart with separate solid historical and dashed forecast lines, a projection window, and guidance about data coverage. Forecasts must not be presented as valid if required history is missing or insufficient; limitations should be explicit.

### UI-04 — Restocking

Purpose: help a user inspect candidate restocking actions. Includes a review queue, current and target stock fields, suggested quantities where supported, and a visible reminder that recommendations are advisory. A human must review the recommendation before any purchase/order action; this wireframe does not imply automatic ordering.

### UI-05 — Product Alerts

Purpose: provide an inbox of exceptions such as stock-threshold reviews, expiry-information checks, incomplete forecast inputs and data synchronisation status. Severity, source and timestamps should be shown when the backend makes them available. Expiry claims must be verified against the source.

### UI-06 — AI Chatbot

Purpose: offer a persistent, dedicated conversational route to inventory, forecasting and alert information. Suggested prompts lower the barrier to entry. Responses should use available Retail-X data, identify missing evidence, and avoid making unsupported claims. The chatbot is available from the shared sidebar.

## Navigation

The shared menu order is Dashboard → Inventory → Forecasting → Restocking → Alerts → AI Chatbot. From each screen a user can switch to any other area without returning to the dashboard. Relevant workflow links also connect Inventory to Forecasting and Restocking, Forecasting to Restocking, and alerts or analysis views to the chatbot. See [`M06-02-navigation-flow.md`](../../../diagrams/ui-ux/M06-02-navigation-flow.md).

## Artefacts

- [`M06-02-navigation-flow.md`](../../../diagrams/ui-ux/M06-02-navigation-flow.md) — shared navigation and interaction logic.
- [`M06-02-wireframes.svg`](../../../diagrams/ui-ux/M06-02-wireframes.svg) — dashboard, inventory, forecasting and restocking layouts.
- [`M06-02-wireframes-alerts-assistant.svg`](../../../diagrams/ui-ux/M06-02-wireframes-alerts-assistant.svg) — product alerts and AI chatbot layouts.
- [`M06-02-wireframes-notes.md`](../../../diagrams/ui-ux/M06-02-wireframes-notes.md) — interpretation, limitations and screen mapping.

## Data and implementation boundaries

All example rows, trend lines and status fields in the SVGs are illustrative placeholders. They are not real Retail-X metrics and must not be represented as live operational data. The diagrams define layout and intended behaviour only; they do not demonstrate a working UI, backend integration, forecast model or chatbot implementation.
