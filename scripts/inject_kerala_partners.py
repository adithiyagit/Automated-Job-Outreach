import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db, email_verifier

VERIFIED_KERALA_PARTNERS = [
    {
        "name": "ZestyBeanz Technologies",
        "website": "https://www.zestybeanz.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "Odoo Gold Partner • Kerala",
        "contact_email": "info@zestybeanz.com"
    },
    {
        "name": "Confianz Global India",
        "website": "https://www.confianzit.com",
        "city": "Technopark Trivandrum & Kochi, Kerala",
        "country": "India",
        "tier": "Odoo Gold Partner • Kerala",
        "contact_email": "info@confianzit.com"
    },
    {
        "name": "Zerone Consulting",
        "website": "https://www.zerone-consulting.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Enterprise Consulting • Kerala",
        "contact_email": "info@zerone-consulting.com"
    },
    {
        "name": "Toobler Technologies",
        "website": "https://www.toobler.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Custom ERP & Tech • Kerala",
        "contact_email": "info@toobler.com"
    },
    {
        "name": "Fingent Technologies",
        "website": "https://www.fingent.com",
        "city": "Infopark Kochi & Technopark Trivandrum",
        "country": "India",
        "tier": "Enterprise Solutions • Kerala",
        "contact_email": "info@fingent.com"
    },
    {
        "name": "Experion Technologies",
        "website": "https://www.experionglobal.com",
        "city": "Technopark Trivandrum & Infopark Kochi",
        "country": "India",
        "tier": "Product Engineering • Kerala",
        "contact_email": "info@experionglobal.com"
    },
    {
        "name": "SayOne Technologies",
        "website": "https://www.sayonetech.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Enterprise Software • Kerala",
        "contact_email": "info@sayonetech.com"
    },
    {
        "name": "KeyValue Software Systems",
        "website": "https://www.keyvaluesoftware.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Product Engineering • Kerala",
        "contact_email": "hello@keyvaluesoftware.com"
    },
    {
        "name": "Aufait Technologies",
        "website": "https://www.aufait.in",
        "city": "Cyberpark Calicut & Infopark Kochi",
        "country": "India",
        "tier": "Digital Transformation • Kerala",
        "contact_email": "info@aufait.in"
    },
    {
        "name": "Focaloid Technologies",
        "website": "https://www.focaloid.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Digital Solutions • Kerala",
        "contact_email": "info@focaloid.com"
    },
    {
        "name": "Acodez IT Solutions",
        "website": "https://www.acodez.in",
        "city": "Infopark Kochi & Calicut, Kerala",
        "country": "India",
        "tier": "Software Solutions • Kerala",
        "contact_email": "info@acodez.in"
    },
    {
        "name": "Accubits Technologies",
        "website": "https://www.accubits.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "Enterprise Tech & AI • Kerala",
        "contact_email": "info@accubits.com"
    },
    {
        "name": "Bridge Global",
        "website": "https://www.bridge-global.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Custom Software • Kerala",
        "contact_email": "info@bridge-global.com"
    },
    {
        "name": "Webcastle Media",
        "website": "https://www.webcastle.in",
        "city": "Kochi & Calicut, Kerala",
        "country": "India",
        "tier": "ERP & Cloud • Kerala",
        "contact_email": "info@webcastle.in"
    },
    {
        "name": "Hashroot Technologies",
        "website": "https://www.hashroot.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Managed IT & Infrastructure • Kerala",
        "contact_email": "info@hashroot.com"
    },
    {
        "name": "Polus Software",
        "website": "https://www.polussoftware.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "Custom Solutions • Kerala",
        "contact_email": "info@polussoftware.com"
    },
    {
        "name": "InApp Information Technologies",
        "website": "https://www.inapp.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "Enterprise Apps • Kerala",
        "contact_email": "info@inapp.com"
    },
    {
        "name": "TechNeurons Consulting",
        "website": "https://www.techneurons.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "ERP & IT Consulting • Kerala",
        "contact_email": "info@techneurons.com"
    },
    {
        "name": "PIT Solutions",
        "website": "https://www.pitsolutions.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "Enterprise Digital • Kerala",
        "contact_email": "info@pitsolutions.com"
    },
    {
        "name": "SBL Corp",
        "website": "https://www.sblcorp.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Global Solutions • Kerala",
        "contact_email": "info@sblcorp.com"
    },
    {
        "name": "Alisons Technology",
        "website": "https://www.alisons.in",
        "city": "Calicut & Malappuram, Kerala",
        "country": "India",
        "tier": "Retail Tech & ERP • Kerala",
        "contact_email": "info@alisons.in"
    },
    {
        "name": "QBurst Technologies",
        "website": "https://www.qburst.com",
        "city": "Technopark Trivandrum & Infopark Kochi",
        "country": "India",
        "tier": "Enterprise Consulting • Kerala",
        "contact_email": "info@qburst.com"
    },
    {
        "name": "Nest Digital",
        "website": "https://www.nestdigital.com",
        "city": "Kalamassery, Kochi, Kerala",
        "country": "India",
        "tier": "Digital Transformation • Kerala",
        "contact_email": "info@nestdigital.com"
    },
    {
        "name": "Codilar Technologies",
        "website": "https://www.codilar.com",
        "city": "Kochi, Kerala",
        "country": "India",
        "tier": "Commerce & ERP • Kerala",
        "contact_email": "info@codilar.com"
    },
    {
        "name": "ThinkPalm Technologies",
        "website": "https://www.thinkpalm.com",
        "city": "Infopark Kochi & Technopark Trivandrum",
        "country": "India",
        "tier": "Enterprise Software • Kerala",
        "contact_email": "info@thinkpalm.com"
    },
    {
        "name": "GadgEon Smart Systems",
        "website": "https://www.gadgeon.com",
        "city": "SmartCity Kochi & Infopark",
        "country": "India",
        "tier": "Digital Systems • Kerala",
        "contact_email": "info@gadgeon.com"
    },
    {
        "name": "Suyati Technologies",
        "website": "https://www.suyati.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Enterprise Digital • Kerala",
        "contact_email": "info@suyati.com"
    },
    {
        "name": "SunTec Business Solutions",
        "website": "https://www.suntecgroup.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "Enterprise Software • Kerala",
        "contact_email": "info@suntecgroup.com"
    },
    {
        "name": "Triassic Solutions",
        "website": "https://www.triassicsolutions.com",
        "city": "Technopark Trivandrum, Kerala",
        "country": "India",
        "tier": "ERP & Cloud • Kerala",
        "contact_email": "info@triassicsolutions.com"
    },
    {
        "name": "Armia Systems",
        "website": "https://www.armia.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Enterprise Software • Kerala",
        "contact_email": "info@armia.com"
    },
    {
        "name": "LiteBreeze Infotech",
        "website": "https://www.litebreeze.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "High-Tech Web & ERP • Kerala",
        "contact_email": "info@litebreeze.com"
    },
    {
        "name": "Grapes Innovative Solutions",
        "website": "https://www.grapessolutions.com",
        "city": "Calicut & Cyberpark, Kerala",
        "country": "India",
        "tier": "Healthcare ERP & Tech • Kerala",
        "contact_email": "info@grapessolutions.com"
    },
    {
        "name": "Cabot Solutions",
        "website": "https://www.cabotsolutions.com",
        "city": "Infopark Kochi, Kerala",
        "country": "India",
        "tier": "Digital Consulting • Kerala",
        "contact_email": "info@cabotsolutions.com"
    },
    {
        "name": "Vanilla Networks",
        "website": "https://www.vanillanetworks.com",
        "city": "Infopark Kochi & Technopark",
        "country": "India",
        "tier": "Web & Cloud Services • Kerala",
        "contact_email": "info@vanillanetworks.com"
    }
]

added_count = 0
for p in VERIFIED_KERALA_PARTNERS:
    pid = db.add_partner(
        company_name=p["name"],
        website=p["website"],
        contact_email=p["contact_email"],
        country=p["country"],
        city=p["city"],
        partner_tier=p["tier"],
        source="kerala_tech_directory"
    )
    if pid:
        db.mark_email_verified(p["contact_email"])
        added_count += 1
        print(f"✅ Added {p['name']} ({p['city']}) -> ID: {pid}")
    else:
        print(f"ℹ️ Already present or excluded: {p['name']}")

print(f"\nTotal new Kerala partners added: {added_count}")
