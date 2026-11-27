import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import email_verifier

ADDITIONAL_PARTNERS = [
    {"name": "Bassam Infotech Odoo Gold Partner", "website": "https://www.bassaminfotech.com", "country": "India", "city": "Calicut / Kochi, Kerala", "tier": "Gold", "contact_email": "info@bassaminfotech.com"},
    {"name": "BroadTech Innovations", "website": "https://www.broadtech-innovations.com", "country": "India", "city": "Kochi, Kerala", "tier": "Silver", "contact_email": "info@broadtech-innovations.com"},
    {"name": "Cybrosys Technologies", "website": "https://www.cybrosys.com", "country": "India", "city": "Calicut / Kochi, Kerala", "tier": "Gold", "contact_email": "info@cybrosys.com"},
    {"name": "Bista Solutions India", "website": "https://www.bistasolutions.com", "country": "India", "city": "Mumbai / Bangalore", "tier": "Gold", "contact_email": "sales@bistasolutions.com"},
    {"name": "Banibro IT Solutions", "website": "https://www.banibro.com", "country": "India", "city": "Chennai", "tier": "Gold", "contact_email": "info@banibro.com"},
    {"name": "O2b Technologies", "website": "https://www.o2btechnologies.com", "country": "India", "city": "Noida", "tier": "Gold", "contact_email": "info@o2btechnologies.com"},
    {"name": "Bytes Technolab", "website": "https://www.bytestechnolab.com", "country": "India", "city": "Ahmedabad", "tier": "Gold", "contact_email": "info@bytestechnolab.com"},
    {"name": "Apagen Solutions", "website": "https://www.apagen.com", "country": "India", "city": "Delhi-NCR", "tier": "Gold", "contact_email": "info@apagen.com"},
    {"name": "Geminate Consultancy", "website": "https://www.geminatecs.com", "country": "India", "city": "Surat", "tier": "Silver", "contact_email": "info@geminatecs.com"},
    {"name": "Techneith Technologies", "website": "https://www.techneith.com", "country": "India", "city": "Ahmedabad", "tier": "Ready", "contact_email": "info@techneith.com"},
    {"name": "Dexciss Technology", "website": "https://www.dexciss.com", "country": "India", "city": "Pune", "tier": "Gold", "contact_email": "info@dexciss.com"},
    {"name": "Techloyce India", "website": "https://www.techloyce.com", "country": "India", "city": "Bangalore", "tier": "Gold", "contact_email": "info@techloyce.com"},
    {"name": "Pinnacle Technologies UAE", "website": "https://www.pinnacle.ae", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@pinnacle.ae"},
    {"name": "First Select International Dubai", "website": "https://www.firstselect.ae", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@firstselect.ae"},
    {"name": "Tri-Tech Middle East", "website": "https://www.tritechme.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Silver", "contact_email": "info@tritechme.com"},
    {"name": "Data Capture Systems Dubai", "website": "https://www.dcsme.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@dcsme.com"},
    {"name": "Smart Vision ME", "website": "https://www.smartvision.ae", "country": "United Arab Emirates", "city": "Dubai", "tier": "Silver", "contact_email": "info@smartvision.ae"},
    {"name": "Global Triangles Dubai", "website": "https://www.globaltriangles.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@globaltriangles.com"},
    {"name": "Mindmill Technologies UAE", "website": "https://www.mindmill.com", "country": "United Arab Emirates", "city": "Dubai", "tier": "Gold", "contact_email": "info@mindmill.com"}
]

for p in ADDITIONAL_PARTNERS:
    email = p["contact_email"]
    is_valid, reason = email_verifier.verify_email_deliverability(email)
    if is_valid:
        print(f"  [VALID] {p['name']} ({email}) - {p['country']}")
    else:
        print(f"  [BLOCKED/BOUNCE] {p['name']} ({email}) - {reason}")
