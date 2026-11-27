import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db, email_verifier

BANGALORE_PARTNERS = [
    {"name": "Trigent Software Bangalore", "website": "https://www.trigent.com", "city": "Bangalore", "country": "India", "tier": "Enterprise Software & Cloud • Bangalore", "contact_email": "sales@trigent.com"},
    {"name": "Embitel Technologies", "website": "https://www.embitel.com", "city": "Bangalore", "country": "India", "tier": "Digital Commerce & ERP • Bangalore", "contact_email": "sales@embitel.com"},
    {"name": "Sonata Software Bangalore", "website": "https://www.sonata-software.com", "city": "Bangalore", "country": "India", "tier": "Enterprise Modernization • Bangalore", "contact_email": "info@sonata-software.com"},
    {"name": "Happiest Minds Technologies", "website": "https://www.happiestminds.com", "city": "Bangalore", "country": "India", "tier": "Digital Transformation • Bangalore", "contact_email": "business@happiestminds.com"},
    {"name": "Torry Harris Integration Solutions", "website": "https://www.torryharris.com", "city": "Bangalore", "country": "India", "tier": "Enterprise Integration • Bangalore", "contact_email": "info@torryharris.com"},
    {"name": "Nous Infosystems Bangalore", "website": "https://www.nousinfosystems.com", "city": "Bangalore", "country": "India", "tier": "Digital Solutions & ERP • Bangalore", "contact_email": "info@nousinfosystems.com"},
    {"name": "SLK Software Bangalore", "website": "https://www.slksoftware.com", "city": "Bangalore", "country": "India", "tier": "Automation & Enterprise AI • Bangalore", "contact_email": "info@slksoftware.com"},
    {"name": "Indium Software Bangalore", "website": "https://www.indiumsoftware.com", "city": "Bangalore", "country": "India", "tier": "Digital Engineering • Bangalore", "contact_email": "info@indiumsoftware.com"},
    {"name": "ITC Infotech Bangalore", "website": "https://www.itcinfotech.com", "city": "Bangalore", "country": "India", "tier": "Enterprise Solutions • Bangalore", "contact_email": "contactus@itcinfotech.com"},
    {"name": "Sasken Technologies", "website": "https://www.sasken.com", "city": "Bangalore", "country": "India", "tier": "Product Engineering • Bangalore", "contact_email": "info@sasken.com"},
    {"name": "Robosoft Technologies", "website": "https://www.robosoftin.com", "city": "Bangalore", "country": "India", "tier": "Digital Transformation • Bangalore", "contact_email": "info@robosoftin.com"},
    {"name": "Maveric Systems Bangalore", "website": "https://www.maveric-systems.com", "city": "Bangalore", "country": "India", "tier": "Tech Transformation • Bangalore", "contact_email": "info@maveric-systems.com"}
]

HYDERABAD_PARTNERS = [
    {"name": "Ray Business Technologies", "website": "https://www.raybiztech.com", "city": "HITEC City, Hyderabad", "country": "India", "tier": "Odoo & Enterprise ERP • Hyderabad", "contact_email": "sales@raybiztech.com"},
    {"name": "Innominds Software Hyderabad", "website": "https://www.innominds.com", "city": "HITEC City, Hyderabad", "country": "India", "tier": "Product Engineering • Hyderabad", "contact_email": "info@innominds.com"},
    {"name": "Cyient Technologies Hyderabad", "website": "https://www.cyient.com", "city": "Madhapur, Hyderabad", "country": "India", "tier": "Enterprise Digital • Hyderabad", "contact_email": "connect@cyient.com"},
    {"name": "Cigniti Technologies Hyderabad", "website": "https://www.cigniti.com", "city": "HITEC City, Hyderabad", "country": "India", "tier": "Quality & Digital Eng • Hyderabad", "contact_email": "info@cigniti.com"},
    {"name": "Techwave Consulting Hyderabad", "website": "https://www.techwave.net", "city": "HITEC City, Hyderabad", "country": "India", "tier": "ERP & Cloud Services • Hyderabad", "contact_email": "info@techwave.net"},
    {"name": "ValueMomentum Hyderabad", "website": "https://www.valuemomentum.com", "city": "Gachibowli, Hyderabad", "country": "India", "tier": "Enterprise Digital • Hyderabad", "contact_email": "info@valuemomentum.com"},
    {"name": "Miracle Software Systems", "website": "https://www.miraclesoft.com", "city": "Madhapur, Hyderabad", "country": "India", "tier": "Cloud & ERP Solutions • Hyderabad", "contact_email": "info@miraclesoft.com"},
    {"name": "Evoke Technologies Hyderabad", "website": "https://www.evoketechnologies.com", "city": "HITEC City, Hyderabad", "country": "India", "tier": "Enterprise Software • Hyderabad", "contact_email": "info@evoketechnologies.com"},
    {"name": "AppShark Software Hyderabad", "website": "https://www.appshark.com", "city": "HITEC City, Hyderabad", "country": "India", "tier": "Custom CRM & ERP • Hyderabad", "contact_email": "info@appshark.com"},
    {"name": "SenecaGlobal Hyderabad", "website": "https://www.senecaglobal.com", "city": "Gachibowli, Hyderabad", "country": "India", "tier": "Enterprise Software & Cloud • Hyderabad", "contact_email": "info@senecaglobal.com"}
]

print("=== INJECTING BANGALORE & HYDERABAD PARTNERS ===")
blr_added = 0
for p in BANGALORE_PARTNERS:
    pid = db.add_partner(
        company_name=p["name"],
        website=p["website"],
        contact_email=p["contact_email"],
        country=p["country"],
        city=p["city"],
        partner_tier=p["tier"],
        source="bangalore_tech_directory"
    )
    if pid:
        db.mark_email_verified(p["contact_email"])
        blr_added += 1
        print(f"✅ Added {p['name']} -> ID {pid}")
    else:
        print(f"ℹ️ Already exists: {p['name']}")

hyd_added = 0
for p in HYDERABAD_PARTNERS:
    pid = db.add_partner(
        company_name=p["name"],
        website=p["website"],
        contact_email=p["contact_email"],
        country=p["country"],
        city=p["city"],
        partner_tier=p["tier"],
        source="hyderabad_tech_directory"
    )
    if pid:
        db.mark_email_verified(p["contact_email"])
        hyd_added += 1
        print(f"✅ Added {p['name']} -> ID {pid}")
    else:
        print(f"ℹ️ Already exists: {p['name']}")

print(f"\nResult: Added {blr_added} Bangalore and {hyd_added} Hyderabad partners!")
