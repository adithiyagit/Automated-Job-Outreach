"""
Gmail SMTP Mailer and Guarded Autopilot Dispatcher
Sends personalized application emails with attached resume PDF,
enforcing anti-spam jitter delays, daily quotas, domain deduplication,
strict DNS MX record verification, and country timezone prioritization.
"""
import smtplib
import ssl
import time
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Callable
import config
from core import db, ai_drafter, email_verifier, timezone_scheduler

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT_SSL = 465
SMTP_PORT_TLS = 587

def validate_email_syntax(email: str) -> bool:
    is_valid, _ = email_verifier.verify_email_deliverability(email)
    return is_valid

def create_email_message(
    sender: str,
    recipient: str,
    subject: str,
    body_text: str,
    resume_path: Optional[Path] = None
) -> MIMEMultipart:
    """Builds a multipart MIME email with plain text body and optional PDF resume."""
    msg = MIMEMultipart()
    msg["From"] = f"{config.CANDIDATE_NAME} <{sender}>"
    msg["To"] = recipient
    msg["Subject"] = subject
    msg["Reply-To"] = sender

    # Body
    msg.attach(MIMEText(body_text, "plain", "utf-8"))

    # Attachment
    res_path = resume_path or config.RESUME_PATH
    if res_path and res_path.exists():
        with open(res_path, "rb") as f:
            part = MIMEBase("application", "pdf")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = f"Resume_{config.CANDIDATE_NAME.replace(' ', '_')}.pdf"
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)

    return msg

def test_smtp_connection() -> Tuple[bool, str]:
    """Tests Gmail credentials without sending an email."""
    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD:
        return False, "Gmail username or 16-character App Password missing in .env"

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT_SSL, context=context, timeout=10) as server:
            server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            return True, "Gmail SMTP authentication successful!"
    except Exception as e:
        return False, f"SMTP Connection failed: {str(e)}"

def send_test_email(to_email: Optional[str] = None) -> Tuple[bool, str]:
    """Sends a verification email to the user's own email to verify formatting & attachment."""
    recipient = to_email or config.GMAIL_USER
    if not recipient:
        return False, "No recipient email specified."

    if not config.GMAIL_APP_PASSWORD:
        return False, "Google App Password not configured in .env. Please set GMAIL_APP_PASSWORD."

    subject = f"Test Verification: Automation Engine Ready — {config.CANDIDATE_NAME}"
    body = (
        f"Hello {config.CANDIDATE_NAME},\n\n"
        f"This is a confirmation test email from your Job Application Automation Tool.\n"
        f"Your Gmail SMTP connection is working properly and your resume PDF is attached.\n\n"
        f"Daily Limit: {config.DAILY_EMAIL_LIMIT} applications/day\n"
        f"Jitter Delay: {config.MIN_DELAY_SECONDS} to {config.MAX_DELAY_SECONDS} seconds between emails\n\n"
        f"Best regards,\nYour Job Application Assistant"
    )

    msg = create_email_message(config.GMAIL_USER, recipient, subject, body, config.RESUME_PATH)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT_SSL, context=context, timeout=15) as server:
            server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            server.send_message(msg)
            return True, f"Test email successfully sent to {recipient}"
    except Exception as e:
        return False, f"Failed to send test email: {str(e)}"

def dispatch_single_email(
    recipient_email: str,
    subject: str,
    body: str,
    partner_id: Optional[int] = None,
    company_name: str = "",
    country: str = "Global",
    job_title: str = "Junior Project Manager / ERP Functional Consultant",
    match_score: int = 90
) -> Tuple[bool, str, int]:
    """
    Safely delivers a single application email via Gmail SMTP,
    checking safety quotas, DNS MX records, and recording in SQLite.
    Returns (success, message, application_id).
    """
    domain = db.extract_domain(recipient_email)

    # 1. Check blacklist
    for exc in config.EXCLUDED_DOMAINS:
        if exc and (exc in domain or domain in exc):
            app_id = db.record_application(
                recipient_email=recipient_email,
                company_name=company_name,
                subject=subject,
                body=body,
                domain=domain,
                partner_id=partner_id,
                country=country,
                job_title=job_title,
                match_score=match_score,
                status="skipped",
                error_message="Domain blacklisted"
            )
            return False, f"Skipped: Domain {domain} is blacklisted", app_id

    # 2. Strict DNS MX Record & Deliverability Verification
    is_valid, reason = email_verifier.verify_email_deliverability(recipient_email)
    if not is_valid:
        # Mark as invalid in DB so we never attempt this again
        db.mark_email_invalid(recipient_email, reason=reason)
        app_id = db.record_application(
            recipient_email=recipient_email,
            company_name=company_name,
            subject=subject,
            body=body,
            domain=domain,
            partner_id=partner_id,
            country=country,
            job_title=job_title,
            match_score=match_score,
            status="skipped",
            error_message=f"Undeliverable / Blocked email: {reason}"
        )
        return False, f"Blocked: {reason}", app_id

    # 3. Check if domain was already contacted
    if db.is_domain_contacted(domain):
        app_id = db.record_application(
            recipient_email=recipient_email,
            company_name=company_name,
            subject=subject,
            body=body,
            domain=domain,
            partner_id=partner_id,
            country=country,
            job_title=job_title,
            match_score=match_score,
            status="skipped",
            error_message="Domain already contacted"
        )
        return False, f"Skipped: {domain} already received an application", app_id

    # 4. Check daily limit
    today_sent = db.get_today_sent_count()
    if today_sent >= config.DAILY_EMAIL_LIMIT:
        app_id = db.record_application(
            recipient_email=recipient_email,
            company_name=company_name,
            subject=subject,
            body=body,
            domain=domain,
            partner_id=partner_id,
            country=country,
            job_title=job_title,
            match_score=match_score,
            status="queued",
            error_message="Daily sending cap reached"
        )
        return False, f"Daily limit reached ({today_sent}/{config.DAILY_EMAIL_LIMIT})", app_id

    # 5. Check credentials
    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD:
        app_id = db.record_application(
            recipient_email=recipient_email,
            company_name=company_name,
            subject=subject,
            body=body,
            domain=domain,
            partner_id=partner_id,
            country=country,
            job_title=job_title,
            match_score=match_score,
            status="failed",
            error_message="Missing GMAIL_APP_PASSWORD in .env"
        )
        return False, "Cannot send: Gmail App Password not set in .env", app_id

    # 6. Build and send email
    msg = create_email_message(config.GMAIL_USER, recipient_email, subject, body, config.RESUME_PATH)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT_SSL, context=context, timeout=15) as server:
            server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            server.send_message(msg)

        # Record success
        db.record_email_sent()
        db.mark_email_verified(recipient_email)
        app_id = db.record_application(
            recipient_email=recipient_email,
            company_name=company_name,
            subject=subject,
            body=body,
            domain=domain,
            partner_id=partner_id,
            country=country,
            job_title=job_title,
            match_score=match_score,
            status="sent"
        )
        return True, f"Application successfully sent to {company_name} ({recipient_email})", app_id

    except Exception as e:
        err = str(e)
        app_id = db.record_application(
            recipient_email=recipient_email,
            company_name=company_name,
            subject=subject,
            body=body,
            domain=domain,
            partner_id=partner_id,
            country=country,
            job_title=job_title,
            match_score=match_score,
            status="failed",
            error_message=err
        )
        return False, f"Send failed: {err}", app_id

def run_autopilot_cycle(
    batch_size: int = 5,
    dry_run: bool = False,
    morning_window_only: bool = False,
    country_filter: str = "",
    progress_callback: Optional[Callable[[str], None]] = None
) -> Dict[str, Any]:
    """
    Executes one autopilot cycle:
    1. Fetches uncontacted partners (optionally filtered by country e.g. 'India').
    2. Prioritizes by country local timezone (targeting 8:30-13:00 HR start hours).
    3. Verifies DNS MX records to prevent bounces.
    4. Drafts country-specific tailored applications.
    5. Sends email with resume attached.
    6. Injects randomized jitter delays between sends.
    """
    def log(msg: str):
        print(msg)
        if progress_callback:
            progress_callback(msg)

    stats = {"processed": 0, "sent": 0, "skipped": 0, "failed": 0, "limit_reached": False}

    raw_partners = db.get_uncontacted_partners_with_emails(
        limit=batch_size * 3,
        country_filter=country_filter
    )
    if not raw_partners:
        log("No uncontacted partners with emails found in queue.")
        return stats

    # Timezone prioritization with optional country preference
    partners = timezone_scheduler.prioritize_by_timezone(raw_partners, prefer_country=country_filter)

    if morning_window_only:
        partners = [
            p for p in partners
            if timezone_scheduler.get_country_schedule_info(p.get("country", "Global"))["is_morning_window"]
        ]
        if not partners:
            log("No target countries currently in their HR morning start window (8:30-11:30 AM). Holding dispatch.")
            return stats

    partners = partners[:batch_size]

    log(f"Starting autopilot cycle for {len(partners)} leads (Dry Run: {dry_run})...")

    for i, p in enumerate(partners):
        today_sent = db.get_today_sent_count()
        if today_sent >= config.DAILY_EMAIL_LIMIT:
            log(f"Daily cap of {config.DAILY_EMAIL_LIMIT} emails reached for today. Stopping.")
            stats["limit_reached"] = True
            break

        stats["processed"] += 1
        comp = p["company_name"]
        email = p["contact_email"]
        country = p.get("country", "Global")
        tier = p.get("partner_tier", "Partner")

        # Timezone schedule info
        tz_info = timezone_scheduler.get_country_schedule_info(country)
        log(f"[{i+1}/{len(partners)}] {comp} | {country} (Local Time: {tz_info['local_time_str']} - {tz_info['status_label']})")

        # Draft country-adapted pitch
        draft = ai_drafter.generate_application_draft(
            company_name=comp,
            country=country,
            job_title="Junior Project Manager / ERP Functional Consultant",
            partner_tier=tier
        )

        if dry_run:
            log(f"[DRY RUN] Would send to: {email} | Subject: {draft['subject']}")
            log(f"[DRY RUN] Template style: {draft.get('region', 'standard')}")
            stats["sent"] += 1
            continue

        success, msg, app_id = dispatch_single_email(
            recipient_email=email,
            subject=draft["subject"],
            body=draft["body"],
            partner_id=p["id"],
            company_name=comp,
            country=country,
            job_title="Junior Project Manager / ERP Functional Consultant",
            match_score=draft["match_score"]
        )

        log(f"-> {msg}")
        if success:
            stats["sent"] += 1
            if i < len(partners) - 1:
                jitter = random.randint(config.MIN_DELAY_SECONDS, config.MAX_DELAY_SECONDS)
                log(f"Sleeping for {jitter}s jitter delay to protect email sender reputation...")
                time.sleep(jitter)
        else:
            if "Skipped" in msg or "Blocked" in msg:
                stats["skipped"] += 1
            else:
                stats["failed"] += 1

    log(f"Cycle completed. Results: {stats}")
    return stats
