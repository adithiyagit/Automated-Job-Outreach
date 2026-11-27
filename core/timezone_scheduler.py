"""
Timezone & Country HR Work Hours Scheduler
Maps countries to local timezones and calculates HR business starting hours
so applications arrive in recruiters' inboxes between 8:30 AM and 11:30 AM local time.
"""
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # Python < 3.9 fallback

# Comprehensive country-to-timezone mapping
COUNTRY_TIMEZONE_MAP = {
    # Middle East & Gulf (Work hours typically start 8:00-8:30 AM)
    "united arab emirates": "Asia/Dubai",
    "uae": "Asia/Dubai",
    "dubai": "Asia/Dubai",
    "abu dhabi": "Asia/Dubai",
    "saudi arabia": "Asia/Riyadh",
    "ksa": "Asia/Riyadh",
    "qatar": "Asia/Qatar",
    "oman": "Asia/Muscat",
    "bahrain": "Asia/Bahrain",
    "kuwait": "Asia/Kuwait",

    # Central & Western Europe (Work hours typically start 8:30-9:00 AM)
    "switzerland": "Europe/Zurich",
    "germany": "Europe/Berlin",
    "france": "Europe/Paris",
    "united kingdom": "Europe/London",
    "uk": "Europe/London",
    "great britain": "Europe/London",
    "ireland": "Europe/Dublin",
    "netherlands": "Europe/Amsterdam",
    "belgium": "Europe/Brussels",
    "spain": "Europe/Madrid",
    "italy": "Europe/Rome",
    "austria": "Europe/Vienna",
    "poland": "Europe/Warsaw",
    "sweden": "Europe/Stockholm",

    # North America
    "united states": "America/New_York",
    "usa": "America/New_York",
    "us": "America/New_York",
    "canada": "America/Toronto",

    # Asia Pacific
    "singapore": "Asia/Singapore",
    "australia": "Australia/Sydney",
    "india": "Asia/Kolkata",
    "kerala": "Asia/Kolkata",
    "kochi": "Asia/Kolkata",
    "trivandrum": "Asia/Kolkata",
    "calicut": "Asia/Kolkata",
    "malaysia": "Asia/Kuala_Lumpur",

    # Default fallback
    "global": "UTC",
    "remote global": "UTC",
    "remote": "UTC"
}

def resolve_country_timezone(country_str: str) -> ZoneInfo:
    """Finds the ZoneInfo object for a given country or city name."""
    clean = (country_str or "").lower().strip()
    # Check exact match
    if clean in COUNTRY_TIMEZONE_MAP:
        tz_name = COUNTRY_TIMEZONE_MAP[clean]
        return ZoneInfo(tz_name)

    # Check substring match
    for k, tz_name in COUNTRY_TIMEZONE_MAP.items():
        if k in clean or clean in k:
            return ZoneInfo(tz_name)

    # Default fallback UTC
    return ZoneInfo("UTC")

def get_country_schedule_info(country: str) -> Dict[str, Any]:
    """
    Calculates current local time for the country and determines
    whether it is currently within the HR morning hiring window (8:30 AM - 11:30 AM)
    or regular business hours (8:00 AM - 17:00 PM).
    """
    tz = resolve_country_timezone(country)
    local_dt = datetime.now(tz)
    weekday = local_dt.weekday() # 0 = Monday, 6 = Sunday

    hour_decimal = local_dt.hour + (local_dt.minute / 60.0)

    # Check weekend (In UAE/Europe/US, weekend is Sat/Sun; in Saudi/Oman Friday/Sat)
    is_weekend = weekday in (5, 6) # Saturday, Sunday
    clean_c = (country or "").lower()
    if any(k in clean_c for k in ["saudi", "oman", "qatar"]) and weekday == 4:
        # Friday is holy weekend in parts of the Gulf
        is_weekend = True

    # Morning Prime Window: 8:30 AM to 1:00 PM (HR morning hiring & review window)
    is_morning_window = not is_weekend and (8.5 <= hour_decimal <= 13.0)

    # Full Business Hours: 8:00 AM to 6:00 PM
    is_business_hours = not is_weekend and (8.0 <= hour_decimal <= 18.0)

    if is_morning_window:
        status_label = "🟢 Morning Prime (8:30 AM - 1:00 PM)"
        priority_weight = 100
    elif is_business_hours:
        status_label = "🟡 Business Hours (Afternoon)"
        priority_weight = 50
    elif is_weekend:
        status_label = "⏸️ Weekend (Hold for Monday morning)"
        priority_weight = 10
    else:
        status_label = "🌙 After Hours (Queued for morning)"
        priority_weight = 20

    return {
        "country": country,
        "timezone_name": str(tz),
        "local_time_str": local_dt.strftime("%I:%M %p"),
        "local_date_str": local_dt.strftime("%A, %b %d"),
        "hour_decimal": hour_decimal,
        "is_morning_window": is_morning_window,
        "is_business_hours": is_business_hours,
        "is_weekend": is_weekend,
        "status_label": status_label,
        "priority_weight": priority_weight
    }

def interleave_by_country(partners_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Groups leads by country and rotates through them round-robin,
    ensuring that every batch reaches multiple distinct destination countries
    (e.g., India, Switzerland, UAE, Belgium, Singapore, etc.) simultaneously.
    """
    from collections import defaultdict
    if not partners_list:
        return []

    grouped = defaultdict(list)
    for p in partners_list:
        c = p.get("country", "Global")
        grouped[c].append(p)

    # Sort country buckets so countries currently in daytime or morning come first
    def country_priority(c_name):
        return get_country_schedule_info(c_name)["priority_weight"]

    sorted_countries = sorted(grouped.keys(), key=country_priority, reverse=True)

    result = []
    has_remaining = True
    while has_remaining:
        has_remaining = False
        for c in sorted_countries:
            if grouped[c]:
                result.append(grouped[c].pop(0))
                if grouped[c]:
                    has_remaining = True

    return result

def prioritize_by_timezone(partners_list: List[Dict[str, Any]], prefer_country: str = "") -> List[Dict[str, Any]]:
    """
    Sorts a list of partner/job leads so that those located in countries
    currently in their HR morning start window (8:30 AM - 1:00 PM) appear first.
    If prefer_country is set (e.g. 'India'), matching leads receive top priority.
    If prefer_country is empty or 'all', leads are round-robin interleaved across all countries.
    """
    if not partners_list:
        return []

    if prefer_country and prefer_country.lower() not in ("all", "global"):
        def get_sort_key(item):
            country = item.get("country", "Global")
            sched = get_country_schedule_info(country)
            weight = sched["priority_weight"]
            if prefer_country.lower() in country.lower():
                weight += 200
            return weight
        return sorted(partners_list, key=get_sort_key, reverse=True)

    # When targeting all countries, interleave round-robin across countries
    return interleave_by_country(partners_list)
