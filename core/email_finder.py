"""
Email Discovery & Extraction Module
Crawls company websites and career pages to find public HR/careers/contact emails.
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Set, List, Optional
from urllib.parse import urljoin, urlparse

# Email regex pattern
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

# Common contact & career sub-paths
TARGET_PATHS = [
    "",
    "/contact",
    "/contact-us",
    "/about",
    "/about-us",
    "/careers",
    "/jobs",
    "/work-with-us",
    "/join-us",
    "/team",
    "/en/contact",
    "/en/careers"
]

# Blacklisted email domains & patterns (noise / invalid / trackers)
IGNORE_DOMAINS = {
    "sentry.io", "example.com", "w3.org", "domain.com", "email.com",
    "google.com", "wixpress.com", "schema.org", "cloudflare.com",
    "gravatar.com", "wordpress.org"
}

IGNORE_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".css", ".js"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def clean_email(email_str: str) -> Optional[str]:
    """Validates and cleans an extracted email string."""
    email = email_str.lower().strip()
    # Check if ends with file extension
    if any(email.endswith(ext) for ext in IGNORE_EXTENSIONS):
        return None
    # Check domain
    parts = email.split("@")
    if len(parts) != 2:
        return None
    user, domain = parts
    if domain in IGNORE_DOMAINS or len(user) < 2 or len(domain) < 4:
        return None
    if "." not in domain:
        return None
    # Filter out numeric or UUID garbage
    if re.match(r'^[0-9a-f]{20,}', user):
        return None
    return email

def score_email_priority(email: str) -> int:
    """Scores an email address: careers/jobs/hr get higher priority over info/contact."""
    e = email.lower()
    if any(k in e for k in ["career", "careers", "job", "jobs", "hiring", "recruitment", "talent", "hr"]):
        return 100
    if any(k in e for k in ["apply", "resume", "cv", "join"]):
        return 90
    if any(k in e for k in ["people", "consulting", "team"]):
        return 80
    if any(k in e for k in ["info", "contact", "hello", "sales", "office"]):
        return 50
    return 30

def extract_emails_from_html(html_content: str) -> List[str]:
    """Finds all emails in HTML text and mailto: links."""
    soup = BeautifulSoup(html_content, "html.parser")
    found: Set[str] = set()

    # Search mailto: links
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("mailto:"):
            raw_email = href.replace("mailto:", "").split("?")[0]
            cleaned = clean_email(raw_email)
            if cleaned:
                found.add(cleaned)

    # Search raw text
    text_matches = EMAIL_REGEX.findall(html_content)
    for m in text_matches:
        cleaned = clean_email(m)
        if cleaned:
            found.add(cleaned)

    # Sort by priority
    return sorted(list(found), key=score_email_priority, reverse=True)

def find_emails_for_website(base_url: str, timeout: int = 6) -> List[str]:
    """Crawls base website and primary contact/career sub-paths for emails."""
    if not base_url:
        return []
    if not base_url.startswith(("http://", "https://")):
        base_url = "https://" + base_url

    parsed = urlparse(base_url)
    domain_root = f"{parsed.scheme}://{parsed.netloc}"

    found_emails: Set[str] = set()

    for path in TARGET_PATHS:
        target_url = urljoin(domain_root, path)
        try:
            resp = requests.get(target_url, headers=HEADERS, timeout=timeout, allow_redirects=True)
            if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
                emails = extract_emails_from_html(resp.text)
                for e in emails:
                    found_emails.add(e)
                    # If high-priority recruitment email found, we can stop early
                    if score_email_priority(e) >= 90:
                        break
        except Exception:
            continue

        if len(found_emails) >= 3:
            break

    return sorted(list(found_emails), key=score_email_priority, reverse=True)
