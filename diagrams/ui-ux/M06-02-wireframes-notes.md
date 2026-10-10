# M06-02 Wireframe Notes

## What these artefacts represent

The SVGs are static, editable vector wireframes showing the proposed Retail-X desktop interface in dark mode. They are intended to communicate structure, screen hierarchy, navigation and key user interactions to the person implementing the UI. They are **not screenshots of a running application**.

## Files

- `M06-02-wireframes.svg`: four screens — Dashboard, Inventory, Forecasting and Restocking.
- `M06-02-wireframes-alerts-assistant.svg`: two screens — Product Alerts and AI Chatbot.
- `M06-02-navigation-flow.md`: navigation paths and data-aware behaviour.

## Dark-mode style

Near-black canvas, charcoal panels, white primary text, muted secondary text and restrained teal / blue / amber / red accents. Keep the left navigation consistent on every screen and clearly highlight the active destination.

## Screen-to-use-case mapping

| Screen | Main purpose | Use-case alignment |
| --- | --- | --- |
| UI-01 Dashboard | Overview and shortcuts | UC-01 overview / entry point |
| UI-02 Inventory | Product and stock review | UC-02 inventory / data review |
| UI-03 Forecasting | Demand history and projections | UC-03 demand forecasting |
| UI-04 Restocking | Review suggested replenishment | UC-04 restocking decision support |
| UI-05 Product Alerts | Review exceptions and warnings | UC-05 alerts |
| UI-06 AI Chatbot | Ask questions using available data | UC-06 AI assistant |

Confirm the UC numbering and wording against the approved use-case catalogue before implementation if that catalogue has changed.

## Important constraints

- Every displayed value and plotted trend is illustrative, not production data.
- Leave unknown quantities, confidence and status values blank or explicitly unavailable. Do not invent inventory counts, demand predictions, alert events or expiry dates.
- Clearly distinguish observed data from predicted demand. Indicate when forecasting is unavailable or limited by missing history.
- Restocking is a human-reviewed recommendation; these designs do not specify automatic purchasing.
- AI responses must be grounded in connected Retail-X sources and state when required information is missing.
- Preserve readable contrast and the same menu order across the screen family: Dashboard, Inventory, Forecasting, Restocking, Alerts, AI Chatbot.
