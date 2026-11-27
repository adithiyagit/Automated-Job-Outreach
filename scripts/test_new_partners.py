import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import email_verifier

# Candidate partner companies to verify
CANDIDATE_PARTNERS = [
    # --- INDIA (Immediate 0-day notice, Kochi, Bangalore, Mumbai, Ahmedabad, Pune) ---
    {"name": "Pragmatic Techsoft", "website": "https://www.pragtech.co.in", "country": "India", "city": "Pune", "tier": "Gold", "contact_email": "sales@pragtech.co.in"},
    {"name": "Serpent Consulting Services", "website": "https://www.serpentcs.com", "country": "India", "city": "Ahmedabad", "tier": "Gold", "contact_email": "contact@serpentcs.com"},
    {"name": "Confianz Global India", "website": "https://www.confianzit.com", "country": "India", "city": "Trivandrum / Kochi", "tier": "Gold", "contact_email": "info@confianzit.com"},
    {"name": "CandidRoot Solutions", "website": "https://www.candidroot.com", "country": "India", "city": "Ahmedabad", "tier": "Silver", "contact_email": "info@candidroot.com"},
    {"name": "Emipro Technologies", "website": "https://www.emiprotechnologies.com", "country": "India", "city": "Rajkot / Ahmedabad", "tier": "Gold", "contact_email": "info@emiprotechnologies.com"},
    {"name": "Zehntech Technologies", "website": "https://www.zehntech.com", "country": "India", "city": "Indore", "tier": "Silver", "contact_email": "info@zehntech.com"},
    {"name": "Techvantage Systems", "website": "https://www.techvantagesystems.com", "country": "India", "city": "Trivandrum / Kochi", "tier": "Ready", "contact_email": "info@techvantagesystems.com"},
    {"name": "Ksolves India Ltd", "website": "https://www.ksolves.com", "country": "India", "city": "Noida / Pune", "tier": "Gold", "contact_email": "sales@ksolves.com"},
    {"name": "Webkul Software", "website": "https://www.webkul.com", "country": "India", "city": "Noida", "tier": "Gold", "contact_email": "sales@webkul.com"},
    {"name": "Aktiv Software", "website": "https://www.aktivsoftware.com", "country": "India", "city": "Ahmedabad", "tier": "Gold", "contact_email": "info@aktivsoftware.com"},
    {"name": "TechUltra Solutions", "website": "https://www.techultrasolutions.com", "country": "India", "city": "Ahmedabad", "tier": "Silver", "contact_email": "contact@techultrasolutions.com"},
    {"name": "Synconics Technologies", "website": "https://www.synconics.com", "country": "India", "city": "Ahmedabad", "tier": "Gold", "contact_email": "contact@synconics.com"},
    {"name": "DevIntelle Consulting", "website": "https://www.devintellecs.com", "country": "India", "city": "Surat", "tier": "Silver", "contact_email": "info@devintellecs.com"},
    {"name": "Planet Odoo", "website": "https://www.planet-odoo.com", "country": "India", "city": "Ahmedabad", "tier": "Silver", "contact_email": "info@planet-odoo.com"},
    {"name": "Silent Infotech", "website": "https://www.silentinfotech.com", "country": "India", "city": "Surat / Ahmedabad", "tier": "Gold", "contact_email": "info@silentinfotech.com"},
    {"name": "Ascetic Business Solution", "website": "https://www.asceticbs.com", "country": "India", "city": "Ahmedabad", "tier": "Silver", "contact_email": "info@asceticbs.com"},
    {"name": "Uncanny Consulting Services", "website": "https://www.uncannycs.com", "country": "India", "city": "Ahmedabad", "tier": "Silver", "contact_email": "info@uncannycs.com"},
    {"name": "Target Integration India", "website": "https://www.targetintegration.com", "country": "India", "city": "Gurgaon", "tier": "Gold", "contact_email": "info@targetintegration.com"},
    {"name": "Brainvire Infotech India", "website": "https://www.brainvire.com", "country": "India", "city": "Mumbai / Ahmedabad", "tier": "Gold", "contact_email": "info@brainvire.com"},

    # --- UNITED ARAB EMIRATES & MIDDLE EAST ---
    {"name": "Azkatech Middle East", "website": "https://www.azkatech.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "contact@azkatech.com"},
    {"name": "Ever Technologies Dubai", "website": "https://www.ever-technologies.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Silver", "contact_email": "info@ever-technologies.com"},
    {"name": "CloudSys Technologies UAE", "website": "https://www.cloudsys.ae", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@cloudsys.ae"},
    {"name": "SmartWay IT Dubai", "website": "https://www.smartway-me.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Silver", "contact_email": "info@smartway-me.com"},
    {"name": "Silicon Spectra UAE", "website": "https://www.siliconspectra.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Silver", "contact_email": "info@siliconspectra.com"},
    {"name": "CNS Middle East", "website": "https://www.cns-me.com", "country": "United Arab Emirates", "city": "Abu Dhabi / Dubai", "tier": "Gold", "contact_email": "info@cns-me.com"},
    {"name": "Tech Vista Systems Dubai", "website": "https://www.techvistasystems.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@techvistasystems.com"},
    {"name": "Alpha Data UAE", "website": "https://www.alpha.ae", "country": "United Arab Emirates", "city": "Abu Dhabi / Dubai", "tier": "Gold", "contact_email": "info@alpha.ae"},
    {"name": "Intertec Systems UAE", "website": "https://www.intertecsystems.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@intertecsystems.com"},
    {"name": "Al-Futtaim Technologies", "website": "https://www.alfuttaim.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "contact@alfuttaim.com"},

    # --- SAUDI ARABIA (KSA) ---
    {"name": "Buraq Systems KSA", "website": "https://www.buraq.sa", "country": "Saudi Arabia", "city": "Riyadh", "tier": "Gold", "contact_email": "info@buraq.sa"},
    {"name": "Gulf Business Machines KSA", "website": "https://www.gbm.sa", "country": "Saudi Arabia", "city": "Riyadh", "tier": "Gold", "contact_email": "info@gbm.sa"},
    {"name": "Al-Jammaz Technologies KSA", "website": "https://www.al-jammaz.com", "country": "Saudi Arabia", "city": "Riyadh", "tier": "Gold", "contact_email": "info@al-jammaz.com"},

    # --- SWITZERLAND & DACH ---
    {"name": "ERP Open Solutions GmbH", "website": "https://www.erp-open-solutions.ch", "country": "Switzerland", "city": "Zurich", "tier": "Gold", "contact_email": "info@erp-open-solutions.ch"},
    {"name": "Naviq AG", "website": "https://www.naviq.ch", "country": "Switzerland", "city": "Bern", "tier": "Silver", "contact_email": "info@naviq.ch"},
    {"name": "AgilOrg Switzerland", "website": "https://www.agilorg.ch", "country": "Switzerland", "city": "Lausanne", "tier": "Silver", "contact_email": "info@agilorg.ch"},
    {"name": "Abakus IT-Solutions DACH", "website": "https://www.abakus-itsolutions.eu", "country": "Switzerland", "city": "Basel", "tier": "Gold", "contact_email": "info@abakus-itsolutions.eu"},

    # --- GERMANY ---
    {"name": "initOS GmbH", "website": "https://www.initos.com", "country": "Germany", "city": "Magdeburg", "tier": "Gold", "contact_email": "info@initos.com"},
    {"name": "equipago GmbH", "website": "https://www.equipago.com", "country": "Germany", "city": "Munich", "tier": "Silver", "contact_email": "info@equipago.com"},
    {"name": "mana-tec GmbH", "website": "https://www.mana-tec.com", "country": "Germany", "city": "Dresden", "tier": "Gold", "contact_email": "info@mana-tec.com"},
    {"name": "Open-DSI Germany", "website": "https://www.open-dsi.fr", "country": "Germany", "city": "Frankfurt", "tier": "Silver", "contact_email": "contact@open-dsi.fr"},
    {"name": "Data Warehouse GmbH", "website": "https://www.data-warehouse.de", "country": "Germany", "city": "Berlin", "tier": "Silver", "contact_email": "info@data-warehouse.de"},
    {"name": "OBS Solutions GmbH", "website": "https://www.obs-solutions.de", "country": "Germany", "city": "Siegen", "tier": "Gold", "contact_email": "info@obs-solutions.de"},

    # --- UNITED KINGDOM ---
    {"name": "Smart IT UK", "website": "https://www.smart-it.com", "country": "United Kingdom", "city": "Gateshead / London", "tier": "Gold", "contact_email": "info@smart-it.com"},
    {"name": "Silverfinch UK", "website": "https://www.silverfinch.co.uk", "country": "United Kingdom", "city": "London", "tier": "Silver", "contact_email": "info@silverfinch.co.uk"},
    {"name": "Target Integration UK", "website": "https://www.targetintegration.com", "country": "United Kingdom", "city": "Birmingham", "tier": "Gold", "contact_email": "uk@targetintegration.com"},

    # --- UNITED STATES & CANADA ---
    {"name": "Open Source Integrators US", "website": "https://www.opensourceintegrators.com", "country": "United States", "city": "Denver / New York", "tier": "Gold", "contact_email": "info@opensourceintegrators.com"},
    {"name": "Novobi LLC", "website": "https://www.novobi.com", "country": "United States", "city": "Austin, Texas", "tier": "Gold", "contact_email": "info@novobi.com"},
    {"name": "Sodexis Inc", "website": "https://www.sodexis.com", "country": "United States", "city": "Orlando, Florida", "tier": "Gold", "contact_email": "info@sodexis.com"},
    {"name": "OSI Digital US", "website": "https://www.osidigital.com", "country": "United States", "city": "Los Angeles", "tier": "Gold", "contact_email": "info@osidigital.com"},

    # --- SINGAPORE & AUSTRALIA ---
    {"name": "Port Cities Singapore", "website": "https://www.portcities.net", "country": "Singapore", "city": "Singapore", "tier": "Gold", "contact_email": "singapore@portcities.net"},
    {"name": "Willow IT Australia", "website": "https://www.willowit.com.au", "country": "Australia", "city": "Melbourne", "tier": "Gold", "contact_email": "info@willowit.com.au"}
]

print(f"Total candidate partners: {len(CANDIDATE_PARTNERS)}")
verified_list = []
failed_list = []

for p in CANDIDATE_PARTNERS:
    email = p["contact_email"]
    is_valid, reason = email_verifier.verify_email_deliverability(email)
    if is_valid:
        verified_list.append(p)
        print(f"  [VALID] {p['name']} ({email}) - {p['country']}")
    else:
        failed_list.append((p, reason))
        print(f"  [BLOCKED/BOUNCE RISK] {p['name']} ({email}) - {reason}")

print(f"\nSummary: {len(verified_list)} Valid MX | {len(failed_list)} Blocked/Bounced")
