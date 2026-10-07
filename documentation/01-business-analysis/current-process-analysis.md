# Retail-X-AI Current Process Analysis

## 1. Introduction

Retail-X-AI is designed to improve inventory management for small spaza shops and local grocery stores in South African townships.

Before implementing Retail-X-AI, many small shops may rely on manual processes, personal experience and basic records to manage products, sales and stock.

This document analyses the current inventory management process and identifies the problems that the Retail-X-AI system is intended to address.

The analysis focuses on the current processes for:

• Product management

• Stock management

• Sales recording

• Stock monitoring

• Purchasing and restocking

• Expiry monitoring

• Sales analysis

• Business decision making

---

# 2. Current Business Environment

A typical small shop manages a range of products such as:

• Food products

• Beverages

• Household products

• Personal care products

• Snacks

• Basic groceries

The shop owner or employees are responsible for selling products, monitoring stock and purchasing replacement stock.

In a manual or partially manual environment, inventory decisions may depend heavily on the owner's experience and observations.

For example, the owner may notice that a particular product is selling quickly and decide to purchase more of it.

However, there may not be a formal system calculating:

• Historical sales

• Sales trends

• Future demand

• Stockout risk

• Recommended reorder quantity

• Slow-moving products

• Expiry risk

---

# 3. Current Process: Product Management

The current product management process can involve the following steps:

1. The shop purchases products from a supplier.

2. Products arrive at the shop.

3. The shop owner or employee identifies the products.

4. Product information may be recorded manually or remembered by the owner.

5. Products are placed in storage or on shelves.

6. When products are sold, the available quantity decreases.

7. When new stock arrives, the quantity increases.

The level of formal record keeping can vary between shops.

### Current Problems

• Product information may not be recorded consistently.

• Product quantities may not always be accurate.

• Product information may be stored in different places.

• Employees may have different ways of recording information.

• There may be no central product database.

---

# 4. Current Process: Sales

A typical sales process is:

```text
Customer selects product
        ↓
Employee processes sale
        ↓
Customer pays
        ↓
Product is given to customer
        ↓
Stock decreases
```

Depending on the shop's existing practices, the sale may be recorded using a cash register, point-of-sale system, notebook or another manual method.

Where sales are not stored in a structured system, historical sales information may be difficult to analyse.

### Current Problems

• Sales information may not be recorded consistently.

• Historical sales may be difficult to retrieve.

• Sales trends may not be visible.

• Product demand may be estimated from memory.

• There may be limited information available for forecasting.

---

# 5. Current Process: Inventory Management

The current inventory process generally involves:

```text
Stock received
      ↓
Stock placed in shop/storage
      ↓
Products sold
      ↓
Stock decreases
      ↓
Owner observes remaining stock
      ↓
Owner decides whether to purchase more
```

The owner may physically inspect shelves or storage areas to determine which products need replenishment.

### Current Problems

• Stock quantities may not be updated immediately.

• Physical stock and recorded stock may differ.

• Low-stock products may not be identified early.

• Stock levels may depend on manual observation.

• There may be no automated stock alerts.

---

# 6. Current Process: Restocking

The current restocking process may follow:

```text
Owner checks shelves/storage
        ↓
Identifies products that appear low
        ↓
Considers recent sales or personal experience
        ↓
Contacts supplier or visits supplier
        ↓
Purchases stock
        ↓
Receives stock
        ↓
Places products in shop/storage
```

The decision about how much stock to purchase may be based on:

• Previous experience

• Current stock level

• Recent customer demand

• Available money

• Supplier availability

• Expected customer demand

### Current Problems

The current process does not necessarily provide a formal calculation of:

• Expected future demand

• Required safety stock

• Reorder quantity

• Stockout risk

• Supplier lead time

This can contribute to both overstocking and understocking.

---

# 7. Current Process: Stockout Management

A stockout occurs when a product is unavailable when a customer wants to purchase it.

The current process may be:

```text
Customer requests product
        ↓
Employee checks shelf/storage
        ↓
Product unavailable
        ↓
Employee informs customer
        ↓
Owner becomes aware of shortage
        ↓
Product is added to next purchase
```

In some cases, the owner may only become aware of a stock problem after the product has already run out.

### Current Problems

• No early stockout warning.

• Lost sales may occur.

• Customers may purchase the product elsewhere.

• Emergency purchasing may be required.

• The owner may not know which products are most likely to run out next.

---

# 8. Current Process: Slow-Moving Products

Slow-moving products are products that sell at a relatively low rate compared with other products.

The current process may involve the owner noticing that certain products remain on shelves for a long time.

The owner may then decide to:

• Reduce future purchases.

• Change the product's shelf position.

• Offer a promotion.

• Keep the existing stock until it sells.

### Current Problems

There may be no systematic analysis of:

• Sales frequency

• Sales velocity

• Historical sales

• Current inventory

• Time since last sale

This makes it difficult to consistently identify slow-moving products.

---

# 9. Current Process: Expiry Monitoring

For products with expiry dates, the shop owner or employee may manually inspect products and their expiry dates.

The process may be:

```text
Products stored/displayed
        ↓
Employee checks expiry dates
        ↓
Products approaching expiry identified
        ↓
Owner decides what action to take
```

Possible actions may include:

• Moving products to a more visible position.

• Prioritising their sale.

• Reducing future purchases.

• Removing expired products.

### Current Problems

• Expiry checks may not happen consistently.

• Products approaching expiry may be missed.

• There may be no automatic warning.

• Expired products can result in financial losses.

---

# 10. Current Process: Sales Analysis

Historical sales information may be reviewed manually or based on the owner's experience.

The owner may ask questions such as:

• Which products sell the most?

• Which products sell slowly?

• What products should I buy?

• What products are popular during certain periods?

The answers may depend on personal observation rather than systematic analysis.

### Current Problems

• Limited historical analysis.

• No automated sales trends.

• No demand forecasting.

• Decisions may rely heavily on experience.

• It may be difficult to compare products objectively.

---

# 11. Current Decision-Making Process

The current decision-making process can be represented as:

```text
Sales and stock activity
          ↓
Owner observes shop
          ↓
Owner considers experience
          ↓
Owner estimates demand
          ↓
Owner decides what to purchase
          ↓
Stock is purchased
```

This approach can work for basic shop operations but becomes difficult as the number of products and transactions increases.

---

# 12. Current Process Problems

The analysis identifies several important problems.

| Area                 | Current Process                          | Problem                                          |
| -------------------- | ---------------------------------------- | ------------------------------------------------ |
| Product management   | Manual or informal records               | Product information may be inconsistent          |
| Sales                | Manual or basic recording                | Limited historical analysis                      |
| Inventory            | Physical/manual checking                 | Stock levels may become inaccurate               |
| Restocking           | Owner decides what to purchase           | Reorder quantities may be difficult to calculate |
| Stockouts            | Identified after or near stock depletion | Lost sales may occur                             |
| Slow-moving products | Identified through observation           | No systematic classification                     |
| Expiry               | Manual checking                          | Expiry warnings may be missed                    |
| Forecasting          | Based mainly on experience               | Future demand is difficult to estimate           |
| Reporting            | Manual observation                       | Limited business visibility                      |
| Decision making      | Experience and available information     | Decisions may lack data-supported analysis       |

---

# 13. Current Process Summary

The current process can be summarised as:

```text
PRODUCTS
   ↓
STOCK RECEIVED
   ↓
PRODUCTS SOLD
   ↓
STOCK DECREASES
   ↓
OWNER CHECKS STOCK
   ↓
OWNER ESTIMATES DEMAND
   ↓
RESTOCKING DECISION
   ↓
PURCHASE STOCK
   ↓
STOCK RECEIVED
   ↓
PROCESS REPEATS
```

The main limitation is that much of the decision-making process occurs after the owner observes what has already happened.

---

# 14. Current Process vs Retail-X-AI

| Current Process                     | Retail-X-AI Proposed Process               |
| ----------------------------------- | ------------------------------------------ |
| Manual stock observation            | Central inventory information              |
| Experience-based decisions          | Data-supported decisions                   |
| Manual stock checks                 | Stock monitoring                           |
| Limited sales analysis              | Sales analytics                            |
| No formal demand forecast           | Demand forecasting                         |
| Stockout discovered late            | Stockout alerts                            |
| Manual reorder decision             | Restocking recommendations                 |
| Manual expiry checking              | Expiry warnings                            |
| Informal slow-moving identification | Slow-moving product analysis               |
| Limited reporting                   | Dashboard                                  |
| Questions answered from experience  | AI assistant using available business data |

---

# 15. Opportunities for Improvement

The current process provides several opportunities for Retail-X-AI to improve inventory management.

### 15.1 Improve Inventory Visibility

The system should provide a central view of current stock levels and product information.

### 15.2 Improve Sales Analysis

Historical sales should be stored and analysed to identify sales patterns and product performance.

### 15.3 Introduce Demand Forecasting

Available historical sales data can be used to estimate future demand where sufficient data exists.

### 15.4 Introduce Stockout Alerts

The system should identify products that may run out based on current stock and expected demand.

### 15.5 Support Restocking Decisions

The system should calculate or recommend reorder quantities using defined project rules.

### 15.6 Identify Slow-Moving Products

The system should analyse sales behaviour and identify products with low sales activity.

### 15.7 Improve Expiry Monitoring

The system should identify products approaching their expiry dates and provide warnings.

### 15.8 Improve Business Visibility

A dashboard should bring important sales, inventory, forecasting and alert information together.

---

# 16. Business Analysis Conclusion

The current process analysis shows that inventory management in a small shop can involve several manual activities and decisions based heavily on available information and owner experience.

The main areas requiring improvement are inventory visibility, sales analysis, stockout identification, demand forecasting, restocking decisions, slow-moving product identification and expiry monitoring.

Retail-X-AI is intended to provide a more structured approach by connecting inventory and sales data with analytics, forecasting, alerts and restocking recommendations.

The current process analysis will be used as an input into the next stages of the project, particularly business requirements, functional requirements, system analysis and system design.
