import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import email_verifier

MORE_KERALA = [
    {"name": "ThinkPalm Technologies", "website": "https://www.thinkpalm.com", "city": "Infopark Kochi & Technopark Trivandrum", "country": "India", "tier": "Enterprise Software & IoT", "contact_email": "info@thinkpalm.com"},
    {"name": "GadgEon Smart Systems", "website": "https://www.gadgeon.com", "city": "SmartCity Kochi & Infopark", "country": "India", "tier": "Digital Transformation & IoT", "contact_email": "info@gadgeon.com"},
    {"name": "Suyati Technologies", "website": "https://www.suyati.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Digital Solutions", "contact_email": "info@suyati.com"},
    {"name": "SunTec Business Solutions", "website": "https://www.suntecgroup.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Enterprise Software Solutions", "contact_email": "info@suntecgroup.com"},
    {"name": "Triassic Solutions", "website": "https://www.triassicsolutions.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "Custom Software & ERP", "contact_email": "info@triassicsolutions.com"},
    {"name": "Armia Systems", "website": "https://www.armia.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Software", "contact_email": "info@armia.com"},
    {"name": "LiteBreeze Infotech", "website": "https://www.litebreeze.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "High-Tech Web & ERP", "contact_email": "info@litebreeze.com"},
    {"name": "Grapes Innovative Solutions", "website": "https://www.grapessolutions.com", "city": "Calicut & Cyberpark, Kerala", "country": "India", "tier": "Healthcare ERP & Tech", "contact_email": "info@grapessolutions.com"},
    {"name": "Cabot Solutions", "website": "https://www.cabotsolutions.com", "city": "Infopark Kochi, Kerala", "country": "India", "tier": "Enterprise Digital Consulting", "contact_email": "info@cabotsolutions.com"},
    {"name": "Artin Dynamics", "website": "https://www.artindynamics.com", "city": "Technopark Trivandrum, Kerala", "country": "India", "tier": "AI & Software Systems", "contact_email": "info@artindynamics.com"},
    {"name": "Vanilla Networks", "website": "https://www.vanillanetworks.com", "city": "Infopark Kochi & Technopark", "country": "India", "tier": "Web & Cloud Services", "contact_email": "info@vanillanetworks.com"}
]

print("Testing second batch of Kerala companies...")
for c in MORE_KERALA:
    is_val, reason = email_verifier.verify_email_deliverability(c["contact_email"])
    if is_val:
        print(f"  [VALID MX] {c['name']} ({c['contact_email']}) - {c['city']}")
    else:
        print(f"  [BLOCKED] {c['name']} ({c['contact_email']}) - {reason}")
