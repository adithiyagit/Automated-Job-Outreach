"""
Multi-Source Fresh Job Openings Aggregator & Live Crawler
Monitors fresh job openings for Odoo Functional Consultant & Junior Project Manager roles
across RemoteOK, Remotive, Jobicy, and global career feeds.
Extracts recruiter/HR emails and verifies MX records before saving.
"""
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from core import db, email_finder, email_verifier

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

TARGET_KEYWORDS = [
    "odoo", "erp functional", "project manager", "business analyst",
    "erp implementation", "functional consultant"
]

def is_relevant_job(title: str, description: str) -> bool:
    """Checks if a job title or description matches Adithiya's target roles."""
    comb = f"{title} {description}".lower()
    return any(k in comb for k in TARGET_KEYWORDS)

def fetch_remoteok_jobs() -> List[Dict[str, Any]]:
    """Crawls RemoteOK API for fresh ERP & Odoo positions."""
    results = []
    for tag in ["odoo", "erp"]:
        url = f"https://remoteok.com/api?tag={tag}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                for item in data[1:]: # Skip legal disclaimer item
                    pos = item.get("position", "")
                    desc = item.get("description", "")
                    if is_relevant_job(pos, desc):
                        results.append({
                            "job_title": pos,
                            "company_name": item.get("company", ""),
                            "country": item.get("location", "Remote Global"),
                            "website": item.get("company_url", ""),
                            "apply_url": item.get("apply_url", item.get("url", "")),
                            "description": desc[:600],
                            "source": "RemoteOK"
                        })
        except Exception as e:
            print(f"RemoteOK fetch note: {e}")
    return results

def fetch_remotive_jobs() -> List[Dict[str, Any]]:
    """Crawls Remotive API for fresh ERP & Project Manager listings."""
    results = []
    for q in ["odoo", "erp", "project manager"]:
        url = f"https://remotive.com/api/remote-jobs?search={q}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200:
                jobs = resp.json().get("jobs", [])
                for item in jobs:
                    title = item.get("title", "")
                    desc = item.get("description", "")
                    if is_relevant_job(title, desc):
                        results.append({
                            "job_title": title,
                            "company_name": item.get("company_name", ""),
                            "country": item.get("candidate_required_location", "Remote Global"),
                            "website": item.get("url", ""),
                            "apply_url": item.get("url", ""),
                            "description": desc[:600],
                            "source": "Remotive"
                        })
        except Exception as e:
            print(f"Remotive fetch note: {e}")
    return results

def fetch_jobicy_jobs() -> List[Dict[str, Any]]:
    """Crawls Jobicy API for global remote positions."""
    results = []
    url = "https://jobicy.com/api/v2/remote-jobs?count=25&tag=management"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        if resp.status_code == 200:
            jobs = resp.json().get("jobs", [])
            for item in jobs:
                title = item.get("jobTitle", "")
                desc = item.get("jobDescription", "")
                if is_relevant_job(title, desc):
                    results.append({
                        "job_title": title,
                        "company_name": item.get("companyName", ""),
                        "country": item.get("jobGeo", "Global"),
                        "website": item.get("url", ""),
                        "apply_url": item.get("url", ""),
                        "description": desc[:600],
                        "source": "Jobicy"
                    })
    except Exception as e:
        print(f"Jobicy fetch note: {e}")
    return results

def sync_all_fresh_jobs(max_enrich: int = 10) -> Dict[str, Any]:
    """
    Aggregates fresh openings across all platforms, finds valid recruiter emails,
    verifies DNS MX records, and queues deliverable leads into SQLite.
    """
    all_jobs = []
    all_jobs.extend(fetch_remoteok_jobs())
    all_jobs.extend(fetch_remotive_jobs())
    all_jobs.extend(fetch_jobicy_jobs())

    # Deduplicate by company name
    seen_companies = set()
    unique_jobs = []
    for j in all_jobs:
        c_name = j["company_name"].strip().lower()
        if c_name and c_name not in seen_companies:
            seen_companies.add(c_name)
            unique_jobs.append(j)

    stats = {
        "found_openings": len(unique_jobs),
        "added_to_queue": 0,
        "emails_discovered": 0,
        "mx_verified": 0,
        "mx_failed": 0
    }

    enriched_count = 0
    for j in unique_jobs:
        comp = j["company_name"]
        site = j.get("website", "")
        email = ""

        # Crawl website for careers/HR email if we have website link
        is_aggregator_site = any(agg in site.lower() for agg in [
            "jobicy.com", "remoteok.", "remotive.", "indeed.com",
            "linkedin.com", "glassdoor.com", "monster.com", "ziprecruiter.com",
            "wellfound.com", "angel.co", "simplyhired.com"
        ])

        if site and not is_aggregator_site and enriched_count < max_enrich:
            discovered = email_finder.find_emails_for_website(site)
            if discovered:
                candidate_email = discovered[0]
                is_valid, reason = email_verifier.verify_email_deliverability(candidate_email)
                if is_valid and not any(agg in candidate_email for agg in ["jobicy", "remoteok", "remotive"]):
                    email = candidate_email
                    stats["emails_discovered"] += 1
                    stats["mx_verified"] += 1
                else:
                    stats["mx_failed"] += 1
            enriched_count += 1

        pid = db.add_partner(
            company_name=comp,
            website=site,
            contact_email=email,
            country=j.get("country", "Remote Global"),
            city="Remote",
            partner_tier=f"Live Opening: {j['job_title'][:30]}",
            source=j.get("source", "job_board")
        )
        if pid:
            stats["added_to_queue"] += 1

    return stats
