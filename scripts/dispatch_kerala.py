import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import autonomous_worker, db

print("--- STARTING KERALA DISPATCH CYCLE ---")
daemon = autonomous_worker.get_daemon()
daemon._cycle_running = False
orig_reg = getattr(daemon, "_target_region", "all")
daemon._target_region = "kerala"

try:
    daemon._execute_cycle()
finally:
    daemon._target_region = "all"  # Return to global round-robin

print("\n--- ACTIVITY LOGS ---")
for l in daemon.get_logs()[-15:]:
    print(l)

print("\n--- TODAY'S RECENT APPLICATIONS ---")
apps = db.get_recent_applications(limit=6)
for a in apps:
    print(f"ID {a['id']} | {a['sent_at']} | {a['company_name']} | {a['country']} | Status: {a['status']} | To: {a['recipient_email']}")
