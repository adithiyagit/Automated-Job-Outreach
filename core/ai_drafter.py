"""
AI Application Drafter and Multi-Region Tailoring Engine
Generates customized, culturally nuanced cold outreach and cover letters for Adithiya B Vinu
tailored specifically for different countries and regions globally (Middle East/Gulf, DACH/Central Europe,
Western Europe/UK, North America, APAC/Remote), powered by Gemini AI with smart regional fallbacks.
"""
import re
import json
from typing import Dict, Any, Tuple
import config
from core import candidate_profile

def get_region_category(country_str: str) -> str:
    """Categorizes country into regional hiring culture buckets."""
    c = (country_str or "").lower().strip()

    if any(k in c for k in ["kerala", "kochi", "cochin", "trivandrum", "thiruvananthapuram", "calicut", "kozhikode", "ernakulam", "infopark", "technopark", "cyberpark", "malappuram", "thrissur"]):
        return "kerala"
    elif any(k in c for k in ["india", "bharat", "bengaluru", "bangalore", "mumbai", "pune", "ahmedabad", "delhi", "gurgaon", "noida", "hyderabad", "chennai"]):
        return "india"
    elif any(k in c for k in ["emirates", "uae", "dubai", "abu dhabi", "saudi", "ksa", "qatar", "oman", "bahrain", "kuwait"]):
        return "middle_east"
    elif any(k in c for k in ["switzerland", "germany", "austria", "deutschland"]):
        return "dach_europe"
    elif any(k in c for k in ["united kingdom", "uk", "britain", "france", "belgium", "netherlands", "spain", "ireland", "italy"]):
        return "western_europe"
    elif any(k in c for k in ["united states", "usa", "us", "canada"]):
        return "north_america"
    else:
        return "apac_global"

def generate_regional_template(
    company_name: str,
    country: str = "Global",
    job_title: str = "Junior Project Manager / ERP Functional Consultant",
    tier: str = "Gold"
) -> Dict[str, Any]:
    """
    Generates culturally adapted outreach specific to the target country/region.
    """
    p = candidate_profile.CANDIDATE_DATA["personal"]
    region = get_region_category(country)
    subject = f"Application: {job_title} — {p['name']}"

    # 0. KERALA LOCAL TECH ECOSYSTEM (Infopark Kochi, Technopark Trivandrum, Cyberpark Calicut)
    # Focus: Based directly in Kochi, Immediate 0-Day Joiner, MCA from Marian College Kuttikanam, live 9-store Odoo retail rollout in Kerala
    if region == "kerala":
        subject = f"Application: {job_title} — {p['name']} (Immediate Joiner | Kochi, Kerala)"
        body = f"""Dear Hiring Team at {company_name},

I hope this email finds you well. I am writing to apply for the position of {job_title} or Business Analyst with {company_name} in Kerala.

Based directly in Kochi, Kerala, I am an immediate joiner (0 days notice period) and available for immediate on-site reporting across Infopark Kochi, Technopark Trivandrum, Cyberpark Calicut, or hybrid deployment.

I bring hands-on functional experience across the complete ERP lifecycle on a live, multi-module Odoo rollout. Currently serving as Junior Project Manager cum Functional Consultant at Empire AE IT Services in Kochi, my core deliverables include:
• Tested and validated end-to-end Odoo workflows across six core modules: CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR.
• Authored BRD/FRD-aligned SOPs, process workflows, and approval matrices, converting business requirements into validated configurations.
• Coordinated client UAT from test planning to defect logging in Jira and final sign-off documentation.
• Led rotational batch user training and hypercare support across nine store branches during a live retail rollout.

I hold an MCA (Master of Computer Applications) from Marian College Kuttikanam (MG University, Kerala) with dual functional experience across Odoo and ERPNext/Python SDLC workflows.

Key Logistics:
• Current Location: Kochi, Kerala (Available for immediate in-person interview & joining)
• Notice Period: Immediate Joiner (0 days notice period)
• Mobility: Ready to report to office immediately across Kochi, Trivandrum, or Calicut

I have attached my resume for your review. I would welcome the opportunity to discuss how my implementation background can support {company_name}'s upcoming client deliverables.

Thank you for your time and consideration.

Warm regards,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
Location: {p['location']} (Immediate Availability)
LinkedIn: {p['linkedin']}
""".strip()

    # 1. INDIA & DOMESTIC IT ECOSYSTEM
    # Focus: Immediate Joiner (0 days notice period), MCA from Kerala, hands-on 9-store rollout, Odoo & ERPNext, pan-India mobility / remote
    elif region == "india":
        body = f"""Dear Hiring Team at {company_name},

I hope this email finds you well. I am writing to apply for the position of {job_title} or Business Analyst supporting {company_name}'s ERP consulting and implementation projects.

I bring hands-on functional experience across the complete ERP lifecycle on a live, multi-module Odoo rollout. Currently serving as Junior Project Manager cum Functional Consultant at Empire AE IT Services, my core contributions include:
• Tested and validated end-to-end Odoo workflows across six core modules: CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR.
• Authored BRD/FRD-aligned SOPs, process workflows, and approval matrices, converting business requirements into validated configurations.
• Coordinated client UAT from test planning to defect logging in Jira and final sign-off documentation.
• Led rotational batch user training and hypercare support across nine store branches during a live retail rollout.

I hold an MCA (Master of Computer Applications) from Marian College Kuttikanam (MG University, Kerala) with dual experience across Odoo and ERPNext/Python SDLC workflows.

Key Highlights for Your Consideration:
• Notice Period: Immediate Joiner (0 days notice period)
• Current Location: Kochi, Kerala
• Mobility: Ready to relocate immediately (Bangalore, Pune, Mumbai, Ahmedabad, Delhi-NCR, Hyderabad, Chennai) or work remotely

I have attached my resume for your review. I would welcome the opportunity to discuss how my implementation background can support {company_name}'s upcoming client deliverables.

Thank you for your time and consideration.

Warm regards,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
LinkedIn: {p['linkedin']}
""".strip()

    # 1. MIDDLE EAST & GULF (UAE, Saudi Arabia, Qatar, Oman)
    # Focus: Immediate deployment readiness, multi-branch rollout delivery, fast UAT sign-off, relocation readiness
    elif region == "middle_east":
        body = f"""Dear Hiring Team at {company_name},

I hope this email finds you well. I am writing to express my strong interest in joining {company_name}'s ERP practice in {country} as a {job_title} or Business Analyst.

With extensive on-ground and functional experience delivering a live, multi-module Odoo rollout across 9 retail store locations, I specialize in bridging business requirements with technical delivery. In my current role at Empire AE IT Services, I have:
• Tested and validated complete end-to-end Odoo workflows across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR modules.
• Authored BRD/FRD-aligned SOPs and multi-tier approval workflows across six business functions.
• Managed client UAT from test planning to defect tracking in Jira and final sign-off documentation.
• Led rotational batch user enablement across 9 store locations, substantially minimizing post-go-live hypercare issues.

Given {company_name}'s standing as an esteemed Odoo partner in the region, I can hit the ground running to support your ongoing implementations and client rollouts.

I am an Indian national with an MCA background, available immediately, and fully open to immediate relocation to {country} or on-site deployment.

My resume is attached for your review. I would welcome the opportunity to connect for a 10-minute introductory discussion.

Warm regards,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
Location: {p['location']} (Immediate Availability | Open to Relocation)
LinkedIn: {p['linkedin']}
""".strip()

    # 2. DACH / CENTRAL EUROPE (Switzerland, Germany, Austria)
    # Focus: Precision, structured SDLC, BRD/FRD functional specifications, rigorous test case coverage, quality sign-offs
    elif region == "dach_europe":
        body = f"""Dear Hiring Team at {company_name},

I am writing to formally apply for the position of {job_title} supporting {company_name}'s Odoo implementations in {country}.

As an ERP specialist experienced in structured SDLC delivery on live Odoo enterprise environments, my core strength lies in functional process analysis, documentation, and quality validation. At Empire AE IT Services, my contributions include:
• Functional Specification & Gap Analysis: Authored detailed BRD and FRD documentation, process flowcharts, and SOPs translating complex operational workflows into validated system configurations.
• Multi-Module Validation: Designed and executed structured test cases across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR modules.
• UAT Management: Led UAT cycles, authored defect logs, coordinated with developers for regression testing, and secured formal stakeholder sign-offs.
• Rollout Delivery: Coordinated the implementation and user enablement across nine operating locations, ensuring high data accuracy and operational stability.

I hold a Master of Computer Applications (MCA) and bring hands-on familiarity with both Odoo and ERPNext/Jira workflows. I work proficiently in English and am adaptable to international consulting standards.

I have attached my curriculum vitae for your consideration. I am immediately available and open to remote collaboration or relocation to {country}.

Thank you for your time and evaluation. I would be pleased to introduce myself in a brief introductory call.

Sincerely,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
LinkedIn: {p['linkedin']}
""".strip()

    # 3. WESTERN EUROPE & UK (United Kingdom, France, Belgium, Netherlands, Spain)
    # Focus: Stakeholder coordination, business analysis, bridging clients and technical teams, change control
    elif region == "western_europe":
        body = f"""Dear Hiring Team at {company_name},

I hope you are having a productive week. I am writing to submit my application for {job_title} or Business Analyst roles within {company_name}'s Odoo consulting team in {country}.

My background centers on delivering live, multi-module Odoo implementations where functional business analysis and proactive stakeholder management are critical. Working as Junior Project Manager cum Functional Consultant at Empire AE IT Services, my key deliverables have included:
• End-to-End Module Testing: Testing and validating client workflows across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR.
• Requirements & SOP Authoring: Developing BRD/FRD documentation, functional process maps, and approval matrices across diverse business units.
• UAT Coordination: Leading user acceptance testing, authoring test suites, defect management, and securing stakeholder sign-off on schedule.
• Change Enablement: Rolling out hands-on end-user training across nine store branches, ensuring rapid adoption during the critical hypercare phase.

With an MCA degree and practical grounding in Jira-driven change control and ERP systems, I can quickly integrate into your team to assist with business requirements, testing, and client coordination.

Please find my resume attached. I am immediately available and welcome remote engagements or discussions regarding relocation.

I look forward to the possibility of discussing how my implementation background aligns with {company_name}'s project pipeline.

Kind regards,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
LinkedIn: {p['linkedin']}
""".strip()

    # 4. NORTH AMERICA (United States, Canada)
    # Focus: High impact, quantifiable metrics, agile problem-solving, rapid turnaround
    elif region == "north_america":
        body = f"""Hi Hiring Team at {company_name},

I am reaching out to apply for the {job_title} role at {company_name}. 

I bring hands-on experience coordinating live Odoo rollouts, conducting functional testing, and bridging the gap between business stakeholders and technical developers. Most recently at Empire AE IT Services, I:
• Validated end-to-end Odoo workflows across 6 core functions: CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR.
• Authored BRD/FRD specifications and standard operating procedures that converted complex business needs into validated configurations.
• Led UAT execution, managing test suites, bug tracking, and milestone sign-offs.
• Coordinated a live 9-store retail rollout, conducting user training that reduced post-launch support tickets during hypercare.

With a Master of Computer Applications (MCA) and hands-on experience in both Odoo and ERPNext/Jira, I am prepared to contribute immediately to {company_name}'s client projects.

My resume is attached. I am available immediately and open to remote engagements or relocation.

I'd welcome the chance to connect for 10 minutes to discuss how my hands-on implementation experience can support your team.

Best regards,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
LinkedIn: {p['linkedin']}
""".strip()

    # 5. APAC & GLOBAL (Singapore, Australia, India, Remote)
    # Focus: Functional versatility, MCA technical depth, cross-timezone collaboration, fast ramp-up
    else:
        body = f"""Dear Hiring Team at {company_name},

I am writing to express my interest in {job_title} or Business Analyst positions with {company_name}.

Having hands-on functional and implementation experience across the full Odoo lifecycle, I specialize in translating complex business processes into validated ERP configurations. In my current role at Empire AE IT Services:
• I validate and test multi-module workflows across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR.
• I author BRD/FRD documentation, SOPs, and approval workflows across six distinct business functions.
• I plan and coordinate user acceptance testing (UAT), defect triage with development teams, and formal sign-offs.
• I coordinated a live rollout across nine operating locations, driving end-user enablement and hypercare stability.

Coupled with a Master of Computer Applications (MCA) and background in ERPNext/Frappe and Jira SDLC tracking, I can quickly step in to support your project coordination and functional consulting teams.

My resume is attached for your review. I am available immediately and fully open to remote, hybrid, or on-site relocation opportunities.

Thank you for your consideration. I look forward to connecting for a brief discussion.

Best regards,

{p['name']}
ERP Functional Consultant | Project Coordinator
Email: {p['email']} | Phone: {p['phone']}
LinkedIn: {p['linkedin']}
""".strip()

    return {
        "subject": subject,
        "body": body,
        "match_score": 93,
        "region": region,
        "source": f"regional_template_{region}"
    }

# Backward compatibility alias
generate_fallback_draft = generate_regional_template

def generate_application_draft(
    company_name: str,
    country: str = "Global",
    job_title: str = "Junior Project Manager / ERP Functional Consultant",
    job_description: str = "",
    partner_tier: str = "Partner"
) -> Dict[str, Any]:
    """
    Generates a personalized application draft adapted to the country hiring culture.
    Uses Gemini AI if configured, otherwise falls back to the regional template engine.
    """
    region = get_region_category(country)
    api_key = config.GEMINI_API_KEY

    if not api_key:
        return generate_regional_template(company_name, country, job_title, partner_tier)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        candidate_summary = candidate_profile.get_candidate_summary_text()

        # Regional cultural instructions
        if region == "india":
            cultural_notes = "Target region is India (Domestic IT/ERP). Emphasize immediate availability (0 days notice period), MCA degree from Kerala, hands-on 9-store live Odoo rollout, and readiness to relocate pan-India (Bangalore/Pune/Mumbai/Ahmedabad/Gurgaon/Hyderabad) or work remotely."
        elif region == "middle_east":
            cultural_notes = "Target region is Middle East (UAE/Saudi/Qatar). Emphasize fast deployment, 9-store retail rollout, immediate joining, and open to relocation."
        elif region == "dach_europe":
            cultural_notes = "Target region is DACH Europe (Switzerland/Germany). Use formal, precise language. Emphasize structured BRD/FRD documentation, quality UAT sign-offs, and SDLC methodology."
        elif region == "western_europe":
            cultural_notes = "Target region is Western Europe (UK/France/Benelux). Balance stakeholder coordination, business analysis, and user enablement."
        elif region == "north_america":
            cultural_notes = "Target region is North America (US/Canada). Use concise, outcome-driven, punchy language with metrics."
        else:
            cultural_notes = "Target region is APAC/Global. Emphasize functional depth across CRM, Sales, Purchase, Inventory, Accounts, Mfg, HR, and MCA background."

        prompt = f"""
You are an expert executive career strategist and technical recruiter.
Draft a highly personalized, compelling, and professional job application email from candidate Adithiya B Vinu to the company "{company_name}" located in "{country}".

Candidate Profile:
{candidate_summary}

Target Company & Role Details:
- Target Company: {company_name}
- Country: {country} (Region: {region})
- Position: {job_title}
- Context / JD: {job_description or 'Odoo ERP Implementation, Consulting, Functional Testing, UAT, and Business Analysis'}

Cultural & Regional Tone Guidelines:
{cultural_notes}

Rules:
1. Subject line format MUST be clean and professional: "Application: {job_title} — Adithiya B Vinu"
2. Body must specifically reference {company_name} and {country}.
3. Highlight core Odoo strengths: CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, HR; BRD/FRD SOPs; UAT sign-offs; and 9-store rollout.
4. Note that resume is attached. Mention immediate availability and open to relocation or remote work.
5. Return a valid JSON object strictly formatted as:
{{
    "subject": "Application: {job_title} — Adithiya B Vinu",
    "body": "...",
    "match_score": 94
}}
Do NOT output any markdown backticks or extra text outside the JSON.
"""

        for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
            try:
                m = genai.GenerativeModel(model_name)
                resp = m.generate_content(prompt)
                if resp and resp.text:
                    cleaned_text = resp.text.strip()
                    if cleaned_text.startswith("```json"):
                        cleaned_text = cleaned_text[7:]
                    if cleaned_text.startswith("```"):
                        cleaned_text = cleaned_text[3:]
                    if cleaned_text.endswith("```"):
                        cleaned_text = cleaned_text[:-3]
                    cleaned_text = cleaned_text.strip()
                    data = json.loads(cleaned_text)
                    return {
                        "subject": data.get("subject", f"Application: {job_title} — Adithiya B Vinu"),
                        "body": data.get("body", ""),
                        "match_score": int(data.get("match_score", 92)),
                        "region": region,
                        "source": f"gemini ({model_name})"
                    }
            except Exception:
                continue

        return generate_regional_template(company_name, country, job_title, partner_tier)

    except Exception as e:
        print(f"Gemini drafting notice: {e}, using regional template.")
        return generate_regional_template(company_name, country, job_title, partner_tier)
