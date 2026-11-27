"""
Indeed & Multi-Country Job Aggregator Engine
Provides:
1. Country-specific Indeed search URL generator (India, UAE, Saudi, Germany, Switzerland, UK, US, etc.).
2. Cross-platform live job scout (combining LinkedIn public guest jobs, European Arbeitnow API, and remote aggregators).
3. 1-Click Pipeline Enrichment: Automatically resolves company domain, finds recruiter/HR emails,
   runs DNS MX verification, and inserts deliverable leads into SQLite for zero-click autonomous outreach.
"""
import urllib.parse
import requests
from typing import List, Dict, Any, Tuple, Optional
import config
from core import db, email_finder, email_verifier, linkedin_engine

# Mapping of countries to localized Indeed domains
INDEED_DOMAINS = {
    "india": "https://in.indeed.com",
    "united arab emirates": "https://ae.indeed.com",
    "uae": "https://ae.indeed.com",
    "saudi arabia": "https://sa.indeed.com",
    "ksa": "https://sa.indeed.com",
    "germany": "https://de.indeed.com",
    "switzerland": "https://ch.indeed.com",
    "united kingdom": "https://uk.indeed.com",
    "uk": "https://uk.indeed.com",
    "canada": "https://ca.indeed.com",
    "australia": "https://au.indeed.com",
    "singapore": "https://sg.indeed.com",
    "united states": "https://www.indeed.com",
    "usa": "https://www.indeed.com",
    "us": "https://www.indeed.com",
    "global": "https://www.indeed.com"
}

def get_indeed_search_url(keywords: str = "Odoo", country: str = "India", location: str = "") -> str:
    """
    Constructs a localized, fresh (last 14 days) Indeed search URL.
    """
    c_key = (country or "india").strip().lower()
    base = INDEED_DOMAINS.get(c_key, "https://www.indeed.com")
    
    q_params = [keywords.strip()]
    url = f"{base}/jobs?q={urllib.parse.quote_plus(' '.join(q_params))}"
    if location and location.strip():
        url += f"&l={urllib.parse.quote_plus(location.strip())}"
    url += "&fromage=14"  # Last 14 days for fresh postings
    return url

def fetch_arbeitnow_jobs(keywords: str = "Odoo", limit: int = 15) -> List[Dict[str, Any]]:
    """
    Crawls Arbeitnow European job feed (strong coverage in Germany, Switzerland, Austria, UK).
    """
    results: List[Dict[str, Any]] = []
    try:
        resp = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=8)
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            kw_lower = keywords.lower().strip()
            for item in data:
                title = item.get("title", "")
                desc = item.get("description", "")
                tags = " ".join(item.get("tags", []))
                comb = f"{title} {desc} {tags}".lower()
                
                # Check for keyword match or relevant ERP/PM match
                is_match = False
                if kw_lower in comb:
                    is_match = True
                elif any(k in comb for k in ["odoo", "erp", "project manager", "business analyst", "functional consultant"]):
                    is_match = True

                if is_match:
                    results.append({
                        "job_title": title,
                        "company_name": item.get("company_name", ""),
                        "location": item.get("location", "Europe"),
                        "country": "Germany" if "germany" in item.get("location", "").lower() else "Europe",
                        "website": item.get("url", ""),
                        "apply_url": item.get("url", ""),
                        "source": "Arbeitnow Europe",
                        "posted_time": "Recent",
                        "description": desc[:300] if desc else ""
                    })
                    if len(results) >= limit:
                        break
    except Exception as e:
        print(f"Arbeitnow job fetch note: {e}")
    return results

def search_live_jobs_multi_source(
    keywords: str = "Odoo",
    country: str = "India",
    limit: int = 25
) -> List[Dict[str, Any]]:
    """
    Aggregates fresh jobs from LinkedIn Public Guest API, European job boards,
    and returns a clean, deduplicated listing for the dashboard.
    """
    all_jobs: List[Dict[str, Any]] = []

    # 1. Fetch from LinkedIn Public Guest Jobs
    li_jobs = linkedin_engine.scrape_linkedin_guest_jobs(keywords=keywords, location=country, limit=limit)
    all_jobs.extend(li_jobs)

    # 2. If country is European (Germany, Switzerland, UK, Europe) or Global, also query Arbeitnow
    c_lower = country.lower()
    if any(k in c_lower for k in ["germany", "switzerland", "uk", "united kingdom", "europe", "dach", "global"]):
        ab_jobs = fetch_arbeitnow_jobs(keywords=keywords, limit=10)
        all_jobs.extend(ab_jobs)

    # Deduplicate by company name & job title
    seen = set()
    deduped: List[Dict[str, Any]] = []
    for j in all_jobs:
        key = f"{j['company_name'].lower().strip()}_{j['job_title'].lower().strip()}"
        if key not in seen:
            seen.add(key)
            deduped.append(j)

    return deduped[:limit]

def queue_company_to_outreach(
    company_name: str,
    website: str = "",
    country: str = "India",
    job_title: str = "Odoo Functional Consultant / Junior Project Manager"
) -> Dict[str, Any]:
    """
    Enriches a discovered company:
    1. Extracts domain.
    2. Crawls corporate website for HR/Career email addresses.
    3. Runs strict DNS MX deliverability verification.
    4. Queues into SQLite database (`partners` table) for autonomous outreach.
    """
    clean_company = company_name.strip()
    if not clean_company:
        return {"success": False, "message": "Company name is empty."}

    discovered_email = ""
    mx_valid = False
    mx_reason = "No website provided for email discovery"

    # Try email discovery if website is provided and not a generic aggregator
    if website:
        is_aggregator = any(agg in website.lower() for agg in [
            "indeed.com", "linkedin.com", "remoteok.", "remotive.", "jobicy."
        ])
        if not is_aggregator:
            emails = email_finder.find_emails_for_website(website)
            if emails:
                discovered_email = emails[0]
                is_valid, reason = email_verifier.verify_email_deliverability(discovered_email)
                mx_valid = is_valid
                mx_reason = reason
            else:
                mx_reason = "No emails found on website; queued for background discovery"

    # Add to SQLite partners table
    partner_id = db.add_partner(
        company_name=clean_company,
        website=website,
        contact_email=discovered_email if mx_valid else "",
        country=country,
        city="",
        partner_tier=f"Radar Lead: {job_title[:30]}",
        source="linkedin_indeed_radar"
    )

    if partner_id:
        if discovered_email and mx_valid:
            msg = f"✅ Added '{clean_company}' to Outreach CRM with MX-verified email: {discovered_email}"
        else:
            msg = f"📥 Added '{clean_company}' to Pipeline. Domain saved; will enrich recruiter email in background."
        return {
            "success": True,
            "partner_id": partner_id,
            "company_name": clean_company,
            "email": discovered_email if mx_valid else "",
            "mx_verified": mx_valid,
            "message": msg
        }
    else:
        return {
            "success": False,
            "company_name": clean_company,
            "message": f"ℹ️ '{clean_company}' is already in your Pipeline or Blacklist."
        }
