import sqlite3
import psycopg2
import psycopg2.extras
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_dbmt_project'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'procurement.db')
TMP_DB_PATH = '/tmp/procurement.db'

class DBWrapper:
    def __init__(self, connection, is_postgres=False):
        self.conn = connection
        self.is_postgres = is_postgres
        
    def execute(self, query, params=None):
        if self.is_postgres:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            # Translate SQLite syntax to PostgreSQL syntax
            if '?' in query:
                query = query.replace('?', '%s')
                
            if 'last_insert_rowid()' in query.lower():
                query = "SELECT lastval()"
                
            query = query.replace('"PENDING"', "'PENDING'")
            query = query.replace('"APPROVED"', "'APPROVED'")
            query = query.replace('"PO_ISSUED"', "'PO_ISSUED'")
            query = query.replace('"SHIPPED"', "'SHIPPED'")
            query = query.replace('"Shipped by Vendor"', "'Shipped by Vendor'")
            query = query.replace('"INVOICED"', "'INVOICED'")
            query = query.replace('"PAID"', "'PAID'")
            
            if params is not None:
                cur.execute(query, params)
            else:
                cur.execute(query)
            return cur
        else:
            if params is not None:
                return self.conn.execute(query, params)
            return self.conn.execute(query)
            
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        conn = psycopg2.connect(db_url)
        return DBWrapper(conn, is_postgres=True)

    import shutil
    # Vercel serverless environment restricts file writes to /tmp/
    if os.environ.get('VERCEL') == '1':
        if not os.path.exists(TMP_DB_PATH):
            if os.path.exists(DB_PATH):
                shutil.copy2(DB_PATH, TMP_DB_PATH)
            else:
                # Fallback if somehow using wrong path
                alt_path = os.path.join(os.getcwd(), 'procurement.db')
                if os.path.exists(alt_path):
                    shutil.copy2(alt_path, TMP_DB_PATH)
        try:
            conn = sqlite3.connect(TMP_DB_PATH)
            # test if tables exist
            conn.execute("SELECT count(*) FROM Users")
        except:
            conn = sqlite3.connect(DB_PATH) # fallback
    else:
        conn = sqlite3.connect(DB_PATH)
        
    conn.row_factory = sqlite3.Row
    return DBWrapper(conn, is_postgres=False)

class User(UserMixin):
    def __init__(self, id, name, email, role_id, role_name, department_id):
        self.id = id
        self.name = name
        self.email = email
        self.role_id = role_id
        self.role_name = role_name
        self.department_id = department_id

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('''
        SELECT u.*, r.role_name 
        FROM Users u 
        JOIN Roles r ON u.role = r.role_id 
        WHERE u.user_id = ?
    ''', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(id=user['user_id'], name=user['name'], email=user['email'], 
                    role_id=user['role'], role_name=user['role_name'], department_id=user['department_id'])
    return None

from datetime import datetime
import pytz

# ... existing code ...

def log_audit(user_id, action, table_affected):
    conn = get_db_connection()
    central = pytz.timezone('US/Central')
    # Get current time in CT, formatted same way SQLite does CURRENT_TIMESTAMP (YYYY-MM-DD HH:MM:SS)
    ct_time = datetime.now(central).strftime('%Y-%m-%d %H:%M:%S')
    
    conn.execute('INSERT INTO Audit_Log (user_id, action, table_affected, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
                 (user_id, action, table_affected, request.remote_addr, ct_time))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/api/auth', methods=['POST'])
def api_auth():
    try:
        data = request.json
        email = data.get('email')
        
        conn = get_db_connection()
        user = conn.execute('''
            SELECT u.*, r.role_name 
            FROM Users u 
            JOIN Roles r ON u.role = r.role_id 
            WHERE u.email = ?
        ''', (email,)).fetchone()
        
        if user:
            user_obj = User(id=user['user_id'], name=user['name'], email=user['email'], 
                            role_id=user['role'], role_name=user['role_name'], department_id=user['department_id'])
            login_user(user_obj)
            log_audit(user['user_id'], 'LOGIN', 'Users')
            conn.close()
            return jsonify({"success": True, "redirect": url_for('dashboard')})
        else:
            conn.close()
            return jsonify({"success": False, "error": "User email not registered in system."})
    except Exception as e:
        import traceback
        return jsonify({"success": False, "error": f"Backend Error: {str(e)}", "trace": traceback.format_exc()})

@app.route('/logout')
@login_required
def logout():
    log_audit(current_user.id, 'LOGOUT', 'Users')
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    data = {}
    
    if current_user.role_name == 'Employee':
        data['requests'] = conn.execute('SELECT * FROM Purchase_Requests WHERE employee_id = ? ORDER BY created_at DESC', (current_user.id,)).fetchall()
        data['kpi_total'] = len(data['requests'])
        data['kpi_approved'] = sum(1 for r in data['requests'] if r['status'] in ('APPROVED', 'PO_ISSUED', 'SHIPPED', 'INVOICED', 'PAID'))
        data['kpi_pending'] = sum(1 for r in data['requests'] if r['status'] == 'PENDING')
        data['kpi_rejected'] = sum(1 for r in data['requests'] if r['status'] == 'REJECTED')
    
    elif current_user.role_name == 'Manager':
        data['pending_requests'] = conn.execute('''
            SELECT * FROM Purchase_Requests 
            WHERE dept_id = ? AND status = "PENDING"
        ''', (current_user.department_id,)).fetchall()
        data['dept'] = conn.execute('SELECT * FROM Departments WHERE dept_id = ?', (current_user.department_id,)).fetchone()
        data['kpi_pending'] = len(data['pending_requests'])
        data['kpi_budget_total'] = data['dept']['budget_allocated']
        data['kpi_budget_used'] = data['dept']['budget_used']

    elif current_user.role_name == 'Procurement':
        data['approved_requests'] = conn.execute('SELECT * FROM Purchase_Requests WHERE status = "APPROVED"').fetchall()
        data['vendors'] = conn.execute("SELECT * FROM Vendors WHERE is_active = TRUE").fetchall()
        data['pos'] = conn.execute('SELECT po.*, v.company_name FROM Purchase_Orders po JOIN Vendors v ON po.vendor_id = v.vendor_id').fetchall()
        data['kpi_to_issue'] = len(data['approved_requests'])
        data['kpi_active'] = len(data['pos'])
        data['kpi_value'] = sum(p['total_amount'] for p in data['pos'])
        
    elif current_user.role_name == 'Vendor':
        vendor_info = conn.execute('SELECT vendor_id FROM Vendors WHERE email = ?', (current_user.email,)).fetchone()
        data['pos'] = []
        if vendor_info:
            data['pos'] = conn.execute('SELECT * FROM Purchase_Orders WHERE vendor_id = ?', (vendor_info['vendor_id'],)).fetchall()
        data['kpi_open'] = len(data['pos'])
        # VENDOR FIX: Status is 'ISSUED' in the Purchase_Orders table
        data['kpi_to_ship'] = sum(1 for p in data['pos'] if p['status'] == 'ISSUED')
        data['kpi_value'] = sum(p['total_amount'] for p in data['pos'])

    elif current_user.role_name == 'Finance':
        data['deliveries'] = conn.execute('SELECT gr.*, po.vendor_id FROM Goods_Receipt gr JOIN Purchase_Orders po ON gr.po_id = po.po_id WHERE po.status = "SHIPPED"').fetchall()
        data['invoices'] = conn.execute('SELECT * FROM Invoices ORDER BY invoice_id DESC').fetchall()
        data['kpi_ready'] = len(data['deliveries'])
        data['kpi_unpaid'] = sum(1 for i in data['invoices'] if i['status'] == 'PENDING')
        data['kpi_paid_amt'] = sum(i['amount'] for i in data['invoices'] if i['status'] == 'PAID')
        data['kpi_total_invoiced'] = sum(i['amount'] for i in data['invoices'])

    elif current_user.role_name == 'SuperAdmin':
        data['departments'] = conn.execute('SELECT * FROM Departments').fetchall()
        data['audit'] = conn.execute('SELECT a.*, u.email FROM Audit_Log a JOIN Users u ON a.user_id = u.user_id ORDER BY timestamp DESC LIMIT 100').fetchall()
        data['all_pos'] = conn.execute('SELECT status, COUNT(*) as count FROM Purchase_Orders GROUP BY status').fetchall()
        data['kpi_depts'] = len(data['departments'])
        data['kpi_logs'] = conn.execute('SELECT COUNT(*) FROM Audit_Log').fetchone()[0]
        data['kpi_pos'] = sum(p['count'] for p in data['all_pos'])
        data['kpi_pipeline_value'] = conn.execute("SELECT COALESCE(SUM(total_amount), 0) FROM Purchase_Orders WHERE status != 'PAID'").fetchone()[0] or 0
        data['kpi_total_spent'] = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM Invoices WHERE status = 'PAID'").fetchone()[0] or 0

    conn.close()
    return render_template('dashboard.html', data=data)

# Actions
@app.route('/submit_pr', methods=['POST'])
@login_required
def submit_pr():
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    cost = float(request.form['cost'])
    desc = request.form['description']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Purchase_Requests (employee_id, dept_id, item_name, description, quantity, estimated_cost)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_user.id, current_user.department_id, item_name, desc, quantity, cost))
    conn.commit()
    pr_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.execute('INSERT INTO PR_Status_History (pr_id, old_status, new_status, changed_by) VALUES (?, ?, ?, ?)',
                 (pr_id, 'NONE', 'PENDING', current_user.id))
    conn.commit()
    conn.close()
    
    log_audit(current_user.id, 'SUBMIT_PR', 'Purchase_Requests')
    flash('Purchase Request Submitted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/approve_pr/<int:pr_id>', methods=['POST'])
@login_required
def approve_pr(pr_id):
    decision = request.form['decision']  # 'APPROVED' or 'REJECTED'
    comments = request.form['comments']

    conn = get_db_connection()
    pr = conn.execute('SELECT * FROM Purchase_Requests WHERE pr_id = ?', (pr_id,)).fetchone()

    # FIX REC 1: Budget validation before approving
    if decision == 'APPROVED' and pr:
        dept = conn.execute('SELECT * FROM Departments WHERE dept_id = ?', (pr['dept_id'],)).fetchone()
        request_total = pr['quantity'] * pr['estimated_cost']
        remaining = dept['budget_allocated'] - dept['budget_used']
        if request_total > remaining:
            conn.close()
            flash('Cannot approve: ${:,.0f} requested exceeds remaining budget of ${:,.0f}'.format(request_total, remaining), 'danger')
            return redirect(url_for('dashboard'))
            
        # BUG FIX: Budget should be encumbered immediately upon Manager approval, not at invoice time
        conn.execute('UPDATE Departments SET budget_used = budget_used + ? WHERE dept_id = ?', (request_total, pr['dept_id']))
        conn.execute('INSERT INTO Budget_Transactions (dept_id, po_id, amount, transaction_type) VALUES (?, NULL, ?, ?)',
                     (pr['dept_id'], request_total, 'ENCUMBRANCE'))

    conn.execute('UPDATE Purchase_Requests SET status = ? WHERE pr_id = ?', (decision, pr_id))
    conn.execute('INSERT INTO PR_Approvals (pr_id, manager_id, decision, comments) VALUES (?, ?, ?, ?)',
                 (pr_id, current_user.id, decision, comments))
    # FIX REC 6: Track the PENDING → APPROVED/REJECTED transition
    conn.execute('INSERT INTO PR_Status_History (pr_id, old_status, new_status, changed_by) VALUES (?, ?, ?, ?)',
                 (pr_id, 'PENDING', decision, current_user.id))
    conn.commit()
    conn.close()
    log_audit(current_user.id, decision + '_PR', 'Purchase_Requests')
    flash('Request ' + decision + ' successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/generate_po', methods=['POST'])
@login_required
def generate_po():
    pr_id = request.form['pr_id']
    vendor_id = request.form['vendor_id']
    delivery_date = request.form['delivery_date']

    conn = get_db_connection()
    pr = conn.execute('SELECT * FROM Purchase_Requests WHERE pr_id = ?', (pr_id,)).fetchone()
    total_amt = pr['quantity'] * pr['estimated_cost']

    conn.execute('''
        INSERT INTO Purchase_Orders (pr_id, vendor_id, procurement_officer_id, delivery_due_date, total_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (pr_id, vendor_id, current_user.id, delivery_date, total_amt))
    conn.commit()
    po_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

    # FIX REC 4: Populate PO_Line_Items — was always empty before
    conn.execute('''
        INSERT INTO PO_Line_Items (po_id, item_description, quantity, unit_price, total_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (po_id, pr['item_name'], pr['quantity'], pr['estimated_cost'], total_amt))

    conn.execute('UPDATE Purchase_Requests SET status = "PO_ISSUED" WHERE pr_id = ?', (pr_id,))
    # FIX REC 6: Track APPROVED → PO_ISSUED transition
    conn.execute('INSERT INTO PR_Status_History (pr_id, old_status, new_status, changed_by) VALUES (?, ?, ?, ?)',
                 (pr_id, 'APPROVED', 'PO_ISSUED', current_user.id))
    conn.commit()
    conn.close()

    log_audit(current_user.id, 'GENERATE_PO', 'Purchase_Orders')
    flash('Purchase Order Generated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/vendor_ship/<int:po_id>', methods=['POST'])
@login_required
def vendor_ship(po_id):
    conn = get_db_connection()
    po = conn.execute('''
        SELECT po.*, pr.quantity, pr.pr_id as linked_pr_id FROM Purchase_Orders po
        JOIN Purchase_Requests pr ON po.pr_id = pr.pr_id
        WHERE po.po_id = ?
    ''', (po_id,)).fetchone()
    quantity = po['quantity'] if po else 0
    conn.execute('UPDATE Purchase_Orders SET status = "SHIPPED" WHERE po_id = ?', (po_id,))
    conn.execute(
        'INSERT INTO Goods_Receipt (po_id, received_by, quantity_received, condition_notes) VALUES (?, ?, ?, ?)',
        (po_id, current_user.id, quantity, 'Goods received in good condition')
    )
    # FIX REC 6: Track PO_ISSUED → SHIPPED transition
    if po:
        conn.execute('INSERT INTO PR_Status_History (pr_id, old_status, new_status, changed_by) VALUES (?, ?, ?, ?)',
                     (po['linked_pr_id'], 'PO_ISSUED', 'SHIPPED', current_user.id))
    conn.commit()
    conn.close()
    log_audit(current_user.id, 'MARK_SHIPPED', 'Purchase_Orders')
    flash('Order marked as Shipped!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/finance_invoice', methods=['POST'])
@login_required
def finance_invoice():
    po_id = request.form['po_id']
    conn = get_db_connection()
    # FIX BUG 1: JOIN to get dept_id so we can update the department budget
    po = conn.execute('''
        SELECT po.*, pr.dept_id FROM Purchase_Orders po
        JOIN Purchase_Requests pr ON po.pr_id = pr.pr_id
        WHERE po.po_id = ?
    ''', (po_id,)).fetchone()
    total_amount = po['total_amount']
    dept_id = po['dept_id']

    conn.execute('INSERT INTO Invoices (po_id, vendor_id, due_date, amount) VALUES (?, ?, ?, ?)',
                 (po_id, po['vendor_id'], po['delivery_due_date'], total_amount))
    conn.commit()
    conn.execute('UPDATE Purchase_Orders SET status = "INVOICED" WHERE po_id = ?', (po_id,))
    # Record that the invoice was generated, but budget was already deducted during manager approval
    conn.execute('INSERT INTO Budget_Transactions (dept_id, po_id, amount, transaction_type) VALUES (?, ?, ?, ?)',
                 (dept_id, po_id, total_amount, 'INVOICE_PROCESSED'))
    conn.commit()
    conn.close()
    log_audit(current_user.id, 'CREATE_INVOICE', 'Invoices')
    flash('Invoice processed and department budget updated!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/mark_paid/<int:invoice_id>', methods=['POST'])
@login_required
def mark_paid(invoice_id):
    # FIX BUG 2: The missing PAID route — complete the payment lifecycle
    if current_user.role_name != 'Finance':
        return redirect(url_for('dashboard'))
    import uuid
    payment_method = request.form.get('payment_method', 'Bank Transfer')
    reference = 'PAY-' + str(uuid.uuid4())[:8].upper()
    conn = get_db_connection()
    inv = conn.execute('SELECT * FROM Invoices WHERE invoice_id = ?', (invoice_id,)).fetchone()
    if inv and inv['status'] == 'PENDING':
        conn.execute('UPDATE Invoices SET status = "PAID" WHERE invoice_id = ?', (invoice_id,))
        conn.execute('''
            INSERT INTO Payments (invoice_id, paid_by, amount_paid, payment_method, reference_no)
            VALUES (?, ?, ?, ?, ?)
        ''', (invoice_id, current_user.id, inv['amount'], payment_method, reference))
        conn.commit()
        log_audit(current_user.id, 'MARK_PAID', 'Payments')
        paid_amt = inv['amount']
        flash('Payment of $' + '{:,.2f}'.format(paid_amt) + ' processed! Ref: ' + reference, 'success')
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/clear_log/<int:log_id>', methods=['POST'])
@login_required
def clear_log(log_id):
    if current_user.role_name != 'SuperAdmin':
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    conn.execute('DELETE FROM Audit_Log WHERE log_id = ?', (log_id,))
    conn.commit()
    conn.close()
    flash('Audit log entry removed.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/clear_all_logs', methods=['POST'])
@login_required
def clear_all_logs():
    if current_user.role_name != 'SuperAdmin':
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    conn.execute('DELETE FROM Audit_Log')
    conn.commit()
    conn.close()
    flash('All audit logs cleared!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    from setup_db import create_database
    if not os.path.exists(DB_PATH):
        create_database()
    app.run(debug=True, port=5000)
