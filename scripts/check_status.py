import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db

conn = db.get_connection()
cur = conn.cursor()

print("--- PARTNERS GROUPED BY STATUS ---")
cur.execute("SELECT status, count(*) FROM partners GROUP BY status")
for row in cur.fetchall():
    print(dict(row))

print("\n--- PARTNERS GROUPED BY EMAIL_STATUS ---")
cur.execute("SELECT email_status, count(*) FROM partners GROUP BY email_status")
for row in cur.fetchall():
    print(dict(row))

print("\n--- UNCONTACTED PARTNERS WITH EMAIL ---")
cur.execute("""
    SELECT id, company_name, country, contact_email, status, email_status 
    FROM partners 
    WHERE status NOT IN ('applied', 'invalid_email', 'bounced')
      AND contact_email IS NOT NULL 
      AND contact_email != ''
""")
uncontacted = cur.fetchall()
print(f"Total found: {len(uncontacted)}")
for u in uncontacted[:10]:
    print(dict(u))

print("\n--- TODAY'S APPLICATIONS ---")
cur.execute("SELECT id, sent_at, status, company_name, recipient_email FROM applications WHERE date(sent_at) = date('now') ORDER BY sent_at DESC")
today_apps = cur.fetchall()
print(f"Total sent today: {len(today_apps)}")
for a in today_apps:
    print(dict(a))

conn.close()
