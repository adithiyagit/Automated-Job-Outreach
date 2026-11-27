import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db, ai_drafter

blr_leads = db.get_uncontacted_partners_with_emails(limit=50, country_filter="bangalore")
print(f"=== UNCONTACTED BANGALORE LEADS ({len(blr_leads)}) ===")
for b in blr_leads[:6]:
    print(f"ID {b['id']} | {b['company_name']} | {b['city']} | {b['contact_email']}")

hyd_leads = db.get_uncontacted_partners_with_emails(limit=50, country_filter="hyderabad")
print(f"\n=== UNCONTACTED HYDERABAD LEADS ({len(hyd_leads)}) ===")
for h in hyd_leads[:6]:
    print(f"ID {h['id']} | {h['company_name']} | {h['city']} | {h['contact_email']}")

print("\n--- SAMPLE BANGALORE DRAFT ---")
draft_blr = ai_drafter.generate_application_draft(
    company_name="Trigent Software Bangalore",
    country="Bangalore",
    job_title="Junior Project Manager / ERP Functional Consultant"
)
print("Subject:", draft_blr["subject"])
print("Region:", draft_blr.get("region"))
print("Body Preview:\n", draft_blr["body"][:350], "...")

print("\n--- SAMPLE HYDERABAD DRAFT ---")
draft_hyd = ai_drafter.generate_application_draft(
    company_name="Ray Business Technologies",
    country="Hyderabad",
    job_title="Junior Project Manager / ERP Functional Consultant"
)
print("Subject:", draft_hyd["subject"])
print("Region:", draft_hyd.get("region"))
print("Body Preview:\n", draft_hyd["body"][:350], "...")
