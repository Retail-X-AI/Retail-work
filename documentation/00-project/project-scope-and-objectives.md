# RetailAI — Project Scope and Objectives

## 1. Project Identification

**Institution:** Vaal University of Technology
**Faculty:** Faculty of Applied and Computer Sciences
**Qualification:** Diploma in Information Technology
**Subject:** Business Analysis 3.2
**Subject Code:** AIBUY3A
**Project:** RetailAI
**Theme:** An AI Solution for Industries
**Industry Sector:** Retail

**Project Title:**
**An AI-Powered Inventory Demand Forecasting and Smart Restocking System for Local Spaza Shops**

**Project Issue:** M01-01 — Confirm Project Scope, Objectives and Boundaries

---

## 2. Project Background

RetailAI is an Artificial Intelligence solution designed for local spaza shops and small grocery retailers. The project applies AI, machine learning, data analysis and natural language processing to address practical inventory management challenges within the retail industry.

The solution focuses on helping small retailers make more informed inventory decisions by analysing historical sales and inventory information, forecasting future demand, identifying potential stockouts and providing intelligent restocking recommendations.

The project is aligned with the Business Analysis 3.2 theme **“An AI Solution for Industries”** because it applies AI technologies to a real-world retail problem affecting small businesses.

---

## 3. Problem Definition

Local spaza shops and small grocery stores often experience difficulties managing inventory because they may have limited digital records, limited access to analytical tools and a strong reliance on manual experience when making purchasing and restocking decisions.

These challenges can result in:

* Overstocking of slow-moving products.
* Stockouts of high-demand products.
* Product expiry and inventory waste.
* Poor purchasing and replenishment decisions.
* Limited visibility of sales trends.
* Difficulty predicting future customer demand.

RetailAI addresses this problem by providing data-driven and AI-assisted decision support for inventory management.

---

## 4. Main Project Objective

The main objective of RetailAI is to design and develop a practical AI-powered inventory management solution that forecasts product demand, supports intelligent restocking decisions, identifies slow-moving and potentially expiring products, and provides an accessible chatbot and dashboard interface for local shop owners.

The solution is intended to help retailers make informed inventory decisions, reduce avoidable stockouts and waste, and improve visibility of their retail operations.

---

## 5. Business Objectives

The project documentation defines the following business objectives:

1. Reduce stockouts of high-demand products by at least 30% within three months of adoption.

2. Decrease inventory holding costs and product expiry losses by approximately 20–25%.

3. Provide weekly and monthly demand forecasts for relevant products.

4. Enable shop owners to query stock and sales information using natural language through a chatbot.

5. Provide a simple visual dashboard displaying current stock levels, predicted demand, reorder recommendations and alerts.

These objectives provide measurable targets against which the proposed solution can be evaluated.

---

## 6. Solution Scope

### 6.1 In Scope

The RetailAI project includes:

* Historical retail sales data analysis.
* Inventory data preparation and analysis.
* Product performance analysis.
* Store performance analysis.
* Sales trend analysis.
* Seasonality analysis.
* Demand forecasting.
* Forecast model evaluation.
* Stockout risk identification.
* Smart restocking recommendations.
* Reorder quantity recommendations.
* Slow-moving product identification.
* Near-expiry product alerts where the required data is available.
* Database design and implementation.
* Python-based AI and machine learning components.
* Natural-language chatbot functionality.
* Dashboard-based presentation of retail information.
* Testing of the developed solution.
* Deployment documentation.
* GitHub-based version control and project management.

### 6.2 Out of Scope

The initial RetailAI solution does not include:

* Automatic purchasing without retailer confirmation.
* Direct banking or payment-system integration.
* Autonomous supplier transactions.
* Physical stock counting using specialised hardware.
* Full enterprise resource planning functionality.
* Guaranteed prediction of customer behaviour.
* Large-scale enterprise retail management.
* Real-time integration with every possible point-of-sale system.

The system is designed as **decision support**, meaning that the retailer remains responsible for final purchasing and inventory decisions.

---

## 7. Target Users

The primary target users are:

* Local spaza shop owners.
* Small grocery shop owners.
* Retail store managers.
* Employees responsible for stock and purchasing decisions.

The interface should be simple and practical because the intended users may have limited exposure to advanced digital and analytical systems.

---

## 8. Core Solution Features

RetailAI will focus on the following major capabilities:

### 8.1 Demand Forecasting

The system will analyse historical sales data and apply suitable forecasting and machine-learning techniques to estimate future product demand.

### 8.2 Smart Restocking

The system will use forecast demand, current stock information and other relevant inventory information to support reorder quantity and replenishment decisions.

### 8.3 Stockout Risk Detection

The system will identify products that may reach insufficient stock levels based on available inventory and predicted demand.

### 8.4 Slow-Moving Product Detection

The system will analyse sales performance to identify products with relatively low movement that may require retailer attention.

### 8.5 Expiry Monitoring

Where expiry-date information is available, the system will identify products approaching expiry and provide appropriate alerts.

### 8.6 Dashboard

A visual dashboard will present relevant sales, inventory, forecasting, recommendation and alert information.

### 8.7 AI Chatbot

A natural-language chatbot will allow users to ask supported questions about stock, sales, forecasts, restocking recommendations and other inventory information.

---

## 9. AI and Technology Scope

The project documentation identifies Python as the primary programming language.

The proposed technology areas include:

* Python.
* Pandas and NumPy for data processing.
* Scikit-learn for machine learning.
* Statsmodels for statistical forecasting.
* Prophet where appropriate.
* TensorFlow/Keras or PyTorch for deep-learning experiments.
* LSTM/GRU models for sequential demand forecasting where sufficient data is available.
* spaCy or NLTK for NLP functionality.
* Streamlit, Gradio or an equivalent lightweight interface for the dashboard and chatbot.
* SQLite or an appropriate database solution for data storage.
* GitHub and GitHub Projects for version control and project management.

The final implementation will select technologies according to project requirements, data availability, feasibility and evaluation results.

---

## 10. Data Scope

The solution may use the following categories of data:

* Historical sales transactions.
* Product information.
* Quantity sold.
* Sales dates and times.
* Revenue or price information.
* Current inventory levels.
* Restocking information.
* Supplier lead-time information where available.
* Product expiry information where available.
* Calendar and seasonal information.
* Stockout and inventory event information.

Synthetic, anonymised or publicly available datasets may be used during development and demonstration where real shop data is unavailable.

---

## 11. Machine Learning and Forecasting Scope

RetailAI will investigate a layered modelling approach.

Possible techniques include:

* Moving Average.
* Exponential Smoothing.
* ARIMA/SARIMA.
* Prophet.
* Random Forest.
* XGBoost or other suitable tree-based models.
* LSTM/GRU deep-learning models.

Models will be evaluated using suitable metrics such as:

* MAPE.
* MAE.
* RMSE.
* R² where applicable.
* Precision, Recall and F1 for relevant classification tasks.

Time-series validation will respect the chronological order of the data to reduce the risk of data leakage.

The final model selection will depend on actual data characteristics and measured performance rather than assuming that the most complex model will always provide the best results.

---

## 12. Chatbot and NLP Scope

The RetailAI chatbot is a core part of the proposed solution.

The chatbot will support relevant retail questions such as:

* Current stock levels.
* Expected product demand.
* Products requiring replenishment.
* Products that may run out of stock.
* Slow-moving products.
* Products approaching expiry where expiry data exists.

The system may use intent classification, entity extraction, rules, retrieval and other appropriate NLP techniques.

Speech recognition and text-to-speech may be considered where feasible within the project scope.

---

## 13. Project Boundaries

RetailAI is a decision-support system rather than an autonomous purchasing system.

The AI models will provide forecasts, alerts and recommendations based on the available data. The shop owner will remain responsible for deciding whether to accept, modify or reject a recommendation.

The system's accuracy will depend on the quality, completeness, volume and relevance of the available data.

Features requiring data that is not available in the selected dataset may be implemented using suitable demonstration data or documented as limitations rather than presented as fully validated capabilities.

---

## 14. Constraints

The project is subject to the following constraints:

* Limited historical retail data.
* Potentially incomplete inventory records.
* Limited hardware and connectivity environments.
* Limited project time within the academic semester.
* Availability of suitable datasets.
* Computational requirements of advanced machine-learning models.
* Limited resources for collecting real-world pilot data.

The project will therefore prioritise practical, explainable and achievable AI functionality.

---

## 15. Key Risks

| Risk                                  | Potential Impact                   | Mitigation                                                                         |
| ------------------------------------- | ---------------------------------- | ---------------------------------------------------------------------------------- |
| Insufficient historical sales data    | Poor forecasting performance       | Use appropriate public, synthetic or anonymised data and establish baseline models |
| Low-quality or incomplete data        | Unreliable analysis                | Apply data validation, cleaning and preprocessing                                  |
| Low digital literacy                  | Difficulty using the system        | Use a simple interface and natural-language interaction                            |
| Internet or power interruptions       | Reduced system availability        | Support local processing where feasible                                            |
| Changing demand patterns              | Model accuracy may decrease        | Monitor performance and periodically retrain models                                |
| Complex models with insufficient data | Overfitting or poor generalisation | Compare advanced models against simpler baselines                                  |
| Limited project time                  | Incomplete implementation          | Prioritise core requirements and maintain milestone-based development              |

---

## 16. Success Criteria

The RetailAI project will be considered successful when the developed solution demonstrates that it can:

1. Process and prepare the selected retail dataset.
2. Analyse historical sales and inventory-related information.
3. Identify meaningful product and sales patterns.
4. Produce demand forecasts using appropriate forecasting or machine-learning techniques.
5. Evaluate forecasting performance using defined metrics.
6. Identify potential stockout situations where sufficient data is available.
7. Generate practical restocking recommendations.
8. Identify slow-moving products.
9. Provide expiry-related alerts where expiry data is available.
10. Provide supported natural-language inventory queries through the chatbot.
11. Present important information through an understandable dashboard.
12. Demonstrate the integration of AI techniques into a practical retail solution.
13. Maintain project evidence and development work through the GitHub repository and GitHub Projects.

---

## 17. Alignment With the Academic Project

RetailAI directly supports the Business Analysis 3.2 project requirements by combining:

* Business analysis.
* Requirements analysis.
* Data analysis.
* Machine learning.
* Time-series forecasting.
* Model evaluation.
* Natural Language Processing.
* Deep learning.
* Chatbot functionality.
* Practical software implementation.

The solution therefore addresses the academic theme **“An AI Solution for Industries”** through a practical application of AI within the **retail industry**.

---

## 18. Scope Approval

This document establishes the project scope, objectives, boundaries, constraints and success criteria used as the foundation for the RetailAI project.

**Milestone:** M01 — Project Foundation & Control
**Issue:** M01-01 — Confirm project scope, objectives and boundaries
**Repository Evidence:** `documentation/00-project/project-scope-and-objectives.md`

**Project:** RetailAI
**Theme:** An AI Solution for Industries
**Industry Sector:** Retail
**Subject:** Business Analysis 3.2 (AIBUY3A)

---

## 19. Source Document

The scope in this repository evidence is derived from the group's **Business Analysis 3.2 Project Documentation — RetailAI**, issued by Vaal University of Technology on **10 August 2026**, with a project submission deadline of **02 November 2026**.

The repository evidence is intended to keep the GitHub project-management work consistent with the group's approved academic project documentation.
