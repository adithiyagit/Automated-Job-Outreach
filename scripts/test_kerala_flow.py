import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db, ai_drafter

kerala_leads = db.get_uncontacted_partners_with_emails(limit=50, country_filter="kerala")
print(f"=== TOTAL UNCONTACTED KERALA LEADS: {len(kerala_leads)} ===")
for kl in kerala_leads[:8]:
    print(f"ID {kl['id']} | {kl['company_name']} | {kl['city']} | {kl['contact_email']}")

print("\n--- SAMPLE KERALA DRAFT ---")
sample_kerala = kerala_leads[0]
draft = ai_drafter.generate_application_draft(
    company_name=sample_kerala["company_name"],
    country="Kerala",
    job_title="Junior Project Manager / ERP Functional Consultant"
)
print("Subject:", draft["subject"])
print("Region:", draft.get("region"))
print("\nBody Preview:\n", draft["body"][:400], "...")
