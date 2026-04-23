from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def add_background_image(slide, img_path):
    slide.shapes.add_picture(img_path, 0, 0, width=Inches(10), height=Inches(7.5))
    
def add_overlay(slide, alpha=128):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(10), Inches(7.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(15, 20, 25)
    shape.width = Inches(5.5)
    shape.line.fill.background()

def create_title(slide, text, top_inch=1.0):
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(top_inch), Inches(4.5), Inches(1))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = 'Arial'

def create_body(slide, lines, top_inch=2.5):
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(top_inch), Inches(4.8), Inches(4.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for line in lines:
        p = tf.add_paragraph()
        p.text = line
        if line.startswith("•") or line.startswith("-") or line[0].isdigit():
            p.font.size = Pt(16)
        else:
            p.font.size = Pt(20)
            p.font.bold = True
        p.font.color.rgb = RGBColor(230, 230, 230)
        p.font.name = 'Arial'
        p.space_after = Pt(10)

def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    img_title = r"C:\Users\nisar\.gemini\antigravity\brain\1e99230e-fdf4-4e98-8f13-ca0289cfda97\ppt_bg_title_1776952410414.png"
    img_data = r"C:\Users\nisar\.gemini\antigravity\brain\1e99230e-fdf4-4e98-8f13-ca0289cfda97\ppt_bg_data_1776952425197.png"
    img_dash = r"C:\Users\nisar\.gemini\antigravity\brain\1e99230e-fdf4-4e98-8f13-ca0289cfda97\ppt_bg_dashboard_1776952443147.png"

    blank_layout = prs.slide_layouts[6] 

    # --- Slide 1 ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_title)
    add_overlay(slide)
    create_title(slide, "Multi-Vendor Procurement &\nPurchase Order System", top_inch=2.0)
    create_body(slide, [
        "Database Management Tools",
        "Final Project",
        " ",
        "Team 3",
        "Members: Nisarg Shah, [Add Member 2], [Add Member 3]"
    ], top_inch=4.0)

    # --- Slide 2 ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_dash)
    add_overlay(slide)
    create_title(slide, "Project Overview\n& Objectives")
    create_body(slide, [
        "The Project:",
        "• A role-based enterprise procurement platform identifying B2B workflows.",
        "The Problem:",
        "• Organizations struggle with fragmented pipelines, missing audit trails, and opaque budgets.",
        "The Goal:",
        "• Centralize the workflow from request to payout.",
        "• Provide real-time budget tracking and role-based access securely."
    ])

    # --- Slide 3 ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_data)
    add_overlay(slide)
    create_title(slide, "Core System\nWorkflow")
    create_body(slide, [
        "1. Employee Request (Status: PENDING)",
        "2. Manager Review (Status: APPROVED / REJECTED)",
        "3. Procurement Cut PO (Status: PO_ISSUED)",
        "4. Vendor Fulfillment (Status: SHIPPED)",
        "5. Finance Payout (Status: INVOICED ➔ PAID)"
    ])

    # ================= WALKTHROUGH SECTION =================
    
    # --- Walkthrough Slide 1: Employee ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_data)
    add_overlay(slide)
    create_title(slide, "Live Demo Phase 1:\nThe Request")
    create_body(slide, [
        "Persona: Alice (IT Employee)",
        " ",
        "Logical Data Input:",
        "• Item: Dell XPS 15 Laptops",
        "• Quantity: 5",
        "• Estimated Cost: $2,000 each",
        "• Total Value: $10,000",
        " ",
        "System Action:",
        "Alice submits the PR. A new record is inserted into Purchase_Requests. Status is clamped to 'PENDING'."
    ], top_inch=1.4)

    # --- Walkthrough Slide 2: Manager ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_title)
    add_overlay(slide)
    create_title(slide, "Live Demo Phase 2:\nThe Approval")
    create_body(slide, [
        "Persona: Bob (IT Manager)",
        " ",
        "Logical Data Input:",
        "• Budget Context: Bob has $100k allocated.",
        "• Action: Bob reviews the $10,000 request and clicks 'Approve'.",
        "• Comment: 'Approved for Q3 Expansion.'",
        " ",
        "System Action:",
        "Status changes to 'APPROVED'. PR_Approvals logs Bob's decision. PR_Status_History locks the timestamp."
    ], top_inch=1.4)

    # --- Walkthrough Slide 3: Procurement ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_dash)
    add_overlay(slide)
    create_title(slide, "Live Demo Phase 3:\nGenerating the PO")
    create_body(slide, [
        "Persona: Charlie (Procurement Officer)",
        " ",
        "Logical Data Input:",
        "• Action: Converts the Approved PR.",
        "• Selected Vendor: 'Tech Supplies Inc.'",
        "• Delivery Date: Nullified for 7 days from today.",
        " ",
        "System Action:",
        "A formal Purchase_Order is generated linking Alice's PR to Vendor #4. Status updates to 'PO_ISSUED'."
    ], top_inch=1.4)

    # --- Walkthrough Slide 4: Vendor ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_data)
    add_overlay(slide)
    create_title(slide, "Live Demo Phase 4:\nVendor Fulfillment")
    create_body(slide, [
        "Persona: Tech Supplies Inc (External Vendor)",
        " ",
        "Logical Data Input:",
        "• The vendor logs in (External RBAC limits sight to only their POs).",
        "• Action: Vendor ships the 5 Laptops and clicks 'Mark as Shipped'.",
        " ",
        "System Action:",
        "Status jumps to 'SHIPPED'. A 'Goods_Receipt' record is auto-generated anticipating physical delivery."
    ], top_inch=1.4)

    # --- Walkthrough Slide 5: Finance ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_title)
    add_overlay(slide)
    create_title(slide, "Live Demo Phase 5:\nPayment & Audit")
    create_body(slide, [
        "Persona: Diana (Finance Team)",
        " ",
        "Logical Data Input:",
        "• Action: Diana verifies the 5 laptops arrived and finalizes payment for the $10,000 invoice.",
        " ",
        "System Action:",
        "1. Invoices table logs a $10,000 transaction 'PAID'.",
        "2. The IT Department budget_used rigidly increments by $10,000.",
        "3. Audit_Log seals the transaction via Trigger."
    ], top_inch=1.2)
    
    # ================= END WALKTHROUGH SECTION =================

    # --- Slide 4 (now 9) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_data)
    add_overlay(slide)
    create_title(slide, "Database Design\n& ERD")
    create_body(slide, [
        "Architecture Insights:",
        "• Highly Normalized (3NF)",
        "• 16 Interconnected Tables",
        "• 6 Isolated Modules",
        "• Total Referential Integrity (Foreign Keys)",
        " ",
        "➔ Note: Paste ERD Image on the right side!"
    ])

    # --- Slide 5 (now 10) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_title)
    add_overlay(slide)
    create_title(slide, "Key Business\nRules")
    create_body(slide, [
        "Role Constraints:",
        "• Vendors view only assigned POs. Managers approve only local department requests.",
        "Budgeting Logic:",
        "• Payments auto-update the budget_used field.",
        "Strict Audit Trail:",
        "• All state changes write to the IP-aware Audit_Log.",
        "Status Progression:",
        "• Rigid state machine prevents skipping process steps."
    ], top_inch=2.2)

    # --- Slide 6 (now 11) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_data)
    add_overlay(slide)
    create_title(slide, "Data Dictionary\nOverview")
    create_body(slide, [
        "1. Identity:",
        "• Users, Roles, Departments",
        "2. Workflow:",
        "• Purchase_Requests, PR_Approvals, PR_Status_History",
        "3. Vendors:",
        "• Vendors, Vendor_Categories, Contracts",
        "4. Orders:",
        "• Purchase_Orders, Goods_Receipt, PO_Line_Items",
        "5. Finance & System:",
        "• Invoices, Payments, Budget_Transactions, Audit_Log"
    ], top_inch=2.0)

    # --- Slide 7 (now 12) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_data)
    add_overlay(slide)
    create_title(slide, "SQL Scripting\n& Queries")
    create_body(slide, [
        "Initialization Matrix (setup_db.py):",
        "• Dynamic DDL table creation with strong constraints.",
        "Mock Data Generator:",
        "• Algorithmic DML creating 30 days of simulated history.",
        "Analytic Queries:",
        "• Basic: Budget aggregations.",
        "• Advanced: Multi-table JOINs across the entire user-to-payout pipeline.",
        " ",
        "➔ Note: Paste Code Snippet on the right side!"
    ])

    # --- Slide 8 (now 13) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_dash)
    add_overlay(slide)
    create_title(slide, "Frontend\nIntegration (Extra)")
    create_body(slide, [
        "Tech Stack:",
        "• Framework: Python Flask & Jinja2 Templates.",
        "• Interface: Bootstrap 5, Glassmorphism UI.",
        "• Visualizations: Interactive Chart.js pipeline metrics.",
        "• Deployment: Live Serverless App on Vercel.",
        " ",
        "➔ Note: Paste Dashboard Screenshot on the right side!"
    ], top_inch=2.2)

    # --- Slide 9 (now 14) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_title)
    add_overlay(slide)
    create_title(slide, "Challenges &\nSolutions")
    create_body(slide, [
        "Challenges ⚠️:",
        "• Cloud Serverless DB Limitations (Read-only OS).",
        "• Auditing securely without duplicating logs.",
        " ",
        "Solutions ✅:",
        "• Custom DBWrapper overriding SQLite in favor of Postgres on cloud, with /tmp fallback.",
        "• Centralized PR_Status_History for absolute state-tracking compliance."
    ])

    # --- Slide 10 (now 15) ---
    slide = prs.slides.add_slide(blank_layout)
    add_background_image(slide, img_title)
    add_overlay(slide)
    create_title(slide, "Conclusion &\nFuture Scope")
    create_body(slide, [
        "Summary:",
        "• Built a robust, normalized database mirroring real B2B logic.",
        "Key Learnings:",
        "• Translating rigid business state machines into 3NF relational schemas while defending data integrity.",
        "Future Scope:",
        "• Migrating entirely to cloud-native PostgreSQL.",
        "• Automated PDF invoice generation."
    ])

    prs.save("Team3_Premium_Walkthrough_Presentation.pptx")
    print("Premium Presentation with Walkthrough generated successfully!")

if __name__ == "__main__":
    main()
