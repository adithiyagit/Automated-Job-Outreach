"""
Generates a pixel-crisp, professional 1-page PDF resume for Adithiya B Vinu
matching the provided resume structure.
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas

def build_pdf(output_path: Path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()

    # Color definitions
    NAVY = colors.HexColor("#1A365D")
    GOLD = colors.HexColor("#B7791F")
    TEXT = colors.HexColor("#2D3748")
    LINE = colors.HexColor("#CBD5E0")

    # Typography styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY,
        alignment=1 # Center
    )

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=GOLD,
        alignment=1 # Center
    )

    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT,
        alignment=1 # Center
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=NAVY,
        spaceBefore=5,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=TEXT,
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10,
        textColor=TEXT,
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=2
    )

    role_title = ParagraphStyle(
        'RoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=TEXT
    )

    story = []

    # Header
    story.append(Paragraph("ADITHIYA B VINU", name_style))
    story.append(Paragraph("ERP Functional Consultant | Project Coordinator | QA & UAT — Odoo Implementation & Business Process Delivery", title_style))
    story.append(Paragraph("adithiyavinu.b@gmail.com | +91 96337 83038 | Kochi, Kerala, India | linkedin.com/in/adithiya-b-vinu | Open to Relocation", contact_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=LINE, spaceBefore=2, spaceAfter=4))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    story.append(Paragraph(
        "ERP professional with hands-on experience across the full implementation lifecycle — functional testing, UAT, BRD/FRD documentation, and change control — on a live, multi-module Odoo rollout. Skilled at analyzing business processes against system capabilities, identifying gaps, and translating requirements into validated configurations, while bridging business users, developers, and vendors. Seeking a structured ERP Functional Consultant, Business Analyst, or Project Coordinator role.",
        body_style
    ))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=2, spaceAfter=3))

    # Key Competencies
    story.append(Paragraph("KEY COMPETENCIES", section_heading))
    competencies = [
        "<b>Project Delivery & Change Control:</b> SDLC (Requirements -> Design -> Build -> Test -> Deploy), change request (CR) scoping & tracking, risk/issue logging, status reporting, Jira, Trello",
        "<b>Stakeholder & Vendor Coordination:</b> functional liaison between business users, developers, and third-party vendors; meeting facilitation; minutes & action tracking; SLA adherence",
        "<b>Business Analysis:</b> BRD & FRD authoring, requirement gathering, gap analysis, process mapping, workflow documentation",
        "<b>Quality & Functional Testing:</b> test case design & execution, UAT coordination & sign-off, defect logging & tracking, regression testing, gap analysis, hypercare support",
        "<b>Documentation & Training:</b> SOPs, process flowcharts, technical handovers, end-user training & enablement",
        "<b>Tools:</b> MS Excel, PowerPoint, Word; Jira, Trello; Odoo, ERPNext/Frappe"
    ]
    for c in competencies:
        story.append(Paragraph(f"• {c}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=2, spaceAfter=3))

    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
    
    # Job 1
    t1 = Table([[
        Paragraph("<b>Junior Project Manager cum Functional Consultant</b> — Empire AE IT Services, Kochi", role_title),
        Paragraph("<font size=8>Jan 2026 – Present</font>", ParagraphStyle('R', parent=role_title, alignment=2))
    ]], colWidths=[420, 120])
    t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
    story.append(t1)
    
    job1_bullets = [
        "Test and validate end-to-end Odoo workflows across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR modules, ensuring functional accuracy before deployment.",
        "Design and execute structured test cases; log defects and coordinate with developers for resolution and regression testing after updates, functioning as the coordination point between business stakeholders and technical team.",
        "Analyze client business processes against Odoo capabilities, identify gaps, and author BRD/FRD-aligned SOPs and approval-authority workflows across six business functions, converting requirements into validated system configurations.",
        "Lead UAT planning and execution, authoring test plans and defect reports and securing sign-off documentation to ensure on-time, on-spec deployment.",
        "Deliver end-user training across nine store locations using a rotational batch rollout plan, reducing post-go-live support load during hypercare."
    ]
    for b in job1_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    # Job 2
    t2 = Table([[
        Paragraph("<b>Python / ERPNext Developer — Intern</b> — Turqosoft Solutions, Kochi", role_title),
        Paragraph("<font size=8>Nov 2025 – Jan 2026</font>", ParagraphStyle('R2', parent=role_title, alignment=2))
    ]], colWidths=[420, 120])
    t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 3)]))
    story.append(t2)
    
    job2_bullets = [
        "Managed change requests end-to-end using Jira — scoping requirements, sprint planning, and delivering documented handovers to the SysAdmin team within agreed SLAs.",
        "Translated client requirements into ERPNext workflows following structured SDLC phases; authored SOPs and led knowledge-sharing sessions."
    ]
    for b in job2_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=2, spaceAfter=3))

    # Relevant Projects
    story.append(Paragraph("RELEVANT PROJECTS", section_heading))
    story.append(Paragraph("• <b>Jewellery Retail ERP Implementation — Odoo (2026):</b> Coordinated a live multi-module Odoo rollout across nine retail locations — requirements gathering, change control, BRD/FRD-aligned SOPs, UAT, and end-user training.", bullet_style))
    story.append(Paragraph("• <b>Fleet Management System — ERPNext (2025–2026):</b> Self-directed project covering vehicle tracking, maintenance scheduling, and fuel logging, built to practice requirements-to-deployment workflow end to end.", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=2, spaceAfter=3))

    # Education
    story.append(Paragraph("EDUCATION", section_heading))
    tedu = Table([
        [
            Paragraph("<b>Master of Computer Applications (MCA)</b> — Marian College Kuttikanam, MG University, Kerala", body_style),
            Paragraph("<font size=8>2024 – 2026</font>", ParagraphStyle('E1', parent=body_style, alignment=2))
        ],
        [
            Paragraph("<b>Bachelor of Science — Botany (BSc)</b> — Bharata Mata College, MG University, Kerala", body_style),
            Paragraph("<font size=8>2020 – 2023</font>", ParagraphStyle('E2', parent=body_style, alignment=2))
        ]
    ], colWidths=[420, 120])
    tedu.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(tedu)
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=2, spaceAfter=3))

    # Personal Information
    story.append(Paragraph("PERSONAL INFORMATION", section_heading))
    story.append(Paragraph("<b>Nationality:</b> Indian | <b>Availability:</b> Immediate | <b>Languages:</b> English, Malayalam (Native), Tamil & Hindi (Conversational) | <b>Open to Relocation</b>", body_style))

    doc.build(story)
    print(f"Generated clean PDF resume at: {output_path}")

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "resume.pdf"
    build_pdf(out)
