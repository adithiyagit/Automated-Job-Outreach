import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db, email_verifier

# Inspect existing Kerala entries
conn = db.get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT id, company_name, city, country, contact_email, status, email_status
    FROM partners
    WHERE (city LIKE '%Kochi%' OR city LIKE '%Kerala%' OR city LIKE '%Trivandrum%' OR city LIKE '%Calicut%')
""")
existing = [dict(r) for r in cur.fetchall()]
print(f"=== CURRENT KERALA COMPANIES IN DB ({len(existing)}) ===")
for e in existing:
    print(f"ID {e['id']} | {e['company_name']} ({e['city']}) | {e['contact_email']} | Status: {e['status']}")
conn.close()

# List of Kerala IT & ERP / Odoo companies to test and verify
KERALA_CANDIDATES = [
    {"name": "Bassam Infotech Odoo Gold Partner", "website": "https://www.bassaminfotech.com", "city": "Calicut & Infopark Kochi, Kerala", "country": "India", "tier": "Odoo Gold Partner", "contact_email": "info@bassaminfotech.com"},
    {"name": "Cybrosys Technologies", "website": "https://www.cybrosys.com", "city": "Cyberpark Calicut & Kochi, Kerala", "country": "India", "tier": "Odoo Gold Partner", "contact_email": "info@cybrosys.com"},
    {"name": "BroadTech Innovations", "website": "https://www.broadtech-innovations.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Odoo Silver Partner", "contact_email": "info@broadtech-innovations.com"},
    {"name": "Confianz Global", "website": "https://www.confianzit.com", "city": "Technopark Trivandrum & Kochi, Kerala", "country": "India", "tier": "Odoo Gold Partner", "contact_email": "info@confianzit.com"},
    {"name": "Techvantage Systems", "website": "https://www.techvantagesystems.com", "city": "Technopark Trivandrum & Infopark Kochi", "country": "India", "tier": "ERP Ready Partner", "contact_email": "info@techvantagesystems.com"},
    {"name": "ZestyBeanz Technologies", "website": "https://www.zestybeanz.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Odoo Gold Partner", "contact_email": "info@zestybeanz.com"},
    {"name": "Zerone Consulting", "website": "https://www.zerone-consulting.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Software", "contact_email": "info@zerone-consulting.com"},
    {"name": "Cabot Technology Solutions", "website": "https://www.cabotitsolutions.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Consulting", "contact_email": "info@cabotitsolutions.com"},
    {"name": "Toobler Technologies", "website": "https://www.toobler.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Custom Software & ERP", "contact_email": "info@toobler.com"},
    {"name": "Fingent Technologies", "website": "https://www.fingent.com", "city": "Infopark Kochi & Technopark Trivandrum", "country": "India", "tier": "Enterprise ERP & Consulting", "contact_email": "info@fingent.com"},
    {"name": "Experion Technologies", "website": "https://www.experionglobal.com", "city": "Technopark Trivandrum & Infopark Kochi", "country": "India", "tier": "Enterprise Digital Solutions", "contact_email": "info@experionglobal.com"},
    {"name": "SayOne Technologies", "website": "https://www.sayonetech.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Software & Cloud", "contact_email": "info@sayonetech.com"},
    {"name": "KeyValue Software Systems", "website": "https://www.keyvaluesoftware.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Product Engineering", "contact_email": "hello@keyvaluesoftware.com"},
    {"name": "Aufait Technologies", "website": "https://www.aufait.in", "city": "Cyberpark Calicut & Infopark Kochi", "country": "India", "tier": "Enterprise Digital Solutions", "contact_email": "info@aufait.in"},
    {"name": "Focaloid Technologies", "website": "https://www.focaloid.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Digital Transformation", "contact_email": "info@focaloid.com"},
    {"name": "Acodez IT Solutions", "website": "https://www.acodez.in", "city": "Infopark Kochi & Calicut", "country": "India", "tier": "Digital & Software Solutions", "contact_email": "info@acodez.in"},
    {"name": "Accubits Technologies", "website": "https://www.accubits.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Enterprise Tech & AI", "contact_email": "info@accubits.com"},
    {"name": "Bridge Global", "website": "https://www.bridge-global.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Software Solutions", "contact_email": "info@bridge-global.com"},
    {"name": "Webcastle Media", "website": "https://www.webcastle.in", "city": "Kochi & Calicut, Kerala", "country": "India", "tier": "ERP & Web Solutions", "contact_email": "info@webcastle.in"},
    {"name": "Hashroot Technologies", "website": "https://www.hashroot.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Managed IT & Cloud", "contact_email": "info@hashroot.com"},
    {"name": "Polus Software", "website": "https://www.polussoftware.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Custom Software Solutions", "contact_email": "info@polussoftware.com"},
    {"name": "InApp Information Technologies", "website": "https://www.inapp.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Enterprise App Development", "contact_email": "info@inapp.com"},
    {"name": "Stepping Stone Technologies", "website": "https://www.steppingstone.co.in", "city": "Kochi, Kerala", "country": "India", "tier": "Enterprise Tech", "contact_email": "info@steppingstone.co.in"},
    {"name": "TechNeurons Consulting", "website": "https://www.techneurons.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Software & Consulting", "contact_email": "info@techneurons.com"},
    {"name": "PIT Solutions", "website": "https://www.pitsolutions.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Enterprise Digital Services", "contact_email": "info@pitsolutions.com"},
    {"name": "SBL Corp", "website": "https://www.sblcorp.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Solutions", "contact_email": "info@sblcorp.com"},
    {"name": "Alisons Technology", "website": "https://www.alisons.in", "city": "Calicut & Malappuram, Kerala", "country": "India", "tier": "Retail Tech & ERP", "contact_email": "info@alisons.in"},
    {"name": "QBurst Technologies", "website": "https://www.qburst.com", "city": "Technopark Trivandrum & Infopark Kochi", "country": "India", "tier": "Enterprise Software & Consulting", "contact_email": "info@qburst.com"},
    {"name": "Nest Digital", "website": "https://www.nestdigital.com", "city": "Kalamassery, Kochi, Kerala", "country": "India", "tier": "Digital Transformation", "contact_email": "info@nestdigital.com"},
    {"name": "Alenu IT Solutions", "website": "https://www.alenu.in", "city": "Kochi, Kerala", "country": "India", "tier": "ERP & Cloud Services", "contact_email": "info@alenu.in"},
    {"name": "Codilar Technologies", "website": "https://www.codilar.com", "city": "Kochi, Kerala", "country": "India", "tier": "Commerce & ERP Solutions", "contact_email": "info@codilar.com"}
]

print(f"\nTesting MX Deliverability for {len(KERALA_CANDIDATES)} Kerala candidates...")
valid_kerala = []
blocked_kerala = []

for c in KERALA_CANDIDATES:
    email = c["contact_email"]
    is_val, reason = email_verifier.verify_email_deliverability(email)
    if is_val:
        valid_kerala.append(c)
        print(f"  [VALID MX] {c['name']} ({email}) - {c['city']}")
    else:
        blocked_kerala.append((c, reason))
        print(f"  [BLOCKED] {c['name']} ({email}) - {reason}")

print(f"\nResult: {len(valid_kerala)} Valid | {len(blocked_kerala)} Blocked")
