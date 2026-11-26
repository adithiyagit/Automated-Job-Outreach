"""
Command Line Interface (CLI) Runner for Global Job Application Automation
"""
import argparse
import sys
from pathlib import Path
import config
from core import db, mailer, ai_drafter
from scrapers import odoo_partners, job_boards

def cmd_stats(args):
    db.init_db()
    s = db.get_stats_summary()
    print("=" * 55)
    print("  🚀 GLOBAL ODOO JOB APPLICATION ENGINE — STATS")
    print("=" * 55)
    print(f"  Candidate:             {config.CANDIDATE_NAME}")
    print(f"  Email:                 {config.GMAIL_USER}")
    print(f"  Total Partners:        {s['total_partners']}")
    print(f"  Partners with Email:   {s['partners_with_email']}")
    print(f"  Emails Sent Today:     {s['today_sent']} / {s['daily_limit']}")
    print(f"  Total Sent All-Time:   {s['total_sent']}")
    print(f"  Total Queued:          {s['total_queued']}")
    print(f"  Daily Quota Left:      {s['daily_remaining']}")
    print("=" * 55)

def cmd_run(args):
    db.init_db()
    dry_run = args.dry_run
    batch = args.batch
    country = getattr(args, "country", "")
    print(f"[*] Starting Autopilot Cycle (Batch: {batch}, Country: {country or 'All'}, Dry Run: {dry_run})...")
    res = mailer.run_autopilot_cycle(batch_size=batch, dry_run=dry_run, country_filter=country)
    print(f"[+] Autopilot Cycle Finished. Results: {res}")

def cmd_test_email(args):
    recipient = args.to or config.GMAIL_USER
    print(f"[*] Dispatching verification test email to: {recipient}...")
    ok, msg = mailer.send_test_email(recipient)
    if ok:
        print(f"[+] SUCCESS: {msg}")
    else:
        print(f"[-] ERROR: {msg}")
        sys.exit(1)

def cmd_scrape(args):
    db.init_db()
    print("[*] Syncing seed Odoo partners...")
    res = odoo_partners.sync_seed_partners_to_db()
    print(f"[+] Seed sync complete: {res}")

    print("[*] Checking job boards...")
    jobs_added = job_boards.sync_job_openings_to_db(limit=10)
    print(f"[+] Job openings added: {jobs_added}")

def cmd_add_partner(args):
    db.init_db()
    pid = db.add_partner(
        company_name=args.name,
        website=args.website or "",
        contact_email=args.email,
        country=args.country or "Global",
        partner_tier=args.tier or "Ready",
        source="cli_entry"
    )
    if pid:
        print(f"[+] Successfully added partner '{args.name}' with ID {pid}.")
    else:
        print(f"[-] Could not add partner '{args.name}' (already exists or domain blacklisted).")

def cmd_daemon(args):
    db.init_db()
    from core import autonomous_worker
    daemon = autonomous_worker.get_daemon()

    if args.action == "status":
        st = daemon.get_status()
        print("=" * 55)
        print("  🤖 AUTONOMOUS APPLICATION DAEMON STATUS")
        print("=" * 55)
        print(f"  Running:           {st['is_running']}")
        print(f"  Enabled:           {st['is_enabled']}")
        print(f"  Interval:          Every {st['interval_minutes']} minutes")
        print(f"  Last Run:          {st['last_cycle_time'] or 'Not run yet'}")
        print(f"  Next Run:          {st['next_cycle_time'] or 'N/A'}")
        print("=" * 55)
        print("  Recent Activity Logs:")
        for log in daemon.get_logs()[-10:]:
            print(f"    {log}")
        print("=" * 55)

    elif args.action == "run-once":
        print("[*] Running single autonomous cycle...")
        daemon._execute_cycle()
        print("[+] Cycle finished.")

    elif args.action == "start":
        region = getattr(args, "region", "all")
        print(f"[*] Starting Autonomous Daemon (interval: {args.interval}m | Region: {region.upper()})... Press Ctrl+C to stop.")
        daemon.start(interval_minutes=args.interval, target_region=region)
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n[*] Stopping daemon...")
            daemon.stop()
            print("[+] Stopped.")

def main():
    parser = argparse.ArgumentParser(description="Global Job Application Automation CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # stats
    subparsers.add_parser("stats", help="Display summary metrics and daily limits")

    # daemon
    p_daemon = subparsers.add_parser("daemon", help="Manage 24/7 autonomous application daemon")
    p_daemon.add_argument("action", choices=["start", "status", "run-once"], help="Daemon action")
    p_daemon.add_argument("--interval", type=int, default=30, help="Scan interval in minutes")
    p_daemon.add_argument("--region", type=str, default="all", choices=["all", "india", "gulf", "europe_americas"], help="Target region focus")

    # run
    p_run = subparsers.add_parser("run", help="Execute an autopilot application batch")
    p_run.add_argument("--batch", type=int, default=5, help="Number of applications to process")
    p_run.add_argument("--dry-run", action="store_true", help="Simulate without sending real emails")
    p_run.add_argument("--country", type=str, default="", help="Filter by country (e.g. India, United Arab Emirates)")

    # test-email
    p_test = subparsers.add_parser("test-email", help="Send a verification test email to your inbox")
    p_test.add_argument("--to", type=str, default="", help="Recipient email address")

    # scrape
    subparsers.add_parser("scrape", help="Run Odoo partners and job board scrapers")

    # add-partner
    p_add = subparsers.add_parser("add-partner", help="Manually add a partner / company lead")
    p_add.add_argument("--name", type=str, required=True, help="Company Name")
    p_add.add_argument("--email", type=str, required=True, help="Contact/Careers Email")
    p_add.add_argument("--website", type=str, default="", help="Website URL")
    p_add.add_argument("--country", type=str, default="Global", help="Country")
    p_add.add_argument("--tier", type=str, default="Partner", help="Partner Tier")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "stats": cmd_stats,
        "daemon": cmd_daemon,
        "run": cmd_run,
        "test-email": cmd_test_email,
        "scrape": cmd_scrape,
        "add-partner": cmd_add_partner
    }
    commands[args.command](args)

if __name__ == "__main__":
    main()
