# M06-02 — Wireframe Coverage Notes

## Visual wireframe inventory

The two SVG files together provide low-fidelity desktop layouts for all six screens:

- UI-01 — Dashboard
- UI-02 — Data Capture
- UI-03 — Demand Forecasts
- UI-04 — Restocking Recommendations
- UI-05 — Product Alerts
- UI-06 — AI Assistant

### Wireframe files

- `M06-02-wireframes.svg` — Dashboard, Data Capture, Demand Forecasts, and Restocking.
- `M06-02-wireframes-alerts-assistant.svg` — Product Alerts and AI Assistant.

The screen descriptions, requirements, and use-case mappings are documented in `documentation/05-system-design/ui-ux/M06-02-navigation-and-wireframes.md`.

These are conceptual, low-fidelity design artefacts. They establish content hierarchy and navigation, not final branding, production styling, or implemented behaviour. Example products and conversation content are placeholders, not actual Retail-X data.

## Design safeguards

- Do not present forecasts or reorder quantities as confirmed when required data is missing.
- Do not label a product as expired or near expiry without verified expiry data.
- The AI Assistant should identify unavailable information rather than inventing figures.
