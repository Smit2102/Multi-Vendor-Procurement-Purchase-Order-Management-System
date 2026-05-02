import sqlite3
import random
from datetime import datetime, timedelta
import pytz

CT = pytz.timezone('US/Central')

def random_date(days_back=30):
    now = datetime.now(CT)
    delta = timedelta(days=random.randint(0, days_back), hours=random.randint(0, 23))
    return (now - delta).strftime('%Y-%m-%d %H:%M:%S')

def insert_dummy():
    conn = sqlite3.connect('procurement.db')
    cursor = conn.cursor()

    # Create more vendors
    vendors = [
        ('Office Supplies Co', 'Bob', 'bob@office.com', '555-0101', '456 East St', 4),
        ('Global Logistics', 'Carol', 'carol@global.com', '555-0102', '789 West St', 3),
        ('Enterprise Hardware', 'Dave', 'dave@eh.com', '555-0103', '101 North St', 5)
    ]
    for v in vendors:
        cursor.execute("INSERT INTO Vendors (company_name, contact_name, email, phone, address, rating) VALUES (?, ?, ?, ?, ?, ?)", v)
    
    # Needs some departments
    cursor.execute("INSERT INTO Departments (dept_name, budget_allocated, budget_used, manager_id) VALUES ('HR Department', 50000, 0, 2)")
    cursor.execute("INSERT INTO Departments (dept_name, budget_allocated, budget_used, manager_id) VALUES ('Finance Department', 75000, 0, 2)")

    items = [
        ("Office Chair", 150.00),
        ("Monitor 27-inch", 250.00),
        ("Ergonomic Keyboard", 80.00),
        ("Standing Desk", 450.00),
        ("Developer Laptop", 1800.00),
        ("Conference Screen", 1200.00),
        ("Coffee Machine", 300.00),
        ("Printer Ink", 45.00),
        ("Whiteboard", 120.00),
        ("Networking Cables", 55.00)
    ]

    for _ in range(15):
        item, price = random.choice(items)
        qty = random.randint(1, 5)
        status = random.choice(['PENDING', 'APPROVED', 'REJECTED'])
        dt = random_date()
        
        cursor.execute('''INSERT INTO Purchase_Requests 
            (employee_id, dept_id, item_name, description, quantity, estimated_cost, status, created_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (1, 1, item, "Dummy Request", qty, price, status, dt))
        pr_id = cursor.lastrowid

        if status in ['APPROVED', 'REJECTED']:
            cursor.execute('''INSERT INTO PR_Approvals 
                (pr_id, manager_id, decision, comments, decided_at) VALUES (?, ?, ?, ?, ?)''',
                (pr_id, 2, status, "Reviewed automatically", dt))

        if status == 'APPROVED':
            po_status = random.choice(['ISSUED', 'SHIPPED', 'INVOICED', 'PAID'])
            vendor = random.randint(1, 4)
            cursor.execute('''INSERT INTO Purchase_Orders 
                (pr_id, vendor_id, procurement_officer_id, issue_date, delivery_due_date, status, total_amount) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (pr_id, vendor, 3, dt, (datetime.now(CT) + timedelta(days=7)).strftime('%Y-%m-%d'), po_status, price * qty))
            po_id = cursor.lastrowid

            if po_status in ['SHIPPED', 'INVOICED', 'PAID']:
                cursor.execute('''INSERT INTO Goods_Receipt 
                    (po_id, received_by, received_date, quantity_received, condition_notes) VALUES (?, ?, ?, ?, ?)''',
                    (po_id, 3, dt, qty, "Looks good"))

            if po_status in ['INVOICED', 'PAID']:
                cursor.execute('''INSERT INTO Invoices 
                    (po_id, vendor_id, invoice_date, due_date, amount, status) VALUES (?, ?, ?, ?, ?, ?)''',
                    (po_id, vendor, dt, (datetime.now(CT) + timedelta(days=14)).strftime('%Y-%m-%d'), price * qty, 'PAID' if po_status == 'PAID' else 'PENDING'))

            if po_status == 'PAID':
                cursor.execute("UPDATE Departments SET budget_used = budget_used + ? WHERE dept_id = 1", (price * qty,))

    conn.commit()
    conn.close()
    print("Dummy data inserted.")

if __name__ == '__main__':
    insert_dummy()
