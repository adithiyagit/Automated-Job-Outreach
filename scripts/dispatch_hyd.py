import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import autonomous_worker, db

print("--- DISPATCHING TO HYDERABAD ---")
daemon = autonomous_worker.get_daemon()
daemon._cycle_running = False
orig_reg = getattr(daemon, "_target_region", "all")

# Set target region to Hyderabad
daemon._target_region = "hyderabad"
try:
    daemon._execute_cycle()
finally:
    daemon._target_region = orig_reg

print("\n--- RECENT SENT APPLICATIONS ---")
apps = db.get_recent_applications(limit=6)
for a in apps:
    print(f"ID {a['id']} | {a['sent_at']} | {a['company_name']} | Status: {a['status']} | To: {a['recipient_email']}")
