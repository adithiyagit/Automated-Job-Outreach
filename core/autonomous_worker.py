"""
Autonomous 24/7 Background Worker & Job Application Daemon
Continuously monitors for brand-new job openings across global job feeds,
MX-verifies recruiter emails, matches with Adithiya's resume, and automatically
applies according to each country's HR work starting window without any manual clicking.
"""
import threading
import time
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import config
from core import db, mailer, ai_drafter, timezone_scheduler, email_verifier
from scrapers import job_boards, odoo_partners

STATE_FILE = config.DATA_DIR / "daemon_state.json"
MAX_ACTIVITY_LOGS = 60

class AutonomousDaemon:
    def __init__(self):
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.RLock()
        self._cycle_running = False
        self._activity_logs: List[str] = []
        self._load_state()

    def _load_state(self):
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._is_enabled = data.get("is_enabled", False)
                    self._interval_minutes = data.get("interval_minutes", 15)
                    self._target_region = data.get("target_region", "all")
                    self._last_cycle_time = data.get("last_cycle_time", None)
                    self._next_cycle_time = data.get("next_cycle_time", None)
                    self._activity_logs = data.get("activity_logs", [])
                    return
            except Exception:
                pass
        self._is_enabled = False
        self._interval_minutes = 15
        self._target_region = "all"
        self._last_cycle_time = None
        self._next_cycle_time = None

    def _save_state(self):
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "is_enabled": self._is_enabled,
                    "interval_minutes": self._interval_minutes,
                    "target_region": getattr(self, "_target_region", "all"),
                    "last_cycle_time": self._last_cycle_time,
                    "next_cycle_time": self._next_cycle_time,
                    "activity_logs": self._activity_logs[-MAX_ACTIVITY_LOGS:]
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving daemon state: {e}")

    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(f"🤖 Autonomous Daemon: {log_entry}")
        with self._lock:
            self._activity_logs.append(log_entry)
            if len(self._activity_logs) > MAX_ACTIVITY_LOGS:
                self._activity_logs = self._activity_logs[-MAX_ACTIVITY_LOGS:]
            self._save_state()

    def get_logs(self) -> List[str]:
        with self._lock:
            return list(self._activity_logs)

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "is_running": self.is_running(),
                "is_enabled": self._is_enabled,
                "interval_minutes": self._interval_minutes,
                "target_region": getattr(self, "_target_region", "all"),
                "last_cycle_time": self._last_cycle_time,
                "next_cycle_time": self._next_cycle_time,
                "log_count": len(self._activity_logs)
            }

    def ensure_running(self):
        """Ensures the background worker is running 24/7 without requiring manual button clicks."""
        with self._lock:
            if not self.is_running():
                self._is_enabled = True
                interval = getattr(self, "_interval_minutes", 15)
                region = getattr(self, "_target_region", "all")
                self.start(interval_minutes=interval, target_region=region)

    def start(self, interval_minutes: int = 15, target_region: str = "all"):
        with self._lock:
            if self.is_running():
                return
            self._is_enabled = True
            self._interval_minutes = interval_minutes
            self._target_region = target_region
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True, name="AutoApplyDaemon")
            self._thread.start()
            self._save_state()
        self.log(f"🟢 Autonomous Daemon STARTED (Scanning interval: every {interval_minutes} mins | Region: {target_region.upper()})")

    def stop(self):
        with self._lock:
            if not self.is_running():
                self._is_enabled = False
                self._save_state()
                return
            self._is_enabled = False
            self._stop_event.set()
            self._save_state()
        self.log("🔴 Autonomous Daemon STOPPED by user")

    def _run_loop(self):
        """Continuous background execution loop."""
        time.sleep(2) # Initial warmup

        while not self._stop_event.is_set():
            try:
                self._execute_cycle()
            except Exception as e:
                self.log(f"⚠️ Exception during autonomous cycle: {str(e)}")

            # Calculate next run time
            sleep_duration = self._interval_minutes * 60
            next_ts = time.time() + sleep_duration
            self._next_cycle_time = datetime.fromtimestamp(next_ts).strftime("%I:%M %p")
            self._save_state()

            self.log(f"Cycle finished. Sleeping until {self._next_cycle_time} ({self._interval_minutes}m)...")

            # Sleep in 1-second chunks to respond quickly to stop requests
            for _ in range(sleep_duration):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def _execute_cycle(self):
        """Runs one full autonomous discovery, validation, and dispatch sequence."""
        if getattr(self, "_cycle_running", False):
            self.log("⚠️ Autonomous cycle already active in another thread. Skipping duplicate execution.")
            return

        self._cycle_running = True
        try:
            self._last_cycle_time = datetime.now().strftime("%I:%M %p")
            self.log("🚀 Starting autonomous cycle: Checking fresh job postings & partner directories...")

            # Step 0: Automatic Gmail IMAP Failure / Bounce Quarantine
            try:
                bounces_count = email_verifier.sync_gmail_bounces()
                if bounces_count > 0:
                    self.log(f"🛡️ Bounce Guard: Quarantined {bounces_count} newly detected bounced/blocked emails from Gmail notifications.")
            except Exception as e:
                self.log(f"Notice during Gmail bounce sync: {e}")

            # Step 1: Scout Fresh Job Openings Across Live Aggregators
            try:
                crawl_stats = job_boards.sync_all_fresh_jobs(max_enrich=6)
                self.log(f"Scout Result: Found {crawl_stats['found_openings']} live openings, queued {crawl_stats['added_to_queue']} with verified MX.")
            except Exception as e:
                self.log(f"Notice during live job crawl: {e}")

            # Step 2: Clean Deliverability & MX Records
            try:
                purge_stats = odoo_partners.clean_database_deliverability()
                if purge_stats["purged_invalid"] > 0:
                    self.log(f"Deliverability Filter: Quarantined {purge_stats['purged_invalid']} dead/blocked addresses.")
            except Exception as e:
                self.log(f"Notice during MX cleanup: {e}")

            # Step 2.5: Auto-Replenish Lead Queue if Low
            try:
                cur_uncontacted = db.get_stats_summary().get("uncontacted_count", 0)
                if cur_uncontacted < 15:
                    self.log(f"🔄 Lead Queue Auto-Replenishment: Only {cur_uncontacted} uncontacted leads remaining. Injecting fresh verified partners...")
                    rep_stats = odoo_partners.replenish_leads_if_low(min_threshold=15)
                    if rep_stats.get("added", 0) > 0:
                        self.log(f"✅ Lead Replenishment: Injected {rep_stats['added']} fresh verified corporate leads into active queue.")
            except Exception as e:
                self.log(f"Notice during lead replenishment: {e}")

            # Step 3: Check Daily Quota
            today_sent = db.get_today_sent_count()
            if today_sent >= config.DAILY_EMAIL_LIMIT:
                self.log(f"Daily cap of {config.DAILY_EMAIL_LIMIT} reached for today ({today_sent} sent). Pausing dispatch until tomorrow.")
                return

            remaining_quota = config.DAILY_EMAIL_LIMIT - today_sent

            # Step 4: Multi-Country Application Dispatch
            reg = getattr(self, "_target_region", "all")
            country_filter = reg if reg not in ("all", "global") else ""
            leads = db.get_uncontacted_partners_with_emails(limit=100, country_filter=country_filter)
            if not leads:
                self.log(f"Queue clear: All contacts for region '{reg}' have been applied to or verified.")
                return

            # Sort leads: round-robin interleaved across countries for global mode, or prioritized for specific region
            sorted_leads = timezone_scheduler.prioritize_by_timezone(leads, prefer_country=country_filter)

            dispatched_in_this_cycle = 0
            max_per_cycle = min(4, remaining_quota)

            for lead in sorted_leads:
                if self._stop_event.is_set():
                    break

                if dispatched_in_this_cycle >= max_per_cycle:
                    self.log(f"Reached cycle batch limit ({dispatched_in_this_cycle} applications). Yielding to next interval.")
                    break

                country = lead.get("country", "Global")
                comp = lead["company_name"]
                email = lead["contact_email"]
                tz_info = timezone_scheduler.get_country_schedule_info(country)

                # Country schedule & window resolution
                window_tag = (
                    "🟢 Morning Prime" if tz_info["is_morning_window"]
                    else ("🟡 Business Hours" if tz_info["is_business_hours"]
                          else ("⏸️ Weekend Delivery (Queued for Monday Review)" if tz_info["is_weekend"] else "🌙 Recruiter Morning Queued"))
                )

                # Strict Pre-Send Deliverability & Blocklist Verification
                is_deliverable, reason = email_verifier.verify_email_deliverability(email)
                if not is_deliverable:
                    self.log(f"🛡️ Bounce Guard: Blocked {comp} ({email}) — {reason}")
                    db.mark_email_invalid(email, reason=reason)
                    continue

                self.log(f"🎯 Target Ready: {comp} | {country} (Local Time: {tz_info['local_time_str']} - {window_tag})")
                
                # Generate country-adapted cover letter
                draft = ai_drafter.generate_application_draft(
                    company_name=comp,
                    country=country,
                    job_title="Junior Project Manager / ERP Functional Consultant",
                    partner_tier=lead.get("partner_tier", "Partner")
                )

                # Dispatch via Gmail SMTP
                success, msg, app_id = mailer.dispatch_single_email(
                    recipient_email=email,
                    subject=draft["subject"],
                    body=draft["body"],
                    partner_id=lead["id"],
                    company_name=comp,
                    country=country,
                    job_title="Junior Project Manager / ERP Functional Consultant",
                    match_score=draft["match_score"]
                )

                if success:
                    dispatched_in_this_cycle += 1
                    self.log(f"✅ Successfully auto-applied to {comp} ({email})! Subject: {draft['subject']}")
                    
                    # Apply anti-spam jitter delay before the next email
                    if dispatched_in_this_cycle < max_per_cycle:
                        jitter = random.randint(config.MIN_DELAY_SECONDS, config.MAX_DELAY_SECONDS)
                        self.log(f"Sleeping {jitter}s jitter delay to preserve Gmail sender reputation...")
                        for _ in range(jitter):
                            if self._stop_event.is_set():
                                break
                            time.sleep(1)
                else:
                    self.log(f"Skipped/Failed {comp}: {msg}")

            self.log(f"Cycle execution finished. Auto-applied to {dispatched_in_this_cycle} companies this cycle.")
        finally:
            self._cycle_running = False

# Global singleton daemon instance
daemon_instance = AutonomousDaemon()

def get_daemon() -> AutonomousDaemon:
    daemon_instance.ensure_running()
    return daemon_instance
