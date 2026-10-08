# Benefits, Constraints and Risks

## 1. Introduction

RetailAI is designed to support local spaza shops and small retailers by helping them make better stock and sales decisions. The system uses available sales and stock information to provide product forecasts, reorder recommendations, alerts and other decision-support features.

This document identifies the expected benefits of the RetailAI solution, the constraints that may affect implementation, and the major risks together with their potential impacts and mitigation strategies.

---

## 2. Benefits

### 2.1 Improved Stock Management

RetailAI will help shop owners understand which products are likely to be needed in the future. This can support better stock planning and reduce unnecessary overstocking or stock shortages.

### 2.2 Improved Forecasting and Decision-Making

The system will use available sales and stock data to generate forecasts. These forecasts can help shop owners make more informed decisions about purchasing and inventory management.

### 2.3 Reduced Stock-Outs

Forecasting and reorder recommendations can help identify products that may need to be replenished before they run out of stock.

### 2.4 Reduced Product Waste

The system can provide alerts for slow-moving or near-expiry products. This can help shop owners identify products that require attention and reduce potential losses.

### 2.5 Simple and Accessible User Experience

The system will be designed for users with limited digital experience. A simple interface and plain-language chatbot can make the system easier to understand and use.

### 2.6 Support for Small Retail Businesses

RetailAI is designed with the conditions of local spaza shops in mind. It aims to provide useful forecasting and stock-management support without requiring expensive infrastructure.

### 2.7 Offline Support

The core forecasting functionality can operate when internet connectivity is unavailable. This is important for environments where internet connectivity may be unreliable.

### 2.8 Better Use of Available Data

The system can use sales and stock information to provide useful insights instead of relying entirely on manual decision-making.

---

## 3. Constraints

### 3.1 Limited Historical Data

Many shops may have incomplete or no digital sales records. The solution must therefore be able to work with small datasets and support progressive learning as more data becomes available.

### 3.2 Hardware and Connectivity Constraints

The system must consider hardware limitations and unreliable internet connectivity that may occur in township environments.

### 3.3 Budget

The project has limited financial resources. The solution should therefore rely on open-source Python libraries and free-tier cloud services where possible.

### 3.4 Time

The project must be completed within the academic semester timeline. This limits the amount of functionality that can be developed and tested.

---

## 4. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Insufficient historical sales data | Poor forecast accuracy | Use synthetic data for prototyping, implement simple forecasting baselines, and allow manual data entry. |
| Low digital literacy of users | Low adoption | Provide an extremely simple user interface, chatbot in plain language, short training guide, and local language support where feasible. |
| Internet or power interruptions | System unavailable | Make core modules offline-capable, use local SQLite storage, and synchronise data when the system is online. |
| Model drift or changing demand patterns | Forecast accuracy may decrease over time | Use a periodic re-training schedule, monitor MAPE, and implement simple model update mechanisms. |

---

## 5. Risk Management Approach

The identified risks will be monitored throughout the project. The project team will review the risks regularly and update their probability, impact and mitigation strategies when necessary.

High-impact risks will receive priority attention. The team will also use testing and user feedback to identify new risks that may arise during development and implementation.

---

## 6. Verification and Evidence

The completed document will be reviewed against the RetailAI problem definition to verify that the identified benefits, constraints and risks are relevant to the project.

Evidence for this milestone includes:

- Benefits documented.
- Project constraints documented.
- Major project risks identified.
- Impact of each risk documented.
- Mitigation strategy provided for each identified risk.
- Document saved in `documentation/01-business-analysis/`.
- Git commit containing issue ID `M03-05`.
- Pull request linked to the M03-05 issue.
- Review completed before merging.

---

## 7. Conclusion

RetailAI can provide significant benefits to local spaza shops by improving stock management, forecasting, purchasing decisions and awareness of slow-moving or near-expiry products. However, the project must consider important constraints such as limited historical data, hardware and connectivity limitations, budget and the academic project timeline.

The main risks can be managed through approaches such as using synthetic data during development, keeping the interface simple, supporting offline functionality and monitoring forecasting performance. Addressing these benefits, constraints and risks will help ensure that the RetailAI solution is practical and suitable for its intended users.
