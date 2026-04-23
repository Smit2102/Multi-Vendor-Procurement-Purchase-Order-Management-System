from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

prs = Presentation()

# Slide 1: Welcome & Title
slide_layout = prs.slide_layouts[0] # Title slide
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Multi-Vendor Procurement & Purchase Order Management System"
subtitle.text = "Database Management Tools - Final Project\n\nTeam 3\nTeam Members: Nisarg Shah, [Add Member 2], [Add Member 3], [Add Member 4]"

# Slide 2: Project Overview & Objective
slide_layout = prs.slide_layouts[1] # Title and Content
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
title.text = "Project Overview & Objectives"
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "The Project: A role-based enterprise procurement platform that digitized the end-to-end B2B purchasing lifecycle."
p = tf.add_paragraph()
p.text = "The Problem: Large organizations struggle with fragmented procurement pipelines, missing audit trails, and opaque budgets."
p = tf.add_paragraph()
p.text = "The Goal: Centralize the workflow from request to payout. Provide real-time budget tracking, robust role-based access control, and a fully normalized relational database backbone to ensure data integrity and track every transaction."

# Slide 3: The Procurement Lifecycle
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Core System Workflow (The Procurement Lifecycle)"
tf = slide.placeholders[1].text_frame
tf.text = "1. Employee Request (Status: PENDING)"
tf.add_paragraph().text = "2. Manager Review (Status: APPROVED / REJECTED)"
tf.add_paragraph().text = "3. Procurement Cut PO (Status: PO_ISSUED)"
tf.add_paragraph().text = "4. Vendor Fulfillment (Status: SHIPPED)"
tf.add_paragraph().text = "5. Finance Payout (Status: INVOICED -> PAID)"

# Slide 4: Database Design & ERD
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Database Design & Architecture"
tf = slide.placeholders[1].text_frame
tf.text = "• Highly Normalized (3NF)"
tf.add_paragraph().text = "• 16 Interconnected Tables"
tf.add_paragraph().text = "• 6 Isolated Modules"
tf.add_paragraph().text = "• Total Referential Integrity (Foreign Keys)"
tf.add_paragraph().text = "\n[Insert Screenshot of your ERD Here]"

# Slide 5: Business Rules & Constraints
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Key Business Rules"
tf = slide.placeholders[1].text_frame
tf.text = "Role Constraints: Vendors can only view their own assigned Purchase Orders. Managers can only approve requests from their own departments."
tf.add_paragraph().text = "Budgeting Logic: Payments made automatically update the budget_used field for the associated department."
tf.add_paragraph().text = "Strict Audit Trail: Every state change requires an automated trigger into the IP-aware Audit_Log tracking the exact user and timestamp."
tf.add_paragraph().text = "Status Progression: A Purchase Request cannot jump straight to an invoice; it logically flows through the enforced state machine."

# Slide 6: Data Dictionary Overview
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Data Dictionary Overview"
tf = slide.placeholders[1].text_frame
tf.text = "1. Identity: Users, Roles, Departments - Manages RBAC and departmental budgets."
tf.add_paragraph().text = "2. Workflow: Purchase_Requests, PR_Approvals, PR_Status_History - Tracks the lifecycle of employee needs."
tf.add_paragraph().text = "3. Vendors: Vendors, Vendor_Categories, Contracts - Stores external supplier details."
tf.add_paragraph().text = "4. Orders: Purchase_Orders, Goods_Receipt, PO_Line_Items - Bound to vendors and requests."
tf.add_paragraph().text = "5. Finance: Invoices, Payments, Budget_Transactions - Tracks corporate capital outflow."
tf.add_paragraph().text = "6. System: Audit_Log, Notifications - Enforces compliance."

# Slide 7: SQL Implementation
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "SQL Scripting & Queries"
tf = slide.placeholders[1].text_frame
tf.text = "Initialization Matrix (setup_db.py): DDL scripts dynamically creating tables and enforcing NOT NULL, UNIQUE, and FOREIGN KEY constraints."
tf.add_paragraph().text = "Mock Data Generation (populate_db.py): Algorithmic DML scripts simulating 30 days of prior transactions."
tf.add_paragraph().text = "Analytic Queries:"
tf.add_paragraph().text = "  - Basic: Finding total spent budgets via aggregations."
tf.add_paragraph().text = "  - Advanced: Deep multi-table JOINs compiling the pipeline from Users -> Requests -> Orders -> Invoices."
tf.add_paragraph().text = "\n[Paste a visually appealing code block snippet of your longest JOIN query here]"

# Slide 8: Frontend Integration
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Live Frontend Integration (Extra Credit)"
tf = slide.placeholders[1].text_frame
tf.text = "Framework: Python Flask & Jinja2 Templates"
tf.add_paragraph().text = "Interface: Bootstrap 5, Glassmorphism UI"
tf.add_paragraph().text = "Visualizations: Interactive Chart.js pipeline metrics"
tf.add_paragraph().text = "Deployment: Live Serverless App on Vercel"
tf.add_paragraph().text = "\n[Insert 2-3 screenshots of the actual app dashboard, especially the large KPI number cards and graphs]"

# Slide 9: Challenges & Solutions
# Let's use the layout format which has 2-content sections if available, list of layouts:
# 0: Title, 1: Title and Content, 2: Section Header, 3: Two Content, 4: Comparison
slide_layout = prs.slide_layouts[3]
slide = prs.slides.add_slide(slide_layout)
slide.shapes.title.text = "Challenges & Solutions"
tf_left = slide.placeholders[1].text_frame
tf_left.text = "CHALLENGES:"
tf_left.add_paragraph().text = "• Cloud Deployment DB Limitations: Serverless architectures have read-only file systems (SQLite limits)."
tf_left.add_paragraph().text = "• Schema Design: Preventing data duplication between roles and departments."
tf_left.add_paragraph().text = "• Audit Tracking: Safely recording state changes."

tf_right = slide.placeholders[2].text_frame
tf_right.text = "SOLUTIONS:"
tf_right.add_paragraph().text = "• Used a custom DBWrapper to seamlessly translate SQLite queries into PostgreSQL for cloud environments, with a /tmp/ fallback."
tf_right.add_paragraph().text = "• Extracted roles and budgets into standalone dimensional tables with Foreign Keys."
tf_right.add_paragraph().text = "• Implemented an isolated PR_Status_History table for full audit compliance."

# Slide 10: Conclusion
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Conclusion & Future Scope"
tf = slide.placeholders[1].text_frame
tf.text = "Summary: Built a robust, normalized database replicating real-world B2B logic, wrapped in an accessible frontend interface."
tf.add_paragraph().text = "Key Learnings: Deepened understanding of 3NF design, referential integrity limitations, and bridging backend databases with frontend frameworks securely."
tf.add_paragraph().text = "Future Improvements: Migrating entirely to cloud-native PostgreSQL, introducing Machine Learning algorithms for vendor selection rating, and generating automated PDF invoices."

prs.save("Team3_Final_Presentation.pptx")
print("Presentation generated successfully!")
