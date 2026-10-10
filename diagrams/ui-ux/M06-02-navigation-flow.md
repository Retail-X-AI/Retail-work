# M06-02 — Navigation Flow

## Shared navigation

Every screen uses the same left-hand navigation in this order: **Dashboard → Inventory → Forecasting → Restocking → Alerts → AI Chatbot**. The active destination is highlighted, and the chatbot remains directly accessible from every screen.

```mermaid
flowchart TD
    D[Dashboard] --> I[Inventory]
    D --> F[Forecasting]
    D --> R[Restocking]
    D --> A[Product Alerts]
    D --> C[AI Chatbot]
    I <--> F
    I <--> R
    I --> A
    F --> R
    F --> C
    R --> C
    A --> C
    I --> V{Inventory data available?}
    V -- Yes --> I1[Show source-backed stock values]
    V -- No --> I2[Show missing-data state; no invented values]
    F --> H{Enough demand history?}
    H -- Yes --> F1[Show observed demand and forecast separately]
    H -- No --> F2[Explain forecast is unavailable or limited]
    R --> Q[Review recommendation]
    Q --> P[Human checks before purchase action]
    C --> G[Answer from connected Retail-X sources]
    G --> M{Required evidence available?}
    M -- Yes --> E[Explain answer and source context]
    M -- No --> N[State what is missing; do not guess]
    A --> X[Verify alert type, timestamp and source]
```

## Main interaction rules

- Dashboard provides a high-level entry point to all six areas.
- Inventory is the source for current stock and configured reorder thresholds. Unknown values remain visibly unknown.
- Forecasting separates historical observations from projected demand and communicates limited or missing history.
- Restocking recommendations are advisory and require human review before any order is placed.
- Alerts show the type, severity, source and timestamp when available. Expiry-related information must be verified against its source.
- The AI Chatbot can be opened from any screen. It should answer using connected Retail-X data, state relevant limitations, and never fabricate quantities, forecasts or events.
