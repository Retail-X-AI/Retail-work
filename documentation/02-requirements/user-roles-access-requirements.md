# User Roles and Access Requirements

## 1. Introduction

This document identifies the intended users of Retail-X-AI and describes how the system supports their retail analysis and decision-making activities.

Retail-X-AI is currently implemented as a Python-based system that processes retail data and produces analytical results, recommendations and chatbot responses.

The document distinguishes the intended users of the system from access-control features that have not been implemented.

## 2. User Roles

### 2.1 Shop Owner / Manager

The Shop Owner / Manager is the primary intended user of Retail-X-AI.

The system supports this user by providing:

- Historical sales analysis.
- Demand estimates.
- Inventory and restocking recommendations.
- Potential stockout-risk analysis.
- Additional machine learning analysis.
- Supplier recommendations.
- Natural-language chatbot assistance.

The Shop Owner / Manager uses these outputs to support retail inventory and purchasing decisions.

### 2.2 System Administrator

A system administrator may be responsible for maintaining the Python environment, project configuration, datasets and application components.

However, a separate administrator account, user-management interface and role-based authentication system are not implemented in the current project.

## 3. User and System Function Mapping

| System Function | Shop Owner / Manager | System Administrator |
|---|---|---|
| Load and prepare retail data | Intended user | Technical maintenance |
| Analyse historical demand | Intended user | Technical maintenance |
| Generate demand estimates | Intended user | Technical maintenance |
| Analyse inventory and restocking requirements | Intended user | Technical maintenance |
| Identify potential stockout risks | Intended user | Technical maintenance |
| Perform additional AI-based analysis | Intended user | Technical maintenance |
| Generate supplier recommendations | Intended user | Technical maintenance |
| Interact with natural-language chatbot | Intended user | Technical maintenance |

## 4. Access and Security Considerations

Retail-X-AI currently operates through Python components and does not implement a user authentication or role-based access control system.

The following are therefore security considerations for possible future development, not implemented system capabilities:

- User authentication.
- Individual user accounts.
- Role identification.
- Permission-based access restrictions.
- Secure user sessions and logout.
- Administrative user management.
- User-specific business data access.

The project should not claim that these controls are operational.

## 5. Functional Requirement Mapping

The intended Shop Owner / Manager use cases correspond to the eight functional requirements:

| Functional Requirement | Description |
|---|---|
| FR-01 | Load and Prepare Retail Data |
| FR-02 | Analyse Historical Demand |
| FR-03 | Generate Demand Estimates |
| FR-04 | Analyse Inventory and Restocking Requirements |
| FR-05 | Identify Potential Stockout Risks |
| FR-06 | Perform Additional AI-Based Retail Analysis |
| FR-07 | Recommend Suppliers |
| FR-08 | Provide a Natural-Language Chatbot |

These requirements describe the system's analytical and AI capabilities rather than a graphical user-access interface.

## 6. Scope Limitations

The current implementation does not include:

- User registration or login.
- Administrator account management.
- Role-based permission enforcement.
- A graphical dashboard.
- A browser-based user interface.
- User-specific sessions.

These functions are outside the implemented project scope.

## 7. Conclusion

The Shop Owner / Manager is the primary intended user of Retail-X-AI. The system supports retail decision-making through data preparation, demand analysis, forecasting, inventory analysis, supplier recommendations and chatbot functionality.

System administration relates to the technical maintenance of the Python project. Authentication and role-based access control are documented as possible future considerations and are not claimed as implemented features.