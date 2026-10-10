# M06-02 — Retail-X-AI Navigation Flow

## Purpose
Show how the Shop Owner / Manager navigates between the main Retail-X-AI functions.

```mermaid
flowchart TD
    START([Open Retail-X-AI]) --> DASH[Dashboard]

    DASH --> DATA[Capture Sales and Stock]
    DASH --> FORECAST[Demand Forecasts]
    DASH --> RESTOCK[Restocking Recommendations]
    DASH --> ALERTS[Product Alerts]
    DASH --> ASSIST[AI Assistant]

    DATA --> METHOD{Choose input method}
    METHOD --> CSV[Upload CSV / POS Export]
    METHOD --> MANUAL[Manual Data Entry]
    CSV --> VALIDATE{Data valid?}
    MANUAL --> VALIDATE
    VALIDATE -->|Yes| SAVED[Confirmation and Saved Data]
    VALIDATE -->|No| ERR[Show errors and request correction]
    ERR --> METHOD
    SAVED --> DASH

    FORECAST --> SELECT[Select product or category]
    SELECT --> CHECK{Sufficient valid history?}
    CHECK -->|Yes| RESULT[View Forecast]
    CHECK -->|No| INSUFF[Explain insufficient data]
    RESULT --> RESTOCK
    INSUFF --> DATA

    RESTOCK --> STOCK{Stock and demand data available?}
    STOCK -->|Yes| RECOMMEND[View suggested reorder quantity]
    STOCK -->|No| MISSING[Explain missing information]
    RECOMMEND --> DASH
    MISSING --> DATA

    ALERTS --> REVIEW[Review slow-moving products]
    REVIEW --> EXPIRY{Valid expiry data available?}
    EXPIRY -->|Yes| EXP[Show verified expiry alerts where applicable]
    EXPIRY -->|No| NOEXP[State expiry status cannot be confirmed]
    EXP --> DASH
    NOEXP --> DASH

    ASSIST --> QUESTION[Enter a natural-language request]
    QUESTION --> RESPONSE[View answer based on available information]
    RESPONSE --> FOLLOW{Ask follow-up?}
    FOLLOW -->|Yes| QUESTION
    FOLLOW -->|No| DASH

    classDef main fill:#e8f0fe,stroke:#356ac3,color:#172b4d
    classDef caution fill:#fff4d6,stroke:#b78103,color:#493600
    class DASH,DATA,FORECAST,RESTOCK,ALERTS,ASSIST main
    class ERR,INSUFF,MISSING,NOEXP caution
```

## Primary navigation
- Dashboard
- Capture Sales and Stock
- Demand Forecasts
- Restocking Recommendations
- Product Alerts
- AI Assistant

## Navigation rules
- Keep the primary navigation available from every main screen.
- Provide a clear return to the Dashboard.
- Show validation errors beside the relevant data input.
- Never show a forecast or reorder quantity as confirmed when required data is missing.
- Never label a product as near expiry unless valid expiry data supports that status.
- The AI Assistant must explain when requested information is unavailable rather than inventing figures.
