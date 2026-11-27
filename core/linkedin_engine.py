"""
LinkedIn Integration Engine for Automated Job Outreach
Provides:
1. Safe Google X-Ray & LinkedIn search query generation for Recruiters, HR & Hiring Managers.
2. Character-capped Connection Note Generator (STRICTLY <= 300 characters for LinkedIn free connect limit).
3. Long-form Recruiter InMail & Message Generator (~150 words).
4. Public LinkedIn Guest Job Feed Crawler (zero credentials, zero ban risk, with rotating headers and smart caching).
"""
import urllib.parse
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import config
from core import candidate_profile

# In-memory cache for public LinkedIn job fetches to avoid 429 rate limits
_JOB_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 900  # 15 minutes

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

def build_recruiter_search_urls(company_name: str, country: str = "", role_focus: str = "Odoo") -> Dict[str, str]:
    """
    Builds direct Google X-Ray and LinkedIn People search links for finding recruiters
    at a specific company without risking account flags.
    """
    clean_company = company_name.strip()
    
    # 1. Google X-Ray Query (Public, highly accurate)
    # site:linkedin.com/in/ ("recruiter" OR "talent acquisition" OR "HR" OR "hiring") ("Odoo" OR "ERP") "Company"
    xray_terms = f'site:linkedin.com/in/ ("recruiter" OR "talent acquisition" OR "HR" OR "hiring manager") "{clean_company}"'
    if country and country.lower() != "global":
        xray_terms += f' "{country}"'
    google_xray_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(xray_terms)}"

    # 2. Direct LinkedIn People Search URL
    li_people_query = f"{clean_company} recruiter talent acquisition {role_focus}"
    linkedin_people_url = f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote_plus(li_people_query)}"

    # 3. Direct LinkedIn Company Jobs URL
    li_jobs_query = f"{role_focus} {clean_company}"
    linkedin_jobs_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote_plus(li_jobs_query)}"

    return {
        "google_xray_url": google_xray_url,
        "linkedin_people_url": linkedin_people_url,
        "linkedin_jobs_url": linkedin_jobs_url,
        "company_name": clean_company,
        "country": country
    }

def generate_connection_note(
    company_name: str,
    recruiter_name: str = "",
    target_role: str = "Odoo Functional Consultant",
    style: str = "high_impact"
) -> str:
    """
    Generates a personalized connection request note guaranteed to be strictly <= 300 characters.
    Free LinkedIn connection requests have a hard 300-character ceiling.
    """
    comp = company_name.strip() or "your company"
    greeting = f"Hi {recruiter_name.strip().split()[0]}," if recruiter_name and recruiter_name.strip() else "Hi,"

    if style == "high_impact":
        # Emphasizes 9-store rollout + MCA + immediate availability
        note = (
            f"{greeting} noticed {comp}'s ERP work. I recently coordinated a live 9-store "
            f"Odoo retail rollout (CRM, Sales, Inv, Accounts, UAT) + MCA background. "
            f"Immediate 0-day joiner. Would love to connect & contribute to your team!"
        )
    elif style == "role_focused":
        # Directly targets an open requisition
        short_role = target_role.replace(" / ERP Functional Consultant", "").replace("Junior ", "")
        note = (
            f"{greeting} saw {comp}'s work in ERP/{short_role}. I bring hands-on experience "
            f"leading 9-store Odoo implementations, BRD/FRD specs, and UAT defect tracking. "
            f"Immediate joiner (0-day notice). Let's connect!"
        )
    elif style == "recruiter_inquiry":
        # Soft outreach for talent acquisition
        note = (
            f"{greeting} reaching out regarding ERP/Odoo talent at {comp}. MCA grad with "
            f"full lifecycle Odoo experience across 9 retail branches & immediate joining. "
            f"Would value connecting with you as opportunities arise!"
        )
    else:
        # Balanced standard
        note = (
            f"{greeting} reaching out regarding Odoo & ERP projects at {comp}. Coordinated a "
            f"live 9-store Odoo rollout across 6 core modules with UAT sign-off. Immediate joiner. "
            f"Would love to connect!"
        )

    # Hard-enforce the 300-character LinkedIn limit
    if len(note) > 300:
        # Intelligently truncate without breaking words
        truncated = note[:296]
        last_space = truncated.rfind(" ")
        if last_space > 250:
            note = truncated[:last_space] + "..."
        else:
            note = truncated + "..."

    return note

def generate_inmail_pitch(
    company_name: str,
    recruiter_name: str = "",
    target_role: str = "Odoo Functional Consultant / Junior Project Manager",
    country: str = "Global"
) -> Dict[str, str]:
    """
    Generates a high-converting, structured 150-word InMail / direct message for recruiters.
    """
    p = candidate_profile.CANDIDATE_DATA["personal"]
    greeting = f"Dear {recruiter_name.strip()}," if recruiter_name and recruiter_name.strip() else "Dear Hiring Team,"
    
    subject = f"Odoo & ERP Implementation Specialist — Adithiya B Vinu ({target_role})"
    
    body = f"""{greeting}

I hope you are having a productive week. I am reaching out to explore potential {target_role} opportunities with {company_name}'s ERP practice.

I bring hands-on experience coordinating a live, multi-module Odoo retail implementation across 9 store branches at Empire AE IT Services. My core deliverables:
• Functional Validation: Tested end-to-end workflows across CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR.
• Business Analysis: Authored BRD/FRD-aligned SOPs and multi-level approval hierarchies.
• UAT & Quality: Executed test cases, logged Jira defects, and secured stakeholder sign-off.
• Hypercare & Enablement: Trained store teams across 9 locations, minimizing post-go-live escalations.

Key Logistics:
• Immediate Joiner (0 days notice period)
• MCA from Marian College Kuttikanam (MG University, Kerala)
• Open to relocation to {country} or remote engagement

I would welcome a brief 10-minute introductory call. My resume and implementation case studies are readily available.

Best regards,

{p['name']}
{p['title']}
Email: {p['email']} | Phone: {p['phone']}
LinkedIn: {p['linkedin']}
""".strip()

    return {
        "subject": subject,
        "body": body,
        "word_count": len(body.split())
    }

def scrape_linkedin_guest_jobs(
    keywords: str = "Odoo",
    location: str = "India",
    limit: int = 15
) -> List[Dict[str, Any]]:
    """
    Scrapes live LinkedIn job listings via public guest endpoint.
    Zero authentication needed; zero ban risk for the user's account.
    Cached for 15 minutes to respect LinkedIn guest rate limits.
    """
    cache_key = f"{keywords.lower().strip()}_{location.lower().strip()}"
    now = time.time()
    
    if cache_key in _JOB_CACHE:
        cached_entry = _JOB_CACHE[cache_key]
        if now - cached_entry["timestamp"] < CACHE_TTL_SECONDS:
            return cached_entry["data"][:limit]

    url = (
        f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
        f"keywords={urllib.parse.quote_plus(keywords)}&"
        f"location={urllib.parse.quote_plus(location)}&start=0"
    )
    
    headers = {
        "User-Agent": USER_AGENTS[int(now) % len(USER_AGENTS)],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.linkedin.com/jobs/search",
        "Cache-Control": "max-age=0"
    }

    results: List[Dict[str, Any]] = []
    try:
        resp = requests.get(url, headers=headers, timeout=9)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.find_all("li")
            for item in items:
                title_el = item.find("h3", class_="base-search-card__title")
                comp_el = item.find("h4", class_="base-search-card__subtitle")
                loc_el = item.find("span", class_="job-search-card__location")
                link_el = item.find("a", class_="base-card__full-link")
                time_el = item.find("time")
                
                title = title_el.get_text(strip=True) if title_el else ""
                company = comp_el.get_text(strip=True) if comp_el else ""
                loc = loc_el.get_text(strip=True) if loc_el else location
                link = link_el["href"] if link_el and "href" in link_el.attrs else ""
                posted_time = time_el.get_text(strip=True) if time_el else "Recent"

                # Clean tracking params from job url
                if link and "?" in link:
                    link = link.split("?")[0]

                if title and company:
                    results.append({
                        "job_title": title,
                        "company_name": company,
                        "location": loc,
                        "apply_url": link,
                        "posted_time": posted_time,
                        "source": "LinkedIn Public Jobs",
                        "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    if len(results) >= limit:
                        break

            # Cache the successful result
            _JOB_CACHE[cache_key] = {
                "timestamp": now,
                "data": results
            }
        elif resp.status_code == 429:
            # Rate limited, return previous cache if exists
            if cache_key in _JOB_CACHE:
                return _JOB_CACHE[cache_key]["data"][:limit]
    except Exception as e:
        print(f"LinkedIn public jobs fetch note: {e}")
        if cache_key in _JOB_CACHE:
            return _JOB_CACHE[cache_key]["data"][:limit]

    return results
