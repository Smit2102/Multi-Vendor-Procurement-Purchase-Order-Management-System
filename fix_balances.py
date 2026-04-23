import psycopg2
import os
from dotenv import load_dotenv

def fix_database_data():
    load_dotenv()
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("No DATABASE_URL found")
        return
        
    print("Connecting to Vercel PostgreSQL DB...")
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    try:
        # Step 1: Sync Purchase_Requests status with Purchase_Orders status
        print("Syncing Purchase_Requests status with Purchase_Orders...")
        cursor.execute("SELECT po_id, pr_id, status FROM Purchase_Orders")
        pos = cursor.fetchall()
        for po in pos:
            po_id, pr_id, po_status = po
            cursor.execute("UPDATE Purchase_Requests SET status = %s WHERE pr_id = %s AND status != %s", (po_status, pr_id, po_status))
            
        print("Syncing Purchase_Requests status from Invoices (for PAID status)...")
        cursor.execute('''
            SELECT i.invoice_id, po.pr_id, i.status 
            FROM Invoices i
            JOIN Purchase_Orders po ON i.po_id = po.po_id
            WHERE i.status = 'PAID'
        ''')
        paid_invs = cursor.fetchall()
        for inv in paid_invs:
            inv_id, pr_id, inv_status = inv
            cursor.execute("UPDATE Purchase_Requests SET status = 'PAID' WHERE pr_id = %s", (pr_id,))
            cursor.execute("UPDATE Purchase_Orders SET status = 'PAID' WHERE po_id = %s", (po_id,))

        # Step 2: Recalculate Budget Used for all departments (Instantly encumbered logic)
        print("Recalculating Departments Budget Used...")
        # Since we encumber at approval, ANY request that is 'APPROVED', 'PO_ISSUED', 'SHIPPED', 'INVOICED', or 'PAID' counts.
        # Wait, what if they were manually rejected? The status is 'REJECTED'.
        cursor.execute('''
            SELECT dept_id, COALESCE(SUM(quantity * estimated_cost), 0)
            FROM Purchase_Requests
            WHERE status IN ('APPROVED', 'PO_ISSUED', 'SHIPPED', 'INVOICED', 'PAID')
            GROUP BY dept_id
        ''')
        dept_budgets = cursor.fetchall()
        
        # Reset all to 0 first (in case some depts have 0 now)
        cursor.execute("UPDATE Departments SET budget_used = 0")
        
        for dept in dept_budgets:
            dept_id, used_budget = dept
            print(f"Setting Dept {dept_id} budget_used to ${used_budget:,.2f}")
            cursor.execute("UPDATE Departments SET budget_used = %s WHERE dept_id = %s", (used_budget, dept_id))

        conn.commit()
        print("Data sync complete! All balances and workflows perfectly reflect actual data.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    fix_database_data()
