from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_IMG = r"C:\Users\nisar\.gemini\antigravity\brain\1e99230e-fdf4-4e98-8f13-ca0289cfda97"
import os
img_title    = os.path.join(BASE_IMG, "ppt_bg_title_1776952410414.png")
img_data     = os.path.join(BASE_IMG, "ppt_bg_data_1776952425197.png")
img_dash     = os.path.join(BASE_IMG, "ppt_bg_dashboard_1776952443147.png")
img_employee = os.path.join(BASE_IMG, "employee_dashboard_final_1776953947777.png")
img_manager  = os.path.join(BASE_IMG, "manager_dashboard_final_1776954034015.png")
img_admin    = os.path.join(BASE_IMG, "admin_dashboard_final_1776954182865.png")

W = Inches(10)
H = Inches(7.5)


# ── helpers ───────────────────────────────────────────────────────────────────

def bg(slide, img, panel_w=5.6):
    """Background image + left dark overlay panel."""
    slide.shapes.add_picture(img, 0, 0, width=W, height=H)
    p = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(panel_w), H)
    p.fill.solid()
    p.fill.fore_color.rgb = RGBColor(10, 14, 22)
    p.line.fill.background()

def bg_dark(slide, img):
    """Full-width dark overlay (for title slides)."""
    slide.shapes.add_picture(img, 0, 0, width=W, height=H)
    ov = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    ov.fill.solid()
    ov.fill.fore_color.rgb = RGBColor(10, 14, 22)
    ov.line.fill.background()
    # make overlay ~80% dark via adjusting RGB slightly lighter
    ov.fill.fore_color.rgb = RGBColor(8, 12, 20)


def full_screenshot_slide(slide, img_path, caption_title, caption_sub=""):
    """
    Entire slide = screenshot.
    A slim dark caption bar sits at the very bottom.
    """
    # Screenshot covers whole slide
    slide.shapes.add_picture(img_path, 0, 0, width=W, height=H)

    # Black caption bar at bottom
    bar_h = Inches(0.85)
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0, H - bar_h,
        W, bar_h
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(10, 14, 22)
    bar.line.fill.background()

    # Accent line above bar
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        0, H - bar_h,
        W, Inches(0.05)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(167, 97, 255)
    line.line.fill.background()

    # Title text in caption bar
    tb = slide.shapes.add_textbox(Inches(0.3), H - bar_h + Inches(0.1), Inches(8), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = caption_title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Calibri"

    if caption_sub:
        tb2 = slide.shapes.add_textbox(Inches(0.3), H - bar_h + Inches(0.46), Inches(8), Inches(0.3))
        p2 = tb2.text_frame.paragraphs[0]
        p2.text = caption_sub
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(167, 97, 255)
        p2.font.name = "Calibri"


def title_text(slide, headline, sub="", left=0.4, top=0.35):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(5.0), Inches(1.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = headline
    p.font.size = Pt(34)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Calibri"
    if sub:
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(167, 97, 255)
        p2.font.name = "Calibri"


def accent(slide, left=0.4, top=1.65, width=1.3):
    r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.06))
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor(167, 97, 255); r.line.fill.background()


def label(slide, txt, left=0.4, top=1.82, color=RGBColor(167, 97, 255)):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(5.0), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = txt.upper(); p.font.size = Pt(10); p.font.bold = True
    p.font.color.rgb = color; p.font.name = "Calibri"


def body(slide, lines, left=0.4, top=2.2, width=5.0):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.0))
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for line in lines:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
        p.text = line
        p.space_after = Pt(7)
        p.font.name = "Calibri"
        if line == "":
            p.font.size = Pt(5)
        elif line.startswith("•") or line.startswith("  →"):
            p.font.size = Pt(15)
            p.font.color.rgb = RGBColor(210, 215, 230)
        else:
            p.font.size = Pt(17)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)


def tag(slide, txt, left=0.4, top=6.85):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(5.0), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = txt; p.font.size = Pt(11); p.font.italic = True
    p.font.color.rgb = RGBColor(130, 140, 170); p.font.name = "Calibri"


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    blank = prs.slide_layouts[6]

    # ── 1. TITLE ──────────────────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg_dark(s, img_title)
    tb = s.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(2.2))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "Multi-Vendor Procurement"
    p.font.size = Pt(46); p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255); p.font.name = "Calibri"
    p2 = tf.add_paragraph()
    p2.text = "& Purchase Order Management System"
    p2.font.size = Pt(26); p2.font.color.rgb = RGBColor(167, 97, 255); p2.font.name = "Calibri"

    tb2 = s.shapes.add_textbox(Inches(1), Inches(4.5), Inches(8), Inches(1.5))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    for line in [
        "Database Management Tools  |  Final Project  |  Team 3",
        "Python Flask  ·  SQLite  ·  Firebase Auth  ·  Vercel",
        "procurement-system-peach.vercel.app"
    ]:
        p = tf2.add_paragraph() if tf2.paragraphs[0].text else tf2.paragraphs[0]
        p.text = line
        p.font.size = Pt(15 if "vercel.app" in line else 14)
        p.font.color.rgb = RGBColor(100, 200, 255) if "vercel.app" in line else RGBColor(180, 185, 200)
        p.font.name = "Calibri"; p.space_after = Pt(4)

    # ── 2. PROJECT OVERVIEW ───────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_dash)
    title_text(s, "Project Overview", "What we built & why")
    accent(s)
    label(s, "The Problem We Solved")
    body(s, [
        "The Problem:",
        "• Organizations lose visibility once a purchase request leaves an employee's desk.",
        "• No enforced budget tracking per department.",
        "• No reliable audit trail — who approved what, and when?",
        "",
        "Our Solution:",
        "• A 6-role enterprise procurement platform with full lifecycle tracking.",
        "• Rigid state-machine: requests cannot skip steps.",
        "• Every action logged with user, IP address, and timestamp."
    ])
    tag(s, "Live URL: procurement-system-peach.vercel.app")

    # ── 3. WORKFLOW OVERVIEW ──────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_data)
    title_text(s, "The Procurement\nState Machine", "5 phases · 16 tables · 6 roles")
    accent(s, top=1.8)
    body(s, [
        "Phase 1 — Employee:",
        "• Submits item request  →  Status: PENDING",
        "",
        "Phase 2 — Manager:",
        "• Approves or rejects  →  Status: APPROVED / REJECTED",
        "",
        "Phase 3 — Procurement:",
        "• Assigns vendor, issues PO  →  Status: PO_ISSUED",
        "",
        "Phase 4 — Vendor:",
        "• Ships goods, creates receipt  →  Status: SHIPPED",
        "",
        "Phase 5 — Finance:",
        "• Processes invoice & payment  →  Status: INVOICED → PAID",
    ], top=2.3)

    # ── 4. TEXT: LOGIN ────────────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_title)
    title_text(s, "System Entry:\nAuthentication")
    accent(s)
    label(s, "Firebase Auth + SQLite Role Lookup")
    body(s, [
        "How the Login Works:",
        "• Firebase Auth SDK verifies email/password client-side.",
        "• Flask backend queries: SELECT * FROM Users JOIN Roles WHERE email=?",
        "• On match → Flask-Login creates a secure session cookie.",
        "  → Audit_Log: INSERT (user_id, action='LOGIN', ip, timestamp)",
        "",
        "Test Credentials (password: 123456):",
        "• employee@test.com",
        "• manager@test.com  |  procurement@test.com",
        "• vendor@test.com  |  finance@test.com  |  admin@test.com"
    ])
    tag(s, "DB Tables: Users · Roles · Audit_Log")

    # ── 5. SCREENSHOT: EMPLOYEE ───────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    full_screenshot_slide(
        s, img_employee,
        "PHASE 1 — Employee Dashboard  |  employee@test.com",
        "Shows: New Request form · Request History (Dell XPS 15 — $10,000 — PO_ISSUED) · Analytics doughnut chart"
    )

    # ── 6. TEXT: EMPLOYEE PHASE ───────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_data)
    title_text(s, "Phase 1: Employee\nSubmits a Request")
    accent(s)
    label(s, "Logged in as: employee@test.com", color=RGBColor(100, 200, 255))
    body(s, [
        "Data Entered (Live Demo):",
        "• Item Name: Dell XPS 15 Laptop",
        "• Quantity: 5 units",
        "• Est. Cost per unit: $2,000.00",
        "• Total Estimated Value: $10,000",
        "• Justification: Required for new IT hires in Q3 expansion",
        "",
        "What Happened in the Database:",
        "• INSERT into Purchase_Requests (employee_id, dept_id, item_name, qty, cost)",
        "• status defaulted to 'PENDING'",
        "• INSERT into PR_Status_History: NONE → PENDING"
    ])
    tag(s, "DB Tables: Purchase_Requests · PR_Status_History")

    # ── 7. SCREENSHOT: MANAGER ────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    full_screenshot_slide(
        s, img_manager,
        "PHASE 2 — Manager Dashboard  |  manager@test.com",
        "Shows: Pending Approvals=0 · Total Budget=$100,000 · Budget Used=$0 · Remaining=$100,000.00"
    )

    # ── 8. TEXT: MANAGER PHASE ────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_title)
    title_text(s, "Phase 2: Manager\nReviews & Approves")
    accent(s)
    label(s, "Logged in as: manager@test.com", color=RGBColor(100, 200, 255))
    body(s, [
        "Manager Sees on Dashboard:",
        "• KPI: Total Budget = $100,000  (green)",
        "• KPI: Budget Used = $0  (safe — room to approve!)",
        "• Pending Team Approvals table listing employee requests",
        "",
        "Action Taken:",
        "• Identifies the Dell XPS 15 Laptop — $10,000 request",
        "• Adds comment: 'Approved for Q3 expansion — budget confirmed'",
        "• Clicks APPROVE",
        "",
        "Triggered SQL:",
        "• UPDATE Purchase_Requests SET status='APPROVED' WHERE pr_id=?",
        "• INSERT into PR_Approvals (pr_id, manager_id, decision, comments)",
        "• INSERT into PR_Status_History: PENDING → APPROVED"
    ])
    tag(s, "DB Tables: Purchase_Requests · PR_Approvals · PR_Status_History")

    # ── 9. TEXT: PROCUREMENT PHASE ────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_dash)
    title_text(s, "Phase 3: Procurement\nGenerates a PO")
    accent(s)
    label(s, "Logged in as: procurement@test.com", color=RGBColor(100, 200, 255))
    body(s, [
        "Dashboard Shows:",
        "• Approved Requests waiting for a Purchase Order",
        "• Active POs list with vendor names and total amounts",
        "• KPI: Total PO Value in the pipeline",
        "",
        "Action Taken:",
        "• Finds the approved Dell XPS 15 ($10,000)",
        "• Selects Vendor: Tech Supplies Inc",
        "• Sets Delivery Date and clicks Generate PO",
        "",
        "Triggered SQL:",
        "• INSERT into Purchase_Orders (pr_id, vendor_id, officer_id, delivery_date, total_amount)",
        "• UPDATE Purchase_Requests SET status='PO_ISSUED'"
    ])
    tag(s, "DB Tables: Purchase_Orders · Purchase_Requests · Vendors")

    # ── 10. TEXT: VENDOR PHASE ────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_data)
    title_text(s, "Phase 4: Vendor\nShips the Goods")
    accent(s)
    label(s, "Logged in as: vendor@test.com", color=RGBColor(100, 200, 255))
    body(s, [
        "Critical Role Restriction:",
        "• Vendor's dashboard query filters by their own vendor_id.",
        "• They CANNOT see other vendors' orders.",
        "",
        "Dashboard Shows:",
        "• KPI: Open Orders  |  Orders to Ship  |  Total Order Value",
        "• The Dell XPS 15 PO for $10,000 is listed as ISSUED",
        "",
        "Action Taken:",
        "• Vendor clicks 'Mark as Shipped'",
        "",
        "Triggered SQL:",
        "• UPDATE Purchase_Orders SET status='SHIPPED'",
        "• INSERT into Goods_Receipt (po_id, received_by, notes='Shipped by Vendor')"
    ])
    tag(s, "DB Tables: Purchase_Orders · Goods_Receipt")

    # ── 11. TEXT: FINANCE PHASE ───────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_title)
    title_text(s, "Phase 5: Finance\nProcesses Invoice")
    accent(s)
    label(s, "Logged in as: finance@test.com", color=RGBColor(100, 200, 255))
    body(s, [
        "Dashboard Shows:",
        "• Shipped Goods Receipts ready for invoicing",
        "• All Invoices with PENDING / PAID status",
        "• KPI: Total Accounts Payable",
        "",
        "Action Taken:",
        "• Finance sees the Dell XPS 15 goods receipt",
        "• Clicks 'Process Invoice'",
        "",
        "Triggered SQL:",
        "• INSERT into Invoices (po_id, vendor_id, amount=$10,000, status='PENDING')",
        "• UPDATE Purchase_Orders SET status='INVOICED'",
        "• department.budget_used += $10,000",
        "• Audit_Log: CREATE_INVOICE logged with IP + timestamp"
    ])
    tag(s, "DB Tables: Invoices · Payments · Budget_Transactions · Audit_Log")

    # ── 12. SCREENSHOT: ADMIN ─────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    full_screenshot_slide(
        s, img_admin,
        "SUPER ADMIN Dashboard  |  admin@test.com",
        "Shows: 1 Department · 4 Total POs · 27 Audit Events · Live System Audit Log · Budget Donut Chart"
    )

    # ── 13. TEXT: ADMIN ───────────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_dash)
    title_text(s, "Super Admin:\nGlobal Oversight")
    accent(s)
    label(s, "Logged in as: admin@test.com", color=RGBColor(100, 200, 255))
    body(s, [
        "Live KPIs Shown (Real Data):",
        "• Operating Departments: 1",
        "• Total Issued POs: 4",
        "• Recorded Audit Events: 27",
        "",
        "System Audit Log (real entries):",
        "• admin@test.com: LOGIN at 09:22:47",
        "• manager@test.com: LOGOUT at 09:20:45",
        "• employee@test.com: LOGIN at 09:18:59",
        "• finance@test.com: LOGOUT at 09:18:17",
        "",
        "Admin Powers:",
        "• Delete individual log entries",
        "• 'Clear All' wipes entire Audit_Log table"
    ])
    tag(s, "DB Tables: Audit_Log · Departments · Purchase_Orders")

    # ── 14. DATABASE DESIGN ───────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_data)
    title_text(s, "Database\nArchitecture", "16 Tables · 3NF · Full FK Integrity")
    accent(s, top=1.9)
    body(s, [
        "Identity Module:",
        "• Roles, Users, Departments",
        "",
        "Procurement Workflow:",
        "• Purchase_Requests, PR_Approvals, PR_Status_History",
        "",
        "Vendor Management:",
        "• Vendors, Vendor_Categories, Contracts",
        "",
        "Order Fulfillment:",
        "• Purchase_Orders, PO_Line_Items, Goods_Receipt",
        "",
        "Finance & Compliance:",
        "• Invoices, Payments, Budget_Transactions, Audit_Log"
    ], top=2.2)
    tag(s, "Paste ERD diagram screenshot on a dedicated slide after this")

    # ── 15. SQL ───────────────────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_title)
    title_text(s, "SQL Implementation\nHighlights")
    accent(s)
    label(s, "DDL · DML · Advanced JOIN Queries")
    body(s, [
        "Table Creation (setup_db.py):",
        "• 16 tables with NOT NULL, UNIQUE, FK constraints",
        "• Auto-translates SQLite → PostgreSQL for Vercel",
        "",
        "Data Population (populate_db.py):",
        "• DML INSERTs simulating 30 days of prior history",
        "• Covers all statuses from PENDING through PAID",
        "",
        "Example Advanced Query:",
        "• 4-table JOIN: Users → Purchase_Requests → Purchase_Orders → Invoices",
        "• Returns: name, item, amount, invoice status",
        "• Proves end-to-end traceability through SQL alone"
    ])
    tag(s, "Paste your SQL JOIN query screenshot after this slide")

    # ── 16. CHALLENGES ────────────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg(s, img_dash)
    title_text(s, "Challenges &\nSolutions")
    accent(s)
    body(s, [
        "Challenge 1 — Vercel Read-Only Filesystem:",
        "• SQLite cannot write to disk on serverless Vercel.",
        "• Fix: Custom DBWrapper routes all writes to /tmp/.",
        "  On DATABASE_URL env → auto-translates to PostgreSQL syntax.",
        "",
        "Challenge 2 — Enforcing the State Machine:",
        "• An invoice should never exist before an approval.",
        "• Fix: Role-based route guards — Finance only sees SHIPPED receipts.",
        "",
        "Challenge 3 — Audit Log Timestamps:",
        "• Default SQLite used UTC; business needed US/Central.",
        "• Fix: pytz forces all Audit_Log INSERTs to US/Central timezone."
    ])

    # ── 17. CONCLUSION ────────────────────────────────────────────────────────
    s = prs.slides.add_slide(blank)
    bg_dark(s, img_title)
    tb = s.shapes.add_textbox(Inches(1), Inches(1.0), Inches(8), Inches(1.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "Conclusion & Future Scope"
    p.font.size = Pt(42); p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255); p.font.name = "Calibri"

    acc = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(2.4), Inches(2.0), Inches(0.06))
    acc.fill.solid(); acc.fill.fore_color.rgb = RGBColor(167, 97, 255); acc.line.fill.background()

    tb2 = s.shapes.add_textbox(Inches(1), Inches(2.6), Inches(8), Inches(4.0))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    sections = [
        ("What We Built:", RGBColor(167,97,255), 17, True),
        ("A production-deployed, 6-role enterprise procurement system backed by a 16-table 3NF-normalized relational database — proving real-world business logic can be modeled precisely in SQL.", RGBColor(210,215,230), 14, False),
        ("", None, 6, False),
        ("Key Learnings:", RGBColor(167,97,255), 17, True),
        ("Translating complex state-machine rules into FK constraints. Bridging SQLite and PostgreSQL with a single abstraction layer. Deploying full-stack to production serverless infrastructure.", RGBColor(210,215,230), 14, False),
        ("", None, 6, False),
        ("Future Improvements:", RGBColor(167,97,255), 17, True),
        ("Full PostgreSQL migration. ML-based vendor rating. Auto-generate PDF invoices. Email notifications per role.", RGBColor(210,215,230), 14, False),
    ]
    first = True
    for txt, color, size, bold in sections:
        p = tf2.paragraphs[0] if first else tf2.add_paragraph()
        first = False
        p.text = txt; p.font.size = Pt(size); p.font.name = "Calibri"; p.font.bold = bold
        if color: p.font.color.rgb = color

    out = r"c:\Users\nisar\OneDrive\Documents\SEM 2\DBMT\project\procurement_system\Team3_FINAL_Presentation.pptx"
    prs.save(out)
    print("Saved: " + out)

if __name__ == "__main__":
    main()
