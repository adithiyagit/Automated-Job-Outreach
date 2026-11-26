"""
Structured Candidate Profile for Adithiya B Vinu
"""

CANDIDATE_DATA = {
    "personal": {
        "name": "Adithiya B Vinu",
        "title": "ERP Functional Consultant | Project Coordinator | QA & UAT",
        "email": "adithiyavinu.b@gmail.com",
        "phone": "+91 96337 83038",
        "location": "Kochi, Kerala, India",
        "linkedin": "https://linkedin.com/in/adithiya-b-vinu",
        "open_to_relocation": True,
        "availability": "Immediate",
        "languages": ["English", "Malayalam (Native)", "Tamil & Hindi (Conversational)"]
    },
    "summary": (
        "ERP professional with hands-on experience across the full implementation lifecycle — "
        "functional testing, UAT, BRD/FRD documentation, and change control on a live, multi-module Odoo rollout. "
        "Skilled at analyzing business processes against system capabilities, identifying gaps, and translating "
        "requirements into validated configurations, while bridging business users, developers, and vendors. "
        "Seeking a structured ERP Functional Consultant, Business Analyst, or Project Coordinator role globally."
    ),
    "core_competencies": [
        "Project Delivery & Change Control: SDLC (Requirements -> Design -> Build -> Test -> Deploy), CR scoping & tracking, Jira, Trello",
        "Stakeholder & Vendor Coordination: Functional liaison between business users, developers, and 3rd-party vendors; SLA adherence",
        "Business Analysis: BRD & FRD authoring, requirement gathering, gap analysis, process mapping, workflow documentation",
        "Quality & Functional Testing: Test case design & execution, UAT coordination & sign-off, defect logging & tracking, hypercare support",
        "Documentation & Training: SOPs, process flowcharts, technical handovers, end-user training & enablement",
        "Tools & Platforms: Odoo (CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, HR), ERPNext/Frappe, Jira, Trello, MS Excel"
    ],
    "experience": [
        {
            "role": "Junior Project Manager cum Functional Consultant",
            "company": "Empire AE IT Services, Kochi",
            "period": "Jan 2026 – Present",
            "highlights": [
                "Tested and validated end-to-end Odoo workflows across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR modules, ensuring functional accuracy before deployment.",
                "Designed and executed structured test cases; logged defects and coordinated with developers for resolution and regression testing after updates.",
                "Analyzed client business processes against Odoo capabilities, identified gaps, and authored BRD/FRD-aligned SOPs and approval-authority workflows across six business functions.",
                "Led UAT planning and execution, authoring test plans, defect reports, and securing sign-off documentation to ensure on-time, on-spec deployment.",
                "Delivered end-user training across nine store locations using a rotational batch rollout plan, reducing post-go-live support load during hypercare."
            ]
        },
        {
            "role": "Python / ERPNext Developer — Intern",
            "company": "Turqosoft Solutions, Kochi",
            "period": "Nov 2025 – Jan 2026",
            "highlights": [
                "Managed change requests end-to-end using Jira — scoping requirements, sprint planning, and delivering documented handovers to the SysAdmin team within agreed SLAs.",
                "Translated client requirements into ERPNext workflows following structured SDLC phases; authored SOPs and led knowledge-sharing sessions."
            ]
        }
    ],
    "projects": [
        {
            "title": "Jewellery Retail ERP Implementation — Odoo (2026)",
            "description": "Coordinated a live multi-module Odoo rollout across nine retail locations — requirements gathering, change control, BRD/FRD-aligned SOPs, UAT, and end-user training."
        },
        {
            "title": "Fleet Management System — ERPNext (2025–2026)",
            "description": "Self-directed project covering vehicle tracking, maintenance scheduling, and fuel logging, built to practice requirements-to-deployment workflow end to end."
        }
    ],
    "education": [
        {
            "degree": "Master of Computer Applications (MCA)",
            "institution": "Marian College Kuttikanam, MG University, Kerala",
            "period": "2024 – 2026"
        },
        {
            "degree": "Bachelor of Science — Botany (BSc)",
            "institution": "Bharata Mata College, MG University, Kerala",
            "period": "2020 – 2023"
        }
    ]
}

def get_candidate_summary_text() -> str:
    """Returns a rich, formatted text summary of the candidate's profile for AI prompting."""
    p = CANDIDATE_DATA["personal"]
    exp_text = "\n".join([
        f"- {exp['role']} at {exp['company']} ({exp['period']}):\n  " + "\n  ".join(f"* {h}" for h in exp["highlights"])
        for exp in CANDIDATE_DATA["experience"]
    ])
    proj_text = "\n".join([
        f"- {prj['title']}: {prj['description']}" for prj in CANDIDATE_DATA["projects"]
    ])
    comp_text = "\n".join([f"- {c}" for c in CANDIDATE_DATA["core_competencies"]])

    return f"""
Candidate: {p['name']}
Title: {p['title']}
Contact: Email: {p['email']} | Phone: {p['phone']} | Location: {p['location']} (Immediate availability, Open to Relocation)
LinkedIn: {p['linkedin']}

Professional Summary:
{CANDIDATE_DATA['summary']}

Core Competencies:
{comp_text}

Professional Experience:
{exp_text}

Featured Implementation Projects:
{proj_text}

Education:
- Master of Computer Applications (MCA) (2024-2026)
- Bachelor of Science (BSc) (2020-2023)
""".strip()
