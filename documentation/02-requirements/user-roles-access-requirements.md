# User Roles and Access Requirements

## 1. Introduction

Retail-X-AI requires clearly defined user roles and access permissions so that users can access the functions relevant to their responsibilities.

Access control helps protect business information and ensures that system functions are only used by authorised users.

The main business user of Retail-X-AI is the Shop Owner / Manager. This user manages retail information, monitors inventory, views demand forecasts, receives restocking recommendations and interacts with the AI assistant.

An Administrator role is included for system-level administration and user management.

---

## 2. User Roles

### 2.1 Shop Owner / Manager

The Shop Owner / Manager is the primary business user of Retail-X-AI.

The user is responsible for managing the shop's products, sales and inventory information and using the system's analytics and AI features to support purchasing and stock-management decisions.

The Shop Owner / Manager can:

- Log into the system.
- Manage product information.
- Record sales information.
- View current inventory levels.
- View sales and inventory trends.
- View demand forecasts.
- View stockout risk information.
- View recommended reorder quantities.
- View slow-moving products.
- View product attention and alert information.
- Use the AI assistant to ask questions about the shop's retail information.
- Create grocery lists and receive purchase suggestions through the AI assistant.
- Ask for grocery suggestions based on a stated budget.
- Compare products and purchasing priorities.
- View the Retail-X-AI dashboard.
- View system-generated alerts and recommendations.

### 2.2 Administrator

The Administrator is responsible for system-level administration.

The Administrator can:

- Log into the system.
- Manage authorised user accounts.
- Manage user roles and access permissions.
- Manage system settings where required.
- Monitor system access.
- Maintain administrative information required for the operation of Retail-X-AI.

The Administrator does not replace the Shop Owner / Manager's normal business activities. Business users remain responsible for managing and interpreting their own shop information.

---

## 3. Role-Based Access Requirements

Access to Retail-X-AI functions shall be controlled according to the user's assigned role.

| System Function | Shop Owner / Manager | Administrator |
|---|---|---|
| Login | Yes | Yes |
| Manage products | Yes | Yes |
| Record sales | Yes | Yes |
| View inventory | Yes | Yes |
| View sales information | Yes | Yes |
| View demand forecasts | Yes | Yes |
| View stockout risk | Yes | Yes |
| View restocking recommendations | Yes | Yes |
| View slow-moving products | Yes | Yes |
| View alerts | Yes | Yes |
| Use AI assistant | Yes | Yes |
| Create grocery lists | Yes | Yes |
| Request budget-based grocery suggestions | Yes | Yes |
| Compare products | Yes | Yes |
| View dashboard | Yes | Yes |
| Manage user accounts | No | Yes |
| Manage user roles and permissions | No | Yes |
| Manage system-level settings | No | Yes |

---

## 4. Access Control Requirements

### AR-01 — User Authentication

The system shall require users to authenticate before accessing protected Retail-X-AI functions.

### AR-02 — Role Identification

The system shall identify the role assigned to each authenticated user.

### AR-03 — Role-Based Access

The system shall provide access to system functions according to the permissions associated with the user's role.

### AR-04 — Restricted Functions

The system shall prevent users from accessing functions that are not authorised for their assigned role.

### AR-05 — Business Data Protection

The system shall protect sales, inventory, product and other business information from unauthorised access.

### AR-06 — Session Security

The system shall provide a secure logout mechanism so that users can end their authenticated session.

### AR-07 — Administrative Access

Only authorised administrators shall be permitted to manage user accounts, roles and system-level access settings.

### AR-08 — Access Consistency

The same role shall receive consistent permissions across the Retail-X-AI system.

---

## 5. Role and Functional Requirement Mapping

The user roles are mapped to the functional requirements defined for Retail-X-AI.

| Functional Requirement | Description | Shop Owner / Manager | Administrator |
|---|---|---|---|
| FR-01 | Capture Sales and Stock Data | Yes | Yes |
| FR-02 | Generate Demand Forecast | Yes | Yes |
| FR-03 | Calculate Recommended Reorder Quantities | Yes | Yes |
| FR-04 | Identify Slow-Moving and Near-Expiry Products | Yes | Yes |
| FR-05 | Interact with Natural-Language AI Assistant | Yes | Yes |
| FR-06 | View Interactive Dashboard | Yes | Yes |

The Shop Owner / Manager is the primary user of the business functions represented by FR-01 to FR-06.

The Administrator has access where necessary to support system operation and administration.

---

## 6. Access Rules

The following access rules apply to Retail-X-AI:

1. A user must authenticate before accessing protected system functions.
2. Each user must have an assigned role.
3. A user may only access functions permitted by their assigned role.
4. Shop Owners / Managers may access business and analytical functions required to operate and monitor the shop.
5. Administrators may manage authorised users and system-level access.
6. Users must not be able to access restricted administrative functions unless they have the required permissions.
7. Business information must only be available to authorised users.
8. Users should log out when they have finished using the system.

---

## 7. Verification and Evidence

The access requirements will be verified by reviewing the role-permission matrix and confirming that each system function has an appropriate access permission.

The following evidence will be provided for this milestone:

- User roles documented.
- Shop Owner / Manager permissions documented.
- Administrator permissions documented.
- Role-based access matrix completed.
- Access control requirements AR-01 to AR-08 documented.
- Functional requirements mapped to user roles.
- Access rules documented.
- Document saved in `documentation/02-requirements/`.
- Git commit containing issue ID `M04-03`.
- Pull request linked to the M04-03 issue.
- Review completed before merging.

---

## 8. Conclusion

Defining user roles and access requirements ensures that Retail-X-AI provides users with the functions they need while protecting business information from unauthorised access.

The Shop Owner / Manager has access to the main business, inventory, forecasting and AI functions, while the Administrator is responsible for user management and system-level administration.

The role-based access requirements provide a clear foundation for implementing secure and consistent access control within Retail-X-AI.
