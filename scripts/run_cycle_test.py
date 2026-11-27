import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core import autonomous_worker, db

print("--- TRIGGERING AUTONOMOUS OUTREACH CYCLE ---")
daemon = autonomous_worker.get_daemon()
daemon._cycle_running = False  # Reset flag if needed
daemon._execute_cycle()

print("\n--- NEW ACTIVITY LOGS ---")
for l in daemon.get_logs()[-15:]:
    print(l)

print("\n--- STATS AFTER CYCLE ---")
stats = db.get_stats_summary()
print("Today Sent:", stats.get("today_sent"))
print("Daily Remaining:", stats.get("daily_remaining"))
print("Uncontacted Remaining:", stats.get("uncontacted_count"))
