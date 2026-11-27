import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import db

conn = db.get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT country, count(*) 
    FROM partners 
    WHERE status NOT IN ('applied', 'invalid_email') 
      AND email_status != 'invalid_email'
      AND contact_email != ''
    GROUP BY country
""")
print("=== UNCONTACTED LEADS BY COUNTRY ===")
for r in cur.fetchall():
    print(f"{r['country']}: {r['count(*)']}")

conn.close()
