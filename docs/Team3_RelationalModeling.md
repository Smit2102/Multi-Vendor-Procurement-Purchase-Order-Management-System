# Relational Database Modeling
**Project Name:** Procurement System
**Team Number:** 3
**Live Working Project (Test Environment):** [https://procurement-system-peach.vercel.app/](https://procurement-system-peach.vercel.app/)

## 1. Business Rules and Scope

### System Context
This system models a real-world enterprise procurement platform designed to manage the entire lifecycle of purchasing goods from external vendors. It seamlessly oversees employee requests, manager approvals, purchase order formulation by procurement officers, order fulfillment by vendors, and final invoice and payment processing by the finance department.

### Business Rules
1. A **User** is assigned exactly one **Role** and belongs to exactly one **Department**.
2. A **Department** can employ/contain multiple **Users**.
3. An employee (`Users`) can submit multiple **Purchase Requests**.
4. Each **Purchase Request** must belong to a single **Department**.
5. A **Manager** (from `Users`) can review, approve, or reject multiple **Purchase Requests**.
6. A **Purchase Request** can have multiple review records (`PR_Approvals`) and status changes (`PR_Status_History`).
7. A **Procurement Officer** generates **Purchase Orders** derived from approved **Purchase Requests**.
8. A **Purchase Order** must be tied to exactly one **Vendor**.
9. A **Vendor** can fulfill multiple **Purchase Orders** and establish multiple **Contracts**.
10. A **Vendor** can have multiple **Vendor Categories** associated with them.
11. A **Purchase Order** can contain multiple **Line Items**.
12. Upon shipping, a **Purchase Order** generates a **Goods Receipt**, which is logged into the system.
13. The Finance department processes **Invoices** which correspond to shipped **Purchase Orders**.
14. An **Invoice** belongs to one **Vendor**.
15. An **Invoice** can have multiple **Payments** associated with it.
16. **Budget Transactions** are recorded against a Department whenever a **Purchase Order** deducts from the department's budget.
17. Any significant action performed by a User triggers an entry in the **Audit Log**.

### Assumptions
- A Vendor interacts directly with the system through their respective Vendor portal account.
- All purchases operate strictly under budget constraints defined at the Department level.
- Single-currency transactions are assumed as the standard.

### Out-of-Scope Items
- Bank or credit card payment gateway integration (payments are manually recorded for simulation).
- Detailed HR operations and management logic beyond basic department and role assignment.
- Post-procurement inventory tracking and advanced warehouse management capabilities.

## 2. Relational Database Model

### Logical Schema Design
The relational database utilizes a comprehensively normalized schema to minimize data redundancy and prevent partial or transitive dependencies (satisfying Third Normal Form - 3NF). 
- **Authentication & Authorization**: Handled via `Users`, `Roles`, and `Departments`.
- **Procurement Workflow**: Anchored by `Purchase_Requests`, tracked dynamically through `PR_Approvals` and `PR_Status_History`.
- **Vendor & Order Fulfillments**: Centralized by `Vendors`, `Vendor_Categories`, and `Contracts` which feed logically into `Purchase_Orders`, `PO_Line_Items`, and `Goods_Receipt`.
- **Finance**: Administered strictly by `Invoices`, `Payments`, and `Budget_Transactions`.
- **System Traceability**: Accounted for dynamically by `Audit_Log` and `Notifications`.

### Entities & Relationships
- **Users (1) to (N) Purchase_Requests**
- **Departments (1) to (N) Purchase_Requests**
- **Purchase_Requests (1) to (N) PR_Approvals**
- **Purchase_Requests (1) to (N) PR_Status_History**
- **Purchase_Requests (1) to (N) Purchase_Orders**
- **Vendors (1) to (N) Purchase_Orders**
- **Vendors (1) to (N) Invoices**
- **Purchase_Orders (1) to (N) PO_Line_Items**
- **Purchase_Orders (1) to (1) Goods_Receipt**
- **Purchase_Orders (1) to (N) Invoices**
- **Invoices (1) to (N) Payments**

## 3. Data Dictionary

*A definitive breakdown of core entities, attributes, and constraints deployed within the relational system.*

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Roles** | `role_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `role_name` | TEXT | - | NOT NULL | UNIQUE |
| | `permissions_json` | TEXT | - | NULL | - |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Departments** | `dept_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `dept_name` | TEXT | - | NOT NULL | - |
| | `budget_allocated` | REAL | - | NULL | DEFAULT 0 |
| | `budget_used` | REAL | - | NULL | DEFAULT 0 |
| | `manager_id` | INTEGER | FK | NULL | REFERENCES Users(user_id) |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Users** | `user_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `name` | TEXT | - | NOT NULL | - |
| | `email` | TEXT | - | NOT NULL | UNIQUE |
| | `role` | INTEGER | FK | NULL | REFERENCES Roles(role_id) |
| | `department_id`| INTEGER | FK | NULL | REFERENCES Departments(dept_id)|
| | `created_at` | TIMESTAMP | - | NULL | DEFAULT CURRENT_TIMESTAMP |
| | `is_active` | BOOLEAN | - | NULL | DEFAULT 1 |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Purchase_Requests**| `pr_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `employee_id`| INTEGER | FK | NULL | REFERENCES Users(user_id) |
| | `dept_id` | INTEGER | FK | NULL | REFERENCES Departments(dept_id)|
| | `item_name` | TEXT | - | NOT NULL | - |
| | `description` | TEXT | - | NULL | - |
| | `quantity` | INTEGER | - | NOT NULL | - |
| | `estimated_cost`| REAL | - | NULL | - |
| | `status` | TEXT | - | NULL | DEFAULT 'PENDING' |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **PR_Approvals** | `approval_id`| INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `pr_id` | INTEGER | FK | NULL | REFERENCES Purchase_Requests(pr_id) |
| | `manager_id` | INTEGER | FK | NULL | REFERENCES Users(user_id) |
| | `decision` | TEXT | - | NULL | - |
| | `comments` | TEXT | - | NULL | - |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Vendors** | `vendor_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `company_name` | TEXT | - | NOT NULL | - |
| | `contact_name` | TEXT | - | NULL | - |
| | `email` | TEXT | - | NULL | - |
| | `rating` | INTEGER | - | NULL | - |
| | `is_active` | BOOLEAN | - | NULL | DEFAULT 1 |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Purchase_Orders** | `po_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `pr_id` | INTEGER | FK | NULL | REFERENCES Purchase_Requests(pr_id) |
| | `vendor_id` | INTEGER | FK | NULL | REFERENCES Vendors(vendor_id) |
| | `procurement_officer_id`| INTEGER| FK | NULL | REFERENCES Users(user_id) |
| | `delivery_due_date`| TEXT | - | NULL | - |
| | `total_amount` | REAL | - | NULL | - |
| | `status` | TEXT | - | NULL | DEFAULT 'ISSUED' |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Invoices** | `invoice_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `po_id` | INTEGER | FK | NULL | REFERENCES Purchase_Orders(po_id) |
| | `vendor_id` | INTEGER | FK | NULL | REFERENCES Vendors(vendor_id) |
| | `due_date` | TEXT | - | NULL | - |
| | `amount` | REAL | - | NULL | - |
| | `status` | TEXT | - | NULL | DEFAULT 'PENDING' |

| Table | Column Name | Data Type | Key Form | Null Constraints | Default Rules & Foreign Checks |
|-------|-------------|-----------|----------|-----------------|----------------------|
| **Payments** | `payment_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT |
| | `invoice_id` | INTEGER | FK | NULL | REFERENCES Invoices(invoice_id) |
| | `paid_by` | INTEGER | FK | NULL | REFERENCES Users(user_id) |
| | `amount_paid` | REAL | - | NULL | - |
| | `payment_method` | TEXT | - | NULL | - |

*(Peripheral system tables tracking historical operations—such as `PR_Status_History`, `Vendor_Categories`, `PO_Line_Items`, `Goods_Receipt`, `Budget_Transactions`, `Audit_Log`, `Notifications`—implicitly adhere to identical structural compliance bindings regarding standard foreign keys and nullable directives).*

## 5. Additional Tables Data Dictionary

| Table | Column Name | Data Type | Key Form | Null Constraints | Description |
|-------|-------------|-----------|----------|-----------------|-------------|
| **PR_Status_History** | `history_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | Tracks status changes of purchase requests over time |
| | `pr_id` | INTEGER | FK | NOT NULL | References Purchase_Requests(pr_id) |
| | `status` | TEXT | - | NOT NULL | Current status |
| | `changed_at` | TIMESTAMP | - | NOT NULL | Timestamp of change |
| **Vendor_Categories** | `vc_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | Links vendors to categories (M:N) |
| | `vendor_id` | INTEGER | FK | NOT NULL | References Vendors(vendor_id) |
| | `category_name` | TEXT | - | NOT NULL | Category name |
| **Contracts** | `contract_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | Formal agreements with vendors |
| | `vendor_id` | INTEGER | FK | NOT NULL | References Vendors(vendor_id) |
| | `start_date` | DATE | - | NOT NULL | Contract start |
| | `end_date` | DATE | - | NULL | Contract end |
| **PO_Line_Items** | `line_item_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | Individual items within a purchase order |
| | `po_id` | INTEGER | FK | NOT NULL | References Purchase_Orders(po_id) |
| | `product_name` | TEXT | - | NOT NULL | Name of product |
| | `quantity` | INTEGER | - | NOT NULL | Quantity ordered |
| | `unit_price` | REAL | - | NOT NULL | Price per unit |
| **Budget_Transactions** | `bt_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | Records budget usage per department |
| | `dept_id` | INTEGER | FK | NOT NULL | References Departments(dept_id) |
| | `amount` | REAL | - | NOT NULL | Transaction amount |
| | `transaction_date` | TIMESTAMP | - | NOT NULL | Date of transaction |
| **Audit_Log** | `log_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | System audit entries for actions |
| | `user_id` | INTEGER | FK | NOT NULL | References Users(user_id) |
| | `action` | TEXT | - | NOT NULL | Description of action |
| | `timestamp` | TIMESTAMP | - | NOT NULL | When action occurred |
| **Notifications** | `notification_id` | INTEGER | PK | NOT NULL | AUTOINCREMENT | User notifications |
| | `user_id` | INTEGER | FK | NOT NULL | References Users(user_id) |
| | `message` | TEXT | - | NOT NULL | Notification content |
| | `is_read` | BOOLEAN | - | NOT NULL | Read status |
| | `created_at` | TIMESTAMP | - | NOT NULL | Creation time |

## 4. Entity-Relationship Diagram (ERD)

<!-- DO NOT REMOVE: ERD diagram -->
![Procurement ERD](file:///C:/Users/nisar/.gemini/antigravity/brain/64f10d36-d523-42a1-9217-9e5fc64a0bd7/procurement_erd_1773792198549.png)
