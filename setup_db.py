import sqlite3
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_PATH = 'procurement.db'

def create_database():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()
    else:
        print("Connecting to SQLite...")
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
    def execute_query(query, params=None):
        if db_url:
            if '?' in query: query = query.replace('?', '%s')
            query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
            query = query.replace('BOOLEAN DEFAULT 1', 'BOOLEAN DEFAULT TRUE')
            query = query.replace('BOOLEAN DEFAULT 0', 'BOOLEAN DEFAULT FALSE')
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

    # 1. User & Auth
    execute_query('''
    CREATE TABLE Roles (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT UNIQUE NOT NULL,
        permissions_json TEXT
    )
    ''')
    
    execute_query('''
    CREATE TABLE Departments (
        dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dept_name TEXT NOT NULL,
        budget_allocated REAL DEFAULT 0,
        budget_used REAL DEFAULT 0,
        manager_id INTEGER
    )
    ''')

    execute_query('''
    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role INTEGER,
        department_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY (role) REFERENCES Roles(role_id),
        FOREIGN KEY (department_id) REFERENCES Departments(dept_id)
    )
    ''')

    execute_query('''
    CREATE TABLE Audit_Log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        table_affected TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # 2. Purchase Requests
    execute_query('''
    CREATE TABLE Purchase_Requests (
        pr_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        dept_id INTEGER,
        item_name TEXT NOT NULL,
        description TEXT,
        quantity INTEGER NOT NULL,
        estimated_cost REAL,
        status TEXT DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES Users(user_id),
        FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
    )
    ''')

    execute_query('''
    CREATE TABLE PR_Approvals (
        approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_id INTEGER,
        manager_id INTEGER,
        decision TEXT,
        comments TEXT,
        decided_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pr_id) REFERENCES Purchase_Requests(pr_id),
        FOREIGN KEY (manager_id) REFERENCES Users(user_id)
    )
    ''')

    execute_query('''
    CREATE TABLE PR_Status_History (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_id INTEGER,
        old_status TEXT,
        new_status TEXT,
        changed_by INTEGER,
        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (pr_id) REFERENCES Purchase_Requests(pr_id),
        FOREIGN KEY (changed_by) REFERENCES Users(user_id)
    )
    ''')

    # 3. Vendors & Contracts
    execute_query('''
    CREATE TABLE Vendors (
        vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        contact_name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        rating INTEGER,
        is_active BOOLEAN DEFAULT 1
    )
    ''')

    execute_query('''
    CREATE TABLE Vendor_Categories (
        vc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        category_name TEXT,
        FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id)
    )
    ''')

    execute_query('''
    CREATE TABLE Contracts (
        contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        payment_terms TEXT,
        max_value REAL,
        status TEXT,
        FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id)
    )
    ''')

    # 4. Purchase Orders
    execute_query('''
    CREATE TABLE Purchase_Orders (
        po_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_id INTEGER,
        vendor_id INTEGER,
        procurement_officer_id INTEGER,
        issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        delivery_due_date TEXT,
        status TEXT DEFAULT 'ISSUED',
        total_amount REAL,
        FOREIGN KEY (pr_id) REFERENCES Purchase_Requests(pr_id),
        FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id),
        FOREIGN KEY (procurement_officer_id) REFERENCES Users(user_id)
    )
    ''')

    execute_query('''
    CREATE TABLE PO_Line_Items (
        line_id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_id INTEGER,
        item_description TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        FOREIGN KEY (po_id) REFERENCES Purchase_Orders(po_id)
    )
    ''')

    execute_query('''
    CREATE TABLE Goods_Receipt (
        gr_id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_id INTEGER,
        received_by INTEGER,
        received_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        quantity_received INTEGER,
        condition_notes TEXT,
        FOREIGN KEY (po_id) REFERENCES Purchase_Orders(po_id),
        FOREIGN KEY (received_by) REFERENCES Users(user_id)
    )
    ''')

    # 5. Invoices & Payments
    execute_query('''
    CREATE TABLE Invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        po_id INTEGER,
        vendor_id INTEGER,
        invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date TEXT,
        amount REAL,
        status TEXT DEFAULT 'PENDING',
        FOREIGN KEY (po_id) REFERENCES Purchase_Orders(po_id),
        FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id)
    )
    ''')

    execute_query('''
    CREATE TABLE Payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        paid_by INTEGER,
        payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount_paid REAL,
        payment_method TEXT,
        reference_no TEXT,
        FOREIGN KEY (invoice_id) REFERENCES Invoices(invoice_id),
        FOREIGN KEY (paid_by) REFERENCES Users(user_id)
    )
    ''')

    execute_query('''
    CREATE TABLE Budget_Transactions (
        txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dept_id INTEGER,
        po_id INTEGER,
        amount REAL,
        transaction_type TEXT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (dept_id) REFERENCES Departments(dept_id),
        FOREIGN KEY (po_id) REFERENCES Purchase_Orders(po_id)
    )
    ''')

    # 6. Notifications & Reporting
    execute_query('''
    CREATE TABLE Notifications (
        notif_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        is_read BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        link_to TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    execute_query('''
    CREATE TABLE Saved_Reports (
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        generated_by INTEGER,
        report_type TEXT,
        filters_json TEXT,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_path TEXT,
        FOREIGN KEY (generated_by) REFERENCES Users(user_id)
    )
    ''')

    # Insert Default Roles
    roles = ['Employee', 'Manager', 'Procurement', 'Vendor', 'Finance', 'SuperAdmin']
    for r in roles:
        execute_query("INSERT INTO Roles (role_name) VALUES (?)", (r,))
    
    # FIX REC 13: Insert Department WITHOUT manager_id to avoid FK violation
    # (Manager user doesn't exist yet at this point)
    execute_query("INSERT INTO Departments (dept_name, budget_allocated, budget_used) VALUES ('IT Department', 100000, 0)")

    # Insert Default Users so they can log in 
    users = [
        ('Test Employee', 'employee@test.com', 1, 1),
        ('Test Manager', 'manager@test.com', 2, 1),
        ('Test Procure', 'procurement@test.com', 3, 1),
        ('Test Vendor', 'vendor@test.com', 4, 1),
        ('Test Finance', 'finance@test.com', 5, 1),
        ('Test Admin', 'admin@test.com', 6, 1)
    ]
    for uid, u in enumerate(users):
        execute_query("INSERT INTO Users (name, email, role, department_id) VALUES (?, ?, ?, ?)", u)

    # FIX REC 13: NOW update manager_id — user_id=2 (Manager) exists at this point
    execute_query("UPDATE Departments SET manager_id = 2 WHERE dept_name = 'IT Department'")
        
    # Insert a Dummy Vendor entry for the Vendor user
    execute_query("INSERT INTO Vendors (company_name, contact_name, email, phone, address, rating) VALUES ('Tech Supplies Inc', 'Alice', 'vendor@test.com', '123-456', '123 Main st', 5)")

    conn.commit()
    conn.close()
    print("Database Setup Complete.")

if __name__ == "__main__":
    create_database()
