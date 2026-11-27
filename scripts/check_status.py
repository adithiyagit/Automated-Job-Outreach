import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from core import db, autonomous_worker

apps = db.get_recent_applications(limit=10)
print("=== RECENT APPLICATIONS ===")
for a in apps[:8]:
    print(f"ID: {a['id']} | Sent At: {a['sent_at']} | Status: {a['status']} | Company: {a['company_name']} | Email: {a['recipient_email']}")

stats = db.get_stats_summary()
print("\n=== STATS SUMMARY ===")
print("Today Sent:", stats.get("today_sent"))
print("Daily Limit:", stats.get("daily_limit"))
print("Daily Remaining:", stats.get("daily_remaining"))
print("Total Partners:", stats.get("total_partners"))
print("Uncontacted Count:", stats.get("uncontacted_count"))
print("Partners With Email:", stats.get("partners_with_email"))
print("Invalid Emails Count:", stats.get("invalid_emails_count"))

daemon = autonomous_worker.get_daemon()
print("\n=== DAEMON STATUS ===")
print(json.dumps(daemon.get_status(), indent=2))

print("\n=== LAST 30 DAEMON LOGS ===")
for log in daemon.get_logs()[-30:]:
    print(log)
