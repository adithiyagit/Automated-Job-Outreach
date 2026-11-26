"""
Database Manager for Global Job Application Automation
Handles SQLite storage, migrations, deduplication, daily quota tracking,
and deliverability verification status.
"""
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional, Any
from urllib.parse import urlparse
import config

def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    path = db_path or config.DATABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30.0)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=30000;")
    except Exception:
        pass
    conn.row_factory = sqlite3.Row
    return conn

def extract_domain(url_or_email: str) -> str:
    """Extract clean domain name from URL or email address."""
    if not url_or_email:
        return ""
    if "@" in url_or_email:
        return url_or_email.split("@")[-1].lower().strip()
    try:
        netloc = urlparse(url_or_email).netloc
        if not netloc and not url_or_email.startswith(("http://", "https://")):
            netloc = urlparse("http://" + url_or_email).netloc
        domain = netloc.lower().replace("www.", "").strip()
        return domain
    except Exception:
        return url_or_email.lower().strip()

def init_db(db_path: Optional[Path] = None) -> None:
    """Initializes tables and indexes."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        country TEXT DEFAULT 'Global',
        city TEXT DEFAULT '',
        website TEXT,
        domain TEXT,
        contact_email TEXT,
        email_status TEXT DEFAULT 'unverified', -- unverified, verified, invalid_email
        partner_tier TEXT DEFAULT 'Ready',
        source TEXT DEFAULT 'odoo_directory',
        status TEXT DEFAULT 'discovered', -- discovered, email_found, applied, skipped, invalid_email
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(domain)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner_id INTEGER,
        recipient_email TEXT NOT NULL,
        recipient_name TEXT DEFAULT '',
        company_name TEXT NOT NULL,
        domain TEXT,
        country TEXT DEFAULT 'Global',
        job_title TEXT DEFAULT 'Junior Project Manager / ERP Functional Consultant',
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        match_score INTEGER DEFAULT 85,
        status TEXT DEFAULT 'queued', -- queued, sent, failed, skipped
        error_message TEXT,
        sent_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(partner_id) REFERENCES partners(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_stats (
        send_date DATE PRIMARY KEY,
        sent_count INTEGER DEFAULT 0,
        limit_count INTEGER DEFAULT 50
    );
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_partners_domain ON partners(domain);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_partners_status ON partners(status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_apps_domain ON applications(domain);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_apps_status ON applications(status);")

    # Lightweight migrations for existing databases
    try:
        cur.execute("ALTER TABLE partners ADD COLUMN email_status TEXT DEFAULT 'unverified';")
    except sqlite3.OperationalError:
        pass # Already exists

    try:
        cur.execute("CREATE INDEX IF NOT EXISTS idx_partners_email_status ON partners(email_status);")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("UPDATE daily_stats SET limit_count = ?", (config.DAILY_EMAIL_LIMIT,))
    except Exception:
        pass

    try:
        cur.execute("""
            UPDATE partners 
            SET status = 'applied'
            WHERE id IN (
                SELECT DISTINCT partner_id FROM applications WHERE status = 'sent' AND partner_id IS NOT NULL
            )
        """)
        cur.execute("""
            UPDATE partners 
            SET status = 'applied'
            WHERE domain IN (
                SELECT DISTINCT domain FROM applications WHERE status = 'sent' AND domain IS NOT NULL AND domain != ''
            )
        """)
    except Exception:
        pass

    conn.commit()
    conn.close()

    # Synchronize and quarantine any historical bounces in applications table
    try:
        sync_all_bounced_applications(db_path)
    except Exception:
        pass

def add_partner(
    company_name: str,
    website: str = "",
    contact_email: str = "",
    country: str = "Global",
    city: str = "",
    partner_tier: str = "Ready",
    source: str = "odoo_directory",
    db_path: Optional[Path] = None
) -> Optional[int]:
    """Adds a partner if domain not already stored or blacklisted. Returns partner_id or None."""
    domain = extract_domain(website or contact_email)
    if not domain:
        domain = company_name.lower().replace(" ", "") + ".com"

    # Check blacklist
    for excluded in config.EXCLUDED_DOMAINS:
        if excluded and (excluded in domain or domain in excluded):
            return None

    conn = get_connection(db_path)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO partners (company_name, country, city, website, domain, contact_email, partner_tier, source, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company_name.strip(),
            country.strip(),
            city.strip(),
            website.strip(),
            domain,
            contact_email.strip().lower() if contact_email else "",
            partner_tier.strip(),
            source,
            "email_found" if contact_email else "discovered"
        ))
        conn.commit()
        partner_id = cur.lastrowid
        return partner_id
    except sqlite3.IntegrityError:
        # Already exists, update contact email if we now have one
        if contact_email:
            cur.execute("""
                UPDATE partners SET contact_email = ?, status = 'email_found'
                WHERE domain = ? AND (contact_email IS NULL OR contact_email = '')
            """, (contact_email.strip().lower(), domain))
            conn.commit()
        return None
    finally:
        conn.close()

def mark_email_invalid(email_or_domain: str, reason: str = "", db_path: Optional[Path] = None):
    """
    Marks a dead or bounced email/domain as invalid in DB so it is never contacted again,
    and updates any existing sent applications for this recipient to 'bounced'.
    """
    domain = extract_domain(email_or_domain)
    clean_email = email_or_domain.lower().strip() if "@" in email_or_domain else ""

    conn = get_connection(db_path)
    cur = conn.cursor()
    if clean_email:
        cur.execute("""
            UPDATE partners SET email_status = 'invalid_email', status = 'invalid_email', notes = ?
            WHERE contact_email = ?
        """, (reason, clean_email))
        cur.execute("""
            UPDATE applications SET status = 'bounced', error_message = ?
            WHERE recipient_email = ? AND status = 'sent'
        """, (reason, clean_email))
    if domain:
        cur.execute("""
            UPDATE partners SET email_status = 'invalid_email', status = 'invalid_email', notes = ?
            WHERE domain = ?
        """, (reason, domain))
        cur.execute("""
            UPDATE applications SET status = 'bounced', error_message = ?
            WHERE domain = ? AND status = 'sent'
        """, (reason, domain))
    conn.commit()
    conn.close()

def sync_all_bounced_applications(db_path: Optional[Path] = None) -> int:
    """
    Scans applications table and ensures that any recipient email that is in
    the quarantined/bounced list or fails deliverability is updated to status='bounced'.
    """
    from core import email_verifier
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, recipient_email, domain FROM applications WHERE status = 'sent'")
    rows = cur.fetchall()
    updated = 0
    for r in rows:
        email = r["recipient_email"]
        is_val, reason = email_verifier.verify_email_deliverability(email)
        if not is_val:
            cur.execute("UPDATE applications SET status = 'bounced', error_message = ? WHERE id = ?", (reason, r["id"]))
            cur.execute("UPDATE partners SET email_status = 'invalid_email', status = 'invalid_email', notes = ? WHERE contact_email = ?", (reason, email))
            updated += 1
    conn.commit()
    conn.close()
    return updated

def mark_email_verified(email: str, db_path: Optional[Path] = None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        UPDATE partners SET email_status = 'verified' WHERE contact_email = ?
    """, (email.strip().lower(),))
    conn.commit()
    conn.close()

def is_domain_contacted(domain: str, db_path: Optional[Path] = None) -> bool:
    """Checks if any application has already been sent to this domain."""
    if not domain:
        return False
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM applications WHERE domain = ? AND status = 'sent'
    """, (domain.lower().strip(),))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0

def get_today_sent_count(db_path: Optional[Path] = None) -> int:
    """Calculates legitimate, non-bounced applications delivered today."""
    today = date.today().isoformat()
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM applications 
        WHERE status = 'sent' 
          AND (sent_at LIKE ? OR date(sent_at) = date(?))
    """, (f"{today}%", today))
    row = cur.fetchone()
    app_count = row[0] if row else 0

    cur.execute("SELECT sent_count FROM daily_stats WHERE send_date = ?", (today,))
    stat_row = cur.fetchone()
    daily_count = stat_row[0] if stat_row else 0
    conn.close()

    # If applications table has sent records, app_count is the strict deliverability ground truth
    return app_count if app_count > 0 else daily_count

def record_email_sent(db_path: Optional[Path] = None) -> int:
    """Increments today's sent count."""
    today = date.today().isoformat()
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO daily_stats (send_date, sent_count, limit_count)
        VALUES (?, 1, ?)
        ON CONFLICT(send_date) DO UPDATE SET sent_count = sent_count + 1
    """, (today, config.DAILY_EMAIL_LIMIT))
    conn.commit()
    cur.execute("SELECT sent_count FROM daily_stats WHERE send_date = ?", (today,))
    count = cur.fetchone()[0]
    conn.close()
    return count

def record_application(
    recipient_email: str,
    company_name: str,
    subject: str,
    body: str,
    domain: str = "",
    partner_id: Optional[int] = None,
    country: str = "Global",
    job_title: str = "Junior Project Manager / ERP Functional Consultant",
    match_score: int = 85,
    status: str = "queued",
    error_message: str = "",
    db_path: Optional[Path] = None
) -> int:
    """Records an application draft or sent entry in SQLite."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    sent_at = datetime.now().isoformat() if status == "sent" else None
    clean_domain = domain or extract_domain(recipient_email)

    cur.execute("""
        INSERT INTO applications (
            partner_id, recipient_email, company_name, domain, country,
            job_title, subject, body, match_score, status, error_message, sent_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        partner_id, recipient_email.strip().lower(), company_name.strip(),
        clean_domain, country, job_title, subject, body,
        match_score, status, error_message, sent_at
    ))
    app_id = cur.lastrowid

    if partner_id:
        cur.execute("UPDATE partners SET status = ? WHERE id = ?", ("applied" if status == "sent" else "email_found", partner_id))

    conn.commit()
    conn.close()
    return app_id

def get_uncontacted_partners_with_emails(
    limit: int = 50,
    country_filter: str = "",
    db_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """
    Returns valid partners who have an email, are not applied or invalid,
    and whose domain hasn't received an application.
    Supports optional country filtering (e.g. 'India', 'United Arab Emirates').
    """
    conn = get_connection(db_path)
    cur = conn.cursor()
    query = """
        SELECT p.* FROM partners p
        WHERE p.contact_email IS NOT NULL 
          AND p.contact_email != ''
          AND p.status NOT IN ('applied', 'invalid_email')
          AND p.email_status != 'invalid_email'
          AND NOT EXISTS (
              SELECT 1 FROM applications a 
              WHERE a.domain = p.domain AND a.status = 'sent'
          )
    """
    params = []
    if country_filter and country_filter.lower() not in ("all", "global"):
        clean_cf = country_filter.lower().strip()
        if clean_cf in ("middle_east", "gulf"):
            query += " AND (p.country LIKE '%Emirates%' OR p.country LIKE '%Saudi%' OR p.country LIKE '%Qatar%' OR p.country LIKE '%Oman%' OR p.country LIKE '%Kuwait%' OR p.country LIKE '%Bahrain%') "
        elif clean_cf in ("europe", "dach", "western_europe"):
            query += " AND (p.country LIKE '%Switzerland%' OR p.country LIKE '%Germany%' OR p.country LIKE '%Belgium%' OR p.country LIKE '%Netherlands%' OR p.country LIKE '%France%' OR p.country LIKE '%United Kingdom%' OR p.country LIKE '%Spain%' OR p.country LIKE '%Italy%' OR p.country LIKE '%Austria%') "
        elif clean_cf in ("north_america", "us", "usa"):
            query += " AND (p.country LIKE '%United States%' OR p.country LIKE '%Canada%') "
        elif clean_cf in ("apac", "asia"):
            query += " AND (p.country LIKE '%Singapore%' OR p.country LIKE '%Australia%' OR p.country LIKE '%Malaysia%') "
        else:
            query += " AND p.country LIKE ? "
            params.append(f"%{country_filter}%")

    query += " ORDER BY p.id ASC LIMIT ? "
    params.append(limit)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats_summary(db_path: Optional[Path] = None) -> Dict[str, Any]:
    """Returns comprehensive dashboard metrics, pipeline funnel, and country breakdown."""
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM partners WHERE status != 'invalid_email'")
    total_partners = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM partners WHERE contact_email != '' AND status != 'invalid_email'")
    partners_with_email = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM partners WHERE email_status = 'invalid_email' OR status = 'invalid_email'")
    invalid_emails_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'sent'")
    total_sent = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'queued'")
    total_queued = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'failed'")
    total_failed = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'bounced'")
    total_bounced = cur.fetchone()[0]

    # Country breakdown of sent applications
    cur.execute("""
        SELECT country, COUNT(*) as cnt FROM applications 
        WHERE status = 'sent' 
        GROUP BY country 
        ORDER BY cnt DESC
    """)
    country_counts = {row["country"]: row["cnt"] for row in cur.fetchall()}

    # Uncontacted leads currently waiting in queue
    cur.execute("""
        SELECT COUNT(*) FROM partners p
        WHERE p.contact_email IS NOT NULL AND p.contact_email != ''
          AND p.status NOT IN ('applied', 'invalid_email')
          AND p.email_status != 'invalid_email'
          AND NOT EXISTS (
              SELECT 1 FROM applications a 
              WHERE a.domain = p.domain AND a.status = 'sent'
          )
    """)
    uncontacted_count = cur.fetchone()[0]

    conn.close()

    today_sent = get_today_sent_count(db_path)
    daily_remaining = max(0, config.DAILY_EMAIL_LIMIT - today_sent)

    return {
        "total_partners": total_partners,
        "partners_with_email": partners_with_email,
        "invalid_emails_count": invalid_emails_count,
        "total_sent": total_sent,
        "total_bounced": total_bounced,
        "total_queued": total_queued,
        "total_failed": total_failed,
        "uncontacted_count": uncontacted_count,
        "today_sent": today_sent,
        "daily_limit": config.DAILY_EMAIL_LIMIT,
        "daily_remaining": daily_remaining,
        "country_breakdown": country_counts
    }

def get_all_partners_filtered(
    search: str = "",
    country: str = "All",
    status_filter: str = "All",
    limit: int = 300,
    db_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """Retrieves partners with search term, country, and status filtering for CRM table."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    query = "SELECT * FROM partners WHERE 1=1"
    params = []

    if search:
        query += " AND (company_name LIKE ? OR contact_email LIKE ? OR domain LIKE ?) "
        term = f"%{search.strip()}%"
        params.extend([term, term, term])

    if country and country != "All":
        query += " AND country LIKE ? "
        params.append(f"%{country.strip()}%")

    if status_filter and status_filter != "All":
        query += " AND status = ? "
        params.append(status_filter.strip())

    query += " ORDER BY id DESC LIMIT ? "
    params.append(limit)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_applications(limit: int = 100, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM applications ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
