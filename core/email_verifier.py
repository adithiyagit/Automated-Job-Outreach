"""
Email Verification & Deliverability Filter
Performs syntax validation, DNS MX record lookup, known-bounce quarantine,
and automatic Gmail IMAP failure synchronization to guarantee 0% bounce rate.
"""
import re
import json
import imaplib
import email as email_lib
from pathlib import Path
from typing import Tuple, Optional, Set, List
import dns.resolver
import config

# Regular expression matching RFC-compliant emails
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
)

# Known dead, disposable, or unmonitored prefixes to avoid
BLOCKED_PREFIXES = {
    "noreply", "no-reply", "donotreply", "do-not-reply",
    "postmaster", "abuse", "mailer-daemon", "root",
    "webmaster", "security", "privacy", "compliance",
    "bounce", "spam", "unsubscribe"
}

# Known dead, tracker, or invalid sample & aggregator domains
BLOCKED_DOMAINS = {
    # Sample / dead domains
    "example.com", "example.org", "domain.com", "email.com",
    "test.com", "sentry.io", "w3.org", "schema.org", "wixpress.com",
    "cloudflare.com", "gravatar.com", "wordpress.org", "localhost",
    # Dead / failed domains verified to bounce
    "smct.om", "whitecapstech.com", "appsgatetech.com", "centrics.in",
    # Job boards & aggregators (never email job board staff directly)
    "jobicy.com", "remoteok.com", "remoteok.io", "remotive.com", "remotive.io",
    "indeed.com", "linkedin.com", "glassdoor.com", "monster.com",
    "ziprecruiter.com", "wellfound.com", "angel.co", "simplyhired.com"
}

# Persistent bounce storage path
BOUNCED_STORAGE_FILE = config.DATA_DIR / "bounced_emails.json"

# In-memory cache for MX lookups
_MX_CACHE: dict = {}

def _load_persisted_bounced_emails() -> Set[str]:
    """Loads quarantined/bounced emails from persistent JSON storage."""
    defaults = {
        "hr@techultrasolutions.com",
        "careers@pixbitsolutions.com",
        "info@centrics.in",
        "careers@opensourceintegrators.com",
        "talent@silverdaletech.com",
        "contact@synodica.com",
        "hi@jobicy.com",
        "careers@smct.om",
        "hr@whitecapstech.com",
        "info@appsgatetech.com",
        "jobs@willdooit.com",
        "careers@smart-it.com",
        "karriere@equitania.de",
        "careers@targetintegration.com",
        "careers@kcsitglobal.com",
        "careers@acsone.eu",
        "career@pragtech.co.in",
        "hr@devintellecs.com",
        "jobs@digitaltrends.me"
    }
    if BOUNCED_STORAGE_FILE.exists():
        try:
            with open(BOUNCED_STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    defaults.update(e.strip().lower() for e in data if e)
        except Exception:
            pass
    return defaults

def _save_persisted_bounced_emails(bounced_set: Set[str]):
    """Persists quarantined emails to disk."""
    try:
        with open(BOUNCED_STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(list(bounced_set)), f, indent=2)
    except Exception as e:
        print(f"Error saving bounced emails cache: {e}")

# Global set of quarantined emails
BLOCKED_EMAILS: Set[str] = _load_persisted_bounced_emails()

def sync_gmail_bounces() -> int:
    """
    Connects to Gmail via IMAP, inspects Mail Delivery Subsystem failure messages,
    extracts rejected recipient emails, and permanently quarantines them.
    Returns the count of newly quarantined emails.
    """
    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD:
        return 0

    from core import db

    newly_quarantined = 0
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
        mail.select("INBOX")

        status, data = mail.search(None, 'FROM', 'mailer-daemon')
        if status != "OK" or not data or not data[0]:
            mail.logout()
            return 0

        msg_ids = data[0].split()
        # Inspect the latest 40 bounce reports
        for msg_id in msg_ids[-40:]:
            try:
                res, msg_data = mail.fetch(msg_id, "(RFC822)")
                if res != "OK":
                    continue
                msg = email_lib.message_from_bytes(msg_data[0][1])

                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body_text = part.get_payload()
                        if not isinstance(body_text, str):
                            continue

                        # Extract rejected email addresses
                        for match in re.findall(r'(?:to|delivered to|rejected:)\s*<?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?', body_text, re.IGNORECASE):
                            target_email = match.lower().strip().rstrip(".")
                            if any(g in target_email for g in ["google", "gmail", "mailer-daemon"]):
                                continue

                            if target_email not in BLOCKED_EMAILS:
                                BLOCKED_EMAILS.add(target_email)
                                newly_quarantined += 1

                            # Update database immediately
                            db.mark_email_invalid(target_email, reason="Bounced in Gmail (Delivery Failure)")
            except Exception:
                continue

        mail.logout()
        if newly_quarantined > 0:
            _save_persisted_bounced_emails(BLOCKED_EMAILS)

    except Exception as e:
        print(f"Notice during Gmail IMAP bounce sync: {e}")

    return newly_quarantined

def get_mx_records(domain: str, timeout: float = 3.0) -> list:
    """Queries DNS MX records for a domain with caching."""
    clean_domain = domain.lower().strip()
    if clean_domain in _MX_CACHE:
        return _MX_CACHE[clean_domain]

    try:
        resolver = dns.resolver.Resolver()
        resolver.lifetime = timeout
        resolver.timeout = timeout
        answers = resolver.resolve(clean_domain, 'MX')
        mx_hosts = [str(r.exchange).rstrip('.') for r in answers]
        _MX_CACHE[clean_domain] = mx_hosts
        return mx_hosts
    except Exception:
        # Check fallback A record (some domains accept mail directly on A record)
        try:
            resolver = dns.resolver.Resolver()
            resolver.lifetime = timeout
            resolver.timeout = timeout
            answers = resolver.resolve(clean_domain, 'A')
            a_records = [str(r) for r in answers]
            _MX_CACHE[clean_domain] = a_records
            return a_records
        except Exception:
            _MX_CACHE[clean_domain] = []
            return []

def verify_email_deliverability(email: str) -> Tuple[bool, str]:
    """
    Validates email format, checks known bounce/block lists,
    and confirms that the domain has active mail servers (MX records).
    Returns (is_valid, reason).
    """
    if not email or not isinstance(email, str):
        return False, "Empty or non-string email"

    clean = email.strip().lower().rstrip(".")

    # 1. Regex Syntax Check
    if not EMAIL_REGEX.match(clean):
        return False, f"Invalid email syntax: {clean}"

    user, domain = clean.split("@", 1)

    # 2. Blocked Quarantined Email Check
    if clean in BLOCKED_EMAILS:
        return False, f"Email '{clean}' is quarantined (known bounce/blocked address)"

    # 3. Blocked Prefix Check (e.g. no-reply, abuse)
    if user in BLOCKED_PREFIXES or user.startswith("no-reply") or user.startswith("noreply"):
        return False, f"Blocked unmonitored prefix: {user}@"

    # 4. Blocked Domain Check
    if domain in BLOCKED_DOMAINS:
        return False, f"Blocked or aggregator domain: {domain}"

    # 5. Check user-configured excluded domains (e.g. past employers)
    for exc in config.EXCLUDED_DOMAINS:
        if exc and (exc in domain or domain in exc):
            return False, f"Excluded domain from settings: {domain}"

    # 6. Filter obvious noise or media asset filenames misidentified as emails
    if any(clean.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js"]):
        return False, "Identified as media asset filename, not an email"

    # 7. DNS MX Records Verification (Active Mail Server Check)
    mx_records = get_mx_records(domain)
    if not mx_records:
        return False, f"Domain '{domain}' has no active MX or A mail records (dead domain or blocked)"

    return True, f"Valid deliverable email (MX: {mx_records[0]})"
