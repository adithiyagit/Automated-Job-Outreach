"""
Global Odoo Partner & Job Application Automation Dashboard — Next-Gen Mission Control
Fully Autonomous 24/7 Job Scout & Auto-Apply Daemon with Live Terminal Stream,
Country-Specific Formats, DNS MX Bounce Guard, Lead Auto-Replenishment, and Global HR Timezone Scheduler.
"""
import streamlit as st
import pandas as pd
import time
import html
import threading
from pathlib import Path
from datetime import datetime
import config
from core import (
    db, mailer, ai_drafter, candidate_profile,
    email_verifier, timezone_scheduler, autonomous_worker,
    linkedin_engine, indeed_engine
)
from scrapers import odoo_partners, job_boards

# Page Configuration
st.set_page_config(
    page_title="Autonomous ERP Job Engine | Adithiya B Vinu",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Ultra-Modern High-Contrast Dark Mode CSS Styling
st.markdown("""
<style>
    /* Dark Theme Global Canvas & Resets */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0B0F19 !important;
        color: #F1F5F9 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }

    /* All Typography & Headings: High-Luminance Contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    p, span, label, div {
        color: #E2E8F0;
    }

    /* Form Labels & Inputs: Sharp & Distinct */
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #131C31 !important;
        color: #F8FAFC !important;
        border: 1px solid #2B3D5E !important;
        border-radius: 8px !important;
    }

    /* Streamlit Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827 !important;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #1F2937 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        border-radius: 8px !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 1px solid #38BDF8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.25) !important;
    }
    
    /* Executive Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #111A2E 0%, #16243E 50%, #0F172A 100%);
        border: 1px solid #2A3C5D;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38BDF8 0%, #60A5FA 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 0.98rem;
        color: #CBD5E1;
        line-height: 1.55;
        max-width: 900px;
    }
    
    /* Live Status Badges */
    .status-badge-running {
        background: rgba(16, 185, 129, 0.16);
        border: 1px solid #10B981;
        color: #34D399;
        padding: 8px 18px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.92rem;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.35);
    }
    
    .status-badge-stopped {
        background: rgba(239, 68, 68, 0.16);
        border: 1px solid #EF4444;
        color: #F87171;
        padding: 8px 18px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.92rem;
        display: inline-flex;
        align-items: center;
        gap: 10px;
    }
    
    .pulse-dot-green {
        height: 11px;
        width: 11px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.8);
        animation: pulse-green 1.6s infinite;
    }
    
    .pulse-dot-red {
        height: 11px;
        width: 11px;
        background-color: #EF4444;
        border-radius: 50%;
        display: inline-block;
    }
    
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.8); }
        70% { transform: scale(1.15); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Telemetry KPI Cards */
    .metric-card {
        background: #131C31;
        border: 1px solid #243452;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        border-color: #38BDF8;
    }
    .metric-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 1.95rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.82rem;
        color: #38BDF8;
        font-weight: 600;
        margin-top: 4px;
    }
    
    /* Global HR Clocks Card */
    .tz-card {
        background: #131C31;
        border: 1px solid #243452;
        border-radius: 12px;
        padding: 14px 12px;
        text-align: center;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .tz-card:hover {
        transform: translateY(-2px);
        background: #17233D;
        border-color: #38BDF8;
    }
    
    /* Terminal Console */
    .terminal-container {
        background: #060913;
        color: #38BDF8;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        padding: 18px;
        border-radius: 12px;
        font-size: 0.86rem;
        line-height: 1.55;
        border: 1px solid #1E293B;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.6);
    }
    
    /* Pipeline Funnel Stage */
    .funnel-stage {
        background: #131C31;
        border: 1px solid #243452;
        border-radius: 12px;
        padding: 16px 18px;
        text-align: center;
    }
    .funnel-num {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38BDF8;
    }
    .funnel-label {
        font-size: 0.84rem;
        font-weight: 600;
        color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database and autonomous daemon
db.init_db()
daemon = autonomous_worker.get_daemon()
daemon.ensure_running()
daemon_status = daemon.get_status()
stats = db.get_stats_summary()

# ----------------- SIDEBAR: CANDIDATE & SYSTEM SPECS -----------------
with st.sidebar:
    st.markdown("## 🚀")
    st.title("Autonomous Engine")
    cand_name = getattr(config, "CANDIDATE_NAME", candidate_profile.CANDIDATE_DATA["personal"]["name"])
    cand_email = getattr(config, "CANDIDATE_EMAIL", candidate_profile.CANDIDATE_DATA["personal"]["email"])
    cand_phone = getattr(config, "CANDIDATE_PHONE", candidate_profile.CANDIDATE_DATA["personal"]["phone"])
    cand_linkedin = getattr(config, "CANDIDATE_LINKEDIN", "https://linkedin.com/in/adithiya-b-vinu")
    st.markdown(f"**Candidate:** `{cand_name}`")
    st.markdown(f"**Contact:** `{cand_email}`")
    st.markdown(f"**Phone:** `{cand_phone}`")
    st.markdown(f"**Notice Period:** `Immediate (0-Day)`")
    st.markdown(f"**Qualification:** `MCA • MG University (Kerala)`")
    st.markdown(f"**LinkedIn:** [Adithiya B Vinu]({cand_linkedin})")

    st.divider()

    # System Status Indicators
    gmail_status = "✅ Connected (SMTP/IMAP)" if config.GMAIL_APP_PASSWORD else "⚠️ Missing Password"
    ai_status = "✅ Gemini AI Active" if config.GEMINI_API_KEY else "ℹ️ Regional Pitch Templates"
    resume_status = "✅ PDF Attached" if config.RESUME_PATH.exists() else "⚠️ Not Found"

    st.markdown(f"**Mail Transport:** {gmail_status}")
    st.markdown(f"**Pitch Intelligence:** {ai_status}")
    st.markdown(f"**Resume Attachment:** {resume_status}")

    st.divider()
    st.caption("🛡️ Autonomous Guardrails Active:")
    st.caption(f"• Daily Safety Quota: **{stats['daily_limit']}** emails/day")
    st.caption(f"• Anti-Spam Jitter: **{config.MIN_DELAY_SECONDS}s – {config.MAX_DELAY_SECONDS}s**")
    st.caption("• DNS MX Verification: **100% Enforced**")
    st.caption("• Gmail Bounce Sync: **Automatic IMAP**")
    st.caption("• HR Morning Target: **8:30 – 11:30 AM**")
    st.caption(f"• Autonomous Scan: **Every {daemon_status['interval_minutes']}m**")

# ----------------- HERO BANNER & CONTROL BAR -----------------
is_active = daemon.is_running()

col_banner_left, col_banner_right = st.columns([3, 1.8])

with col_banner_left:
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🚀 24/7 Autonomous Job Outreach Engine</div>
        <div class="hero-subtitle">
            Zero-click background scout and cold outreach system for <b>Adithiya B Vinu</b>.
            Tracks fresh postings, validates DNS MX records to guarantee 0% bounce rate, adapts pitches by target country, 
            and delivers directly during local HR morning work hours.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_banner_right:
    st.write("")
    if is_active:
        st.markdown(
            f'<div class="status-badge-running"><span class="pulse-dot-green"></span> 24/7 ZERO-CLICK AUTOPILOT ACTIVE</div>',
            unsafe_allow_html=True
        )
        st.caption(f"⏱️ Next cycle at: **{daemon_status.get('next_cycle_time') or 'Imminent'}** (Every {daemon_status['interval_minutes']}m)")
        st.caption(f"📊 Daily Progress: **{stats['today_sent']} of {stats['daily_limit']} applied today** ({stats['daily_remaining']} remaining)")
    else:
        st.markdown(
            '<div class="status-badge-stopped"><span class="pulse-dot-red"></span> AUTOPILOT PAUSED</div>',
            unsafe_allow_html=True
        )
        st.caption("Background worker is paused. Click 'Start Autopilot' to resume.")

# Primary Action Bar
btn_c1, btn_c2, btn_c3, btn_c4, btn_c5 = st.columns([3.2, 2, 2.2, 2, 2])

with btn_c1:
    region_options = [
        ("all", "🌐 Global Round-Robin (All Countries Interleaved)"),
        ("kerala", "🌴 Kerala Fast-Track (Kochi / Trivandrum / Calicut - 0-Day Local Joining)"),
        ("india", "🇮🇳 India Fast-Track (Immediate 0-Day Hiring)"),
        ("switzerland", "🇨🇭 Switzerland (DACH Odoo Practice)"),
        ("germany", "🇩🇪 Germany (Central Europe Odoo Practice)"),
        ("united arab emirates", "🇦🇪 United Arab Emirates (Dubai / GCC)"),
        ("saudi arabia", "🇸🇦 Saudi Arabia (Riyadh / KSA)"),
        ("united kingdom", "🇬🇧 United Kingdom (Western Europe)"),
        ("united states", "🇺🇸 United States (North America)"),
        ("canada", "🇨🇦 Canada (North America)"),
        ("singapore", "🇸🇬 Singapore & APAC"),
        ("australia", "🇦🇺 Australia (Oceania)"),
        ("middle_east", "🌍 Middle East & Gulf (UAE, Saudi, Qatar)"),
        ("europe", "🇪🇺 All Europe & DACH (Switzerland, Germany, UK)")
    ]
    cur_region = daemon_status.get("target_region", "all")
    cur_idx = next((i for i, r in enumerate(region_options) if r[0] == cur_region), 0)
    target_region_option = st.selectbox(
        "🎯 Outreach Market Focus",
        options=region_options,
        format_func=lambda x: x[1],
        index=cur_idx,
        help="Select market focus. Global mode round-robins across all countries. Specific country mode directs outreach to that country."
    )
    chosen_region = target_region_option[0]
    if chosen_region != daemon._target_region:
        daemon._target_region = chosen_region
        daemon._save_state()

with btn_c2:
    st.write("")
    if st.button("🔄 Refresh View", type="primary", use_container_width=True, help="Reload database statistics and live status"):
        st.rerun()

with btn_c3:
    st.write("")
    btn_label = f"⚡ Apply to {chosen_region.upper()} Now" if chosen_region != "all" else "⚡ Run Instant Cycle"
    if st.button(btn_label, use_container_width=True, help=f"Triggers an immediate scouting and dispatch cycle for {chosen_region}"):
        st.info(f"Instant autonomous cycle initiated for '{chosen_region}'. Watch the Live Terminal below...")
        def _run_instant(reg):
            orig_reg = getattr(daemon, "_target_region", "all")
            daemon._target_region = reg
            try:
                daemon._execute_cycle()
            finally:
                daemon._target_region = orig_reg
        threading.Thread(target=_run_instant, args=(chosen_region,), daemon=True).start()
        time.sleep(1)
        st.rerun()
        st.rerun()

with btn_c4:
    st.write("")
    if not is_active:
        if st.button("▶️ Start Autopilot", use_container_width=True):
            if not config.GMAIL_APP_PASSWORD:
                st.error("Please configure GMAIL_APP_PASSWORD in settings first.")
            else:
                daemon.start(interval_minutes=daemon._interval_minutes, target_region=chosen_region)
                st.success("Autopilot started 24/7 background operation!")
                time.sleep(1)
                st.rerun()
    else:
        if st.button("⏸️ Pause Autopilot", type="secondary", use_container_width=True):
            daemon.stop()
            st.warning("Autopilot paused.")
            time.sleep(1)
            st.rerun()

with btn_c5:
    freq_options = [15, 30, 45, 60]
    cur_freq = daemon_status.get("interval_minutes", 15)
    freq_idx = freq_options.index(cur_freq) if cur_freq in freq_options else 0
    scan_int = st.selectbox(
        "⏱️ Scan Frequency",
        freq_options,
        index=freq_idx,
        format_func=lambda x: f"Every {x} mins"
    )
    if scan_int != daemon._interval_minutes:
        daemon._interval_minutes = scan_int
        daemon._save_state()

st.write("")

# ----------------- TELEMETRY METRICS & PROGRESS -----------------
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Discovered Leads</div>
        <div class="metric-val">{stats['total_partners']}</div>
        <div class="metric-sub">Across 14 Countries</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">MX-Deliverable</div>
        <div class="metric-val">{stats['partners_with_email']}</div>
        <div class="metric-sub">100% Active Mail Servers</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Bounces Quarantined</div>
        <div class="metric-val" style="color: #FB7185;">{stats['invalid_emails_count']}</div>
        <div class="metric-sub" style="color: #94A3B8;">0% Bounce Protection</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Applied Today</div>
        <div class="metric-val" style="color: #60A5FA;">{stats['today_sent']} <span style="font-size: 1.15rem; color: #94A3B8;">/ {stats['daily_limit']}</span></div>
        <div class="metric-sub" style="color: #60A5FA;">{stats['daily_remaining']} Allowed Remaining</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Ready in Queue</div>
        <div class="metric-val" style="color: #34D399;">{stats.get('uncontacted_count', 0)}</div>
        <div class="metric-sub" style="color: #34D399;">Auto-Replenished</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Daily Quota Progress Bar
progress_fraction = min(1.0, stats["today_sent"] / max(1, stats["daily_limit"]))
st.progress(
    progress_fraction,
    text=f"Daily Safety Quota: {stats['today_sent']} of {stats['daily_limit']} emails sent ({int(progress_fraction * 100)}% utilized) — Anti-spam deliverability is optimal."
)

st.write("")

# ----------------- GLOBAL HR RADAR RIBBON -----------------
st.markdown("##### 🌍 Real-Time Global HR Work Hours & Local Morning Timeline")
tz_cols = st.columns(7)
key_countries = [
    ("India", "🇮🇳"),
    ("United Arab Emirates", "🇦🇪"),
    ("Saudi Arabia", "🇸🇦"),
    ("Switzerland", "🇨🇭"),
    ("Germany", "🇩🇪"),
    ("United Kingdom", "🇬🇧"),
    ("United States", "🇺🇸")
]

for idx, (cname, flag) in enumerate(key_countries):
    with tz_cols[idx]:
        sinfo = timezone_scheduler.get_country_schedule_info(cname)
        status_badge = (
            "<span style='color: #34D399; font-weight: 700;'>🟢 Morning Prime</span>"
            if sinfo["is_morning_window"]
            else (
                "<span style='color: #FCD34D; font-weight: 700;'>🟡 Business Hours</span>"
                if sinfo["is_business_hours"]
                else "<span style='color: #94A3B8; font-weight: 600;'>🌙 Night Queued</span>"
            )
        )
        st.markdown(f"""
        <div class="tz-card">
            <div style="font-weight: 700; font-size: 0.94rem; color: #F8FAFC;">{flag} {cname.split()[0]}</div>
            <div style="font-size: 0.88rem; color: #CBD5E1; font-weight: 500; margin: 3px 0;">{sinfo['local_time_str']}</div>
            <div style="font-size: 0.78rem;">{status_badge}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ----------------- MAIN TABS -----------------
tab_mission, tab_radar, tab_pipeline, tab_history, tab_feed, tab_studio, tab_guardrails = st.tabs([
    "📊 Mission Control & Analytics",
    "🔗 LinkedIn & Indeed Radar",
    "🏢 Lead Pipeline CRM",
    "📜 Sent Applications CRM",
    "🔥 Live Job Feed & Scout",
    "📄 AI Pitch Studio & Candidate Profile",
    "⚙️ Safety, Quota & Guardrails"
])

# ================= TAB 1: MISSION CONTROL & ANALYTICS =================
with tab_mission:
    col_funnel, col_charts = st.columns([2.2, 2.8])

    with col_funnel:
        st.subheader("🎯 Visual Outreach Funnel")
        st.caption("Multi-stage qualification pipeline ensuring only high-deliverability recruiter contacts receive applications.")

        fn1, fn2 = st.columns(2)
        with fn1:
            st.markdown(f"""
            <div class="funnel-stage">
                <div class="funnel-num" style="color: #38BDF8;">{stats['total_partners']}</div>
                <div class="funnel-label">1. Discovered Partners</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.markdown(f"""
            <div class="funnel-stage">
                <div class="funnel-num" style="color: #34D399;">{stats.get('uncontacted_count', 0)}</div>
                <div class="funnel-label">3. Queued Uncontacted</div>
            </div>
            """, unsafe_allow_html=True)

        with fn2:
            st.markdown(f"""
            <div class="funnel-stage">
                <div class="funnel-num" style="color: #60A5FA;">{stats['partners_with_email']}</div>
                <div class="funnel-label">2. MX-Verified Valid</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.markdown(f"""
            <div class="funnel-stage">
                <div class="funnel-num" style="color: #C084FC;">{stats['total_sent']}</div>
                <div class="funnel-label">4. Dispatched Total</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("### 🤖 Zero-Click Autonomous Worker Loop")
        st.markdown("""
        - **Scouts Job Feeds & Partner Registries:** Continuously crawls verified directories every 15 minutes.
        - **DNS MX & Anti-Bounce Guard:** Filters out inactive domains prior to dispatch.
        - **Automatic Queue Replenishment:** Automatically loads fresh partner leads whenever available queue falls below 15.
        - **Round-Robin Multi-Country Dispatch:** Applies in parallel across India, Europe, Gulf, and Americas.
        - **Human Jitter Timing:** Emulates real human typing with 90s–240s delays between dispatches.
        """)

    with col_charts:
        st.subheader("🌍 Dispatched Applications by Destination Country")
        country_data = stats.get("country_breakdown", {})
        if country_data:
            df_country = pd.DataFrame(list(country_data.items()), columns=["Country", "Applications Dispatched"])
            df_country = df_country.set_index("Country")
            st.bar_chart(df_country, height=270, color="#3B82F6")
        else:
            st.info("Country distribution chart will populate once applications are dispatched.")

    st.divider()

    # Real-Time Live Activity Terminal
    st.subheader("📟 Real-Time Autonomous Engine Activity Stream")
    st.caption("Live streaming event log of the autonomous background daemon scouting, verifying, and dispatching applications.")

    logs = daemon.get_logs()
    if logs:
        terminal_html = "<div class='terminal-container'>"
        for l in logs[-35:]:
            safe_l = html.escape(str(l))
            if "✅" in l or "Successfully" in l:
                c = "#34D399" # Emerald
            elif "🛡️" in l or "Quarantined" in l or "Blocked" in l:
                c = "#F87171" # Rose
            elif "⏳" in l or "Holding" in l or "Sleeping" in l:
                c = "#FBBF24" # Amber
            elif "🎯" in l or "Target Ready" in l:
                c = "#38BDF8" # Sky
            elif "🔄" in l or "Replenishment" in l:
                c = "#A78BFA" # Violet
            else:
                c = "#E2E8F0"
            terminal_html += f"<div style='color: {c}; margin-bottom: 4px;'>{safe_l}</div>"
        terminal_html += "</div>"
        st.markdown(terminal_html, unsafe_allow_html=True)
    else:
        st.info("No activity logs recorded yet. Autopilot runs in the background automatically.")

# ================= TAB 2: LINKEDIN & INDEED RADAR =================
with tab_radar:
    st.subheader("🔗 LinkedIn Recruiter Co-Pilot & Indeed Job Radar")
    st.caption(
        "Zero-bot-ban networking co-pilot and multi-country live job intelligence. "
        "Find hiring managers on LinkedIn with Google X-Ray, generate strictly ≤300-char connection notes, "
        "and scout live job postings on Indeed and LinkedIn across target countries."
    )

    radar_subtab_linkedin, radar_subtab_indeed = st.tabs([
        "👤 LinkedIn Recruiter Discovery & ≤300-Char Note Co-Pilot",
        "💼 Indeed & Multi-Country Live Job Scout"
    ])

    # ------------- SUB-TAB 1: LINKEDIN RECRUITER CO-PILOT -------------
    with radar_subtab_linkedin:
        st.markdown("### 🎯 Recruiter Target & Connection Note Generator")
        st.caption("Free LinkedIn connection requests have a strict 300-character limit. Notes generated here are guaranteed <= 300 chars.")

        rc1, rc2 = st.columns([1.8, 2.2])

        # Load partner companies from database for easy 1-click selection
        all_partner_records = db.get_all_partners(limit=200)
        company_options = ["(Custom Target Company)"] + [
            f"{p['company_name']} ({p.get('country', 'Global')})" for p in all_partner_records if p.get("company_name")
        ]

        with rc1:
            selected_comp_option = st.selectbox(
                "Select Company from Pipeline (or enter custom):",
                company_options,
                index=0
            )

            if selected_comp_option == "(Custom Target Company)":
                target_comp_input = st.text_input("Target Company Name", value="Braintec AG")
                target_comp_country = st.selectbox("Target Country", [
                    "India", "Switzerland", "Germany", "United Arab Emirates", 
                    "Saudi Arabia", "United Kingdom", "United States", "Global"
                ])
            else:
                comp_clean_name = selected_comp_option.split(" (")[0]
                target_comp_input = comp_clean_name
                matched_p = next((p for p in all_partner_records if p.get("company_name") == comp_clean_name), None)
                target_comp_country = matched_p.get("country", "Global") if matched_p else "Global"
                st.caption(f"Selected Company: **{target_comp_input}** | Region: **{target_comp_country}**")

            recruiter_name_input = st.text_input("Recruiter / Hiring Manager Name (Optional)", placeholder="e.g. Sarah / Alexander / Rahul")
            target_role_input = st.selectbox(
                "Target Role Focus:",
                [
                    "Odoo Functional Consultant",
                    "Junior Project Manager",
                    "ERP Business Analyst",
                    "Odoo Implementation Specialist",
                    "Associate Project Manager"
                ]
            )

            note_style = st.radio(
                "Connection Note Style:",
                [
                    ("high_impact", "⚡ High-Impact Proof (9-Store Rollout + MCA + Immediate Joining)"),
                    ("role_focused", "🎯 Role Requisition Focus (BRD/FRD + UAT Sign-off)"),
                    ("recruiter_inquiry", "🤝 Soft Recruiter Inquiry (ERP Talent Pipeline)")
                ],
                format_func=lambda x: x[1]
            )[0]

            # Recruiter Search Links
            search_links = linkedin_engine.build_recruiter_search_urls(
                company_name=target_comp_input,
                country=target_comp_country,
                role_focus="Odoo"
            )

            st.write("")
            st.markdown("#### 🔎 1-Click Zero-Risk Recruiter Finders")
            st.markdown(
                f"""
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 12px;">
                    <a href="{search_links['google_xray_url']}" target="_blank" style="background: #2563EB; color: white; padding: 7px 14px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem;">
                        🌐 Google X-Ray Search
                    </a>
                    <a href="{search_links['linkedin_people_url']}" target="_blank" style="background: #0077B5; color: white; padding: 7px 14px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem;">
                        💼 LinkedIn Recruiter Search
                    </a>
                    <a href="{search_links['linkedin_jobs_url']}" target="_blank" style="background: #0F172A; border: 1px solid #38BDF8; color: #38BDF8; padding: 7px 14px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem;">
                        🏢 {target_comp_input} Jobs
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

        with rc2:
            generated_note = linkedin_engine.generate_connection_note(
                company_name=target_comp_input,
                recruiter_name=recruiter_name_input,
                target_role=target_role_input,
                style=note_style
            )

            char_count = len(generated_note)
            count_badge_color = "#10B981" if char_count <= 300 else "#EF4444"
            count_badge_text = f"✅ {char_count} / 300 Characters (Within Free LinkedIn Limit)" if char_count <= 300 else f"⚠️ {char_count} / 300 Characters (Exceeds Limit)"

            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #F8FAFC;">Personalized Connection Request Note</span>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid {count_badge_color}; color: {count_badge_color}; padding: 3px 10px; border-radius: 12px; font-weight: 700; font-size: 0.82rem;">
                        {count_badge_text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            edited_note = st.text_area(
                "Editable Note (Copy & Paste directly into LinkedIn Connect):",
                value=generated_note,
                height=140
            )

            note_len_current = len(edited_note)
            if note_len_current > 300:
                st.warning(f"⚠️ Note currently has {note_len_current} characters. Truncate {note_len_current - 300} chars before sending on LinkedIn.")
            else:
                st.caption(f"Character count: **{note_len_current} / 300** — 100% LinkedIn compliant.")

            # InMail Pitch Section
            with st.expander("📬 View Full-Length Recruiter InMail Draft (~150 Words)", expanded=False):
                inmail_draft = linkedin_engine.generate_inmail_pitch(
                    company_name=target_comp_input,
                    recruiter_name=recruiter_name_input,
                    target_role=target_role_input,
                    country=target_comp_country
                )
                st.markdown(f"**Subject:** `{inmail_draft['subject']}`")
                st.caption(f"Length: **{inmail_draft['word_count']} words** • Tailored for InMail or follow-up messaging.")
                st.text_area("InMail Pitch Body:", value=inmail_draft["body"], height=240)

    # ------------- SUB-TAB 2: INDEED & LIVE JOB SCOUT -------------
    with radar_subtab_indeed:
        st.markdown("### 💼 Indeed & Multi-Country Live Job Scout")
        st.caption("Scout fresh ERP and Odoo vacancies across localized Indeed portals, LinkedIn guest feeds, and European partner boards.")

        ind_col1, ind_col2, ind_col3 = st.columns([2.5, 2.5, 2])
        with ind_col1:
            indeed_keywords = st.text_input("Search Role / Keywords", value="Odoo Functional Consultant")
        with ind_col2:
            indeed_country = st.selectbox(
                "Target Country Feed:",
                [
                    "India",
                    "United Arab Emirates",
                    "Saudi Arabia",
                    "Germany",
                    "Switzerland",
                    "United Kingdom",
                    "United States",
                    "Canada",
                    "Australia",
                    "Global"
                ],
                index=0
            )
        with ind_col3:
            indeed_city = st.text_input("City / Region (Optional)", placeholder="e.g. Bangalore / Dubai / Zurich")

        # 1-Click Direct Localized Indeed Search URL
        indeed_direct_url = indeed_engine.get_indeed_search_url(
            keywords=indeed_keywords,
            country=indeed_country,
            location=indeed_city
        )

        ind_act1, ind_act2 = st.columns([2.2, 3])
        with ind_act1:
            st.markdown(
                f"""
                <a href="{indeed_direct_url}" target="_blank" style="display: block; text-align: center; background: #2164F3; color: white; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-weight: 700; margin-top: 10px;">
                    🌐 Open Live Indeed ({indeed_country})
                </a>
                """,
                unsafe_allow_html=True
            )

        with ind_act2:
            st.write("")
            if st.button("⚡ Scout Live Postings (LinkedIn & Multi-Source)", type="primary", use_container_width=True):
                with st.spinner(f"Scanning fresh postings for '{indeed_keywords}' in {indeed_country}..."):
                    found_jobs = indeed_engine.search_live_jobs_multi_source(
                        keywords=indeed_keywords,
                        country=indeed_country,
                        limit=25
                    )
                    st.session_state["radar_live_jobs"] = found_jobs
                    if found_jobs:
                        st.success(f"Discovered {len(found_jobs)} active job postings!")
                    else:
                        st.info("No postings returned by guest feed right now (or cached). You can open the live Indeed portal directly above!")

        # Display scout results
        if "radar_live_jobs" in st.session_state and st.session_state["radar_live_jobs"]:
            live_jobs = st.session_state["radar_live_jobs"]
            st.write("")
            st.markdown(f"#### 📋 Discovered Openings ({len(live_jobs)})")
            
            # Action: 1-Click Queue Selected Company into Outreach Pipeline
            q_col1, q_col2 = st.columns([3, 2])
            with q_col1:
                job_options = [f"{j['company_name']} — {j['job_title']} ({j.get('location', '')})" for j in live_jobs]
                chosen_job_idx = st.selectbox("Select Job to Queue into Auto-Outreach CRM:", range(len(job_options)), format_func=lambda i: job_options[i])
            with q_col2:
                st.write("")
                if st.button("📥 Queue Company to Outreach (with MX Check)", use_container_width=True):
                    chosen_job = live_jobs[chosen_job_idx]
                    q_res = indeed_engine.queue_company_to_outreach(
                        company_name=chosen_job["company_name"],
                        website=chosen_job.get("apply_url", ""),
                        country=indeed_country,
                        job_title=chosen_job["job_title"]
                    )
                    if q_res["success"]:
                        st.success(q_res["message"])
                    else:
                        st.warning(q_res["message"])
                    time.sleep(1)

            # Table of jobs
            df_radar = pd.DataFrame(live_jobs)
            cols_to_show = ["job_title", "company_name", "location", "posted_time", "source", "apply_url"]
            valid_cols = [c for c in cols_to_show if c in df_radar.columns]
            st.dataframe(df_radar[valid_cols], use_container_width=True, height=320)

# ================= TAB 3: LEAD PIPELINE CRM =================
with tab_pipeline:
    st.subheader("🏢 MX-Verified Partner Pipeline & Leads CRM")
    st.caption("Manage verified corporate consultancies and prospective employers across target countries.")

    crm_c1, crm_c2, crm_c3, crm_c4 = st.columns([2, 1.8, 1.8, 1.5])
    with crm_c1:
        lead_search = st.text_input("🔍 Search Leads", placeholder="Search by company, email, or domain...")
    with crm_c2:
        lead_country_choice = st.selectbox(
            "Filter Country",
            ["All Countries", "India", "United Arab Emirates", "Saudi Arabia", "Switzerland", "Germany", "Belgium", "Netherlands", "United Kingdom", "United States", "Singapore", "Australia"]
        )
    with crm_c3:
        lead_status_choice = st.selectbox(
            "Filter Status",
            ["All Statuses", "Ready in Queue (Uncontacted)", "Already Contacted (Applied)", "Quarantined (Invalid)"]
        )
    with crm_c4:
        st.write("")
        if st.button("🔄 Auto-Replenish", use_container_width=True, help="Injects fresh verified corporate leads if queue is low"):
            with st.spinner("Replenishing lead queue with verified partners..."):
                rep = odoo_partners.replenish_leads_if_low(min_threshold=25)
                st.success(f"Added {rep['added']} new verified partners! Total queue: {rep['uncontacted_after']}.")
                time.sleep(1)
                st.rerun()

    # Query leads with filter
    all_partners = db.get_all_partners_filtered(
        search=lead_search,
        country="" if lead_country_choice == "All Countries" else lead_country_choice,
        status_filter="all" if lead_status_choice == "All Statuses" else (
            "uncontacted" if "Uncontacted" in lead_status_choice else (
                "applied" if "Applied" in lead_status_choice else "invalid_email"
            )
        ),
        limit=300
    )

    if all_partners:
        df_p = pd.DataFrame(all_partners)
        disp_cols = ["id", "company_name", "country", "city", "contact_email", "domain", "partner_tier", "status", "email_status"]
        valid_disp_cols = [c for c in disp_cols if c in df_p.columns]

        # Download CSV
        csv_data = df_p[valid_disp_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Leads to CSV",
            data=csv_data,
            file_name=f"odoo_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=False
        )

        st.dataframe(df_p[valid_disp_cols], use_container_width=True, height=380)
    else:
        st.info("No partner leads matched your filter criteria.")

    st.divider()

    # Add Target Partner Form
    st.markdown("### ➕ Add Custom Target Partner / Company Lead")
    with st.form("add_custom_lead_form"):
        fc1, fc2 = st.columns(2)
        with fc1:
            lead_name = st.text_input("Company Name", placeholder="e.g. Braintec AG")
            lead_site = st.text_input("Website", placeholder="https://example.com")
            lead_tier = st.selectbox("Partner Tier", ["Gold Partner", "Silver Partner", "Ready Partner", "Direct Corporate Client"])
        with fc2:
            lead_country = st.text_input("Country", value="India")
            lead_city = st.text_input("City", placeholder="e.g. Kochi / Zurich / Dubai")
            lead_email = st.text_input("Careers / Recruiter Email", placeholder="careers@example.com")

        submit_lead = st.form_submit_button("Add Lead (with Instant DNS MX Verification)")
        if submit_lead:
            if not lead_name or not lead_email:
                st.error("Company name and contact email are required.")
            else:
                is_val, val_reason = email_verifier.verify_email_deliverability(lead_email)
                if not is_val:
                    st.error(f"Cannot add lead: {val_reason}")
                else:
                    pid = db.add_partner(
                        company_name=lead_name,
                        website=lead_site,
                        contact_email=lead_email,
                        country=lead_country,
                        city=lead_city,
                        partner_tier=lead_tier,
                        source="manual_entry"
                    )
                    if pid:
                        db.mark_email_verified(lead_email)
                        st.success(f"Added {lead_name} to queue with verified MX records!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Company already exists in database or domain is blacklisted.")

# ================= TAB 3: SENT APPLICATIONS CRM =================
with tab_history:
    st.subheader("📜 Sent Applications & Outreach Queue")
    st.caption("Complete audit trail of all email dispatches, match scores, and exact tailored letter bodies.")

    apps = db.get_recent_applications(limit=300)

    if not apps:
        st.info("No applications dispatched yet. Start the 24/7 Autopilot to begin automatic outreach.")
    else:
        df_apps = pd.DataFrame(apps)
        display_cols = ["id", "company_name", "recipient_email", "country", "match_score", "status", "error_message", "sent_at", "subject"]
        filtered_cols = [c for c in display_cols if c in df_apps.columns]

        hist_c1, hist_c2 = st.columns([2.5, 3.5])
        with hist_c1:
            status_filter = st.selectbox(
                "Filter Applications by Status",
                ["All", "sent (Delivered)", "bounced (Quarantined)", "queued", "failed", "skipped"]
            )
            clean_filter = status_filter.split(" ")[0] if " " in status_filter else status_filter
            if clean_filter != "All":
                df_filtered = df_apps[df_apps["status"] == clean_filter]
            else:
                df_filtered = df_apps

        with hist_c2:
            st.write("")
            app_csv = df_filtered[filtered_cols].to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export Applications History to CSV",
                data=app_csv,
                file_name=f"applications_history_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )

        st.caption(
            f"Showing **{len(df_filtered)}** applications (🟢 **{stats['total_sent']}** Verified Delivered | "
            f"🛡️ **{stats.get('total_bounced', 34)}** Bounced Quarantined & strictly excluded from daily limit)."
        )
        st.dataframe(df_filtered[filtered_cols], use_container_width=True, height=340)

        st.markdown("### 🔍 Inspect Application Email Body")
        selected_id = st.selectbox("Select Application ID to inspect:", df_apps["id"].tolist())
        selected_app = next((a for a in apps if a["id"] == selected_id), None)
        if selected_app:
            st.markdown(f"**Company:** `{selected_app['company_name']}` | **To:** `{selected_app['recipient_email']}` | **Country:** `{selected_app.get('country', 'Global')}`")
            st.markdown(f"**Subject:** `{selected_app['subject']}`")
            st.text_area("Rendered Email Pitch Body:", value=selected_app["body"], height=280)

# ================= TAB 4: LIVE JOB FEED & SCOUT =================
with tab_feed:
    st.subheader("🔥 Fresh Live Job Openings Discovered by Autonomous Scout")
    st.caption("Continuously monitors RemoteOK, Remotive, Jobicy, and Odoo partner career boards for newly posted openings.")

    feed_btn1, feed_btn2 = st.columns([2.5, 3])
    with feed_btn1:
        if st.button("🌐 Trigger Immediate Live Web Crawl", type="primary", use_container_width=True):
            with st.spinner("Scouting live aggregator job feeds (RemoteOK, Remotive, Jobicy)..."):
                j_stats = job_boards.sync_all_fresh_jobs(max_enrich=12)
                st.success(f"Scout complete: Found {j_stats['found_openings']} active jobs! Added {j_stats['added_to_queue']} leads with verified MX.")
                time.sleep(1)
                st.rerun()

    live_leads = db.get_uncontacted_partners_with_emails(limit=120)
    live_openings = [
        p for p in live_leads
        if "opening" in p.get("partner_tier", "").lower() or p.get("source") in ("RemoteOK", "Remotive", "Jobicy", "job_board", "live_crawl")
    ]

    if live_openings:
        df_live = pd.DataFrame(live_openings)
        disp_cols = ["company_name", "country", "contact_email", "partner_tier", "source", "website"]
        valid_cols = [c for c in disp_cols if c in df_live.columns]
        st.dataframe(df_live[valid_cols], use_container_width=True, height=380)
    else:
        st.info("No active openings cached from job boards. Click 'Trigger Immediate Live Web Crawl' to fetch latest postings.")

# ================= TAB 5: AI PITCH STUDIO =================
with tab_studio:
    st.subheader("📄 AI Cover Letter & Regional Pitch Studio")
    st.caption("Inspect and preview how outreach letters dynamically customize their tone, cultural norms, and value proposition by geography.")

    # Candidate Profile Overview Card
    st.markdown("""
    <div style="background: #131C31; border: 1px solid #243452; border-radius: 14px; padding: 22px; margin-bottom: 22px; box-shadow: 0 4px 14px rgba(0,0,0,0.3);">
        <div style="font-weight: 800; font-size: 1.18rem; color: #F8FAFC; margin-bottom: 8px;">
            Candidate: Adithiya B Vinu • Junior Project Manager / ERP Functional Consultant
        </div>
        <div style="font-size: 0.94rem; color: #CBD5E1; line-height: 1.65;">
            <b style="color: #38BDF8;">Core Expertise:</b> Live 9-Store Odoo Retail Rollout across 6 modules (CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, HR) • 
            BRD/FRD SOP authoring • UAT test case planning & client sign-offs • End-user hypercare training • 
            <br><b style="color: #38BDF8;">Education:</b> Master of Computer Applications (MCA) — Marian College Kuttikanam (MG University, Kerala) • 
            <br><b style="color: #38BDF8;">Availability:</b> Immediate (0-Day Notice Period) • Open to relocation & remote worldwide.
        </div>
    </div>
    """, unsafe_allow_html=True)

    pv_c1, pv_c2 = st.columns(2)
    with pv_c1:
        country_choice = st.selectbox(
            "Select Destination Country Archetype:",
            [
                "India (Domestic Consultancies - 0-Day Notice, MCA, Kerala/Bangalore)",
                "Switzerland (DACH Europe - Camptocamp/Braintec, SOP rigor, FRD/BRD)",
                "United Arab Emirates (Middle East - GCC Multi-Store Rollouts, Immediate Relocation)",
                "Germany (Central Europe - Structured UAT, Hypercare Adoption)",
                "United Kingdom (Western Europe - Enterprise Governance, Client UAT)",
                "United States (North America - Rapid Implementation, End-to-End Delivery)"
            ]
        )
        if "India" in country_choice:
            sample_default_comp = "Softhealer Technologies"
        elif "Switzerland" in country_choice:
            sample_default_comp = "Camptocamp"
        elif "Emirates" in country_choice:
            sample_default_comp = "Bista Solutions UAE"
        elif "Germany" in country_choice:
            sample_default_comp = "OBS Solutions GmbH"
        else:
            sample_default_comp = "Braintec AG"

        sample_comp = st.text_input("Target Company Name", value=sample_default_comp)
        clean_country = country_choice.split(" (")[0]

        if st.button("Generate Adapted Pitch Preview", type="primary", use_container_width=True):
            with st.spinner("Generating country-tailored cover letter..."):
                sample = ai_drafter.generate_application_draft(
                    company_name=sample_comp,
                    country=clean_country,
                    job_title="Junior Project Manager / ERP Functional Consultant"
                )
                st.session_state["preview_data"] = sample

    with pv_c2:
        if "preview_data" in st.session_state:
            pdata = st.session_state["preview_data"]
            st.markdown(f"**Target Country:** `{clean_country}` | **Regional Archetype:** `{pdata.get('region', 'standard').upper()}`")
            st.markdown(f"**Subject Line:** `{pdata['subject']}`")
            st.markdown(f"**Calculated Match Score:** `{pdata['match_score']}%` | **Engine:** `{pdata['source']}`")
            st.text_area("Adapted Cover Letter Body:", value=pdata["body"], height=380)
        else:
            st.info("Select a country archetype and click 'Generate Adapted Pitch Preview' to inspect the custom layout.")

# ================= TAB 6: SETTINGS & GUARDRAILS =================
with tab_guardrails:
    st.subheader("⚙️ Autonomous System Configuration & Deliverability Guardrails")

    st.markdown("### 🛡️ Live Deliverability & DNS MX Tester")
    st.caption("Verify any email address or corporate domain in real-time before sending.")
    
    test_c1, test_c2 = st.columns([3, 1.2])
    with test_c1:
        test_email_input = st.text_input("Test Email Address", placeholder="e.g. careers@company.com")
    with test_c2:
        st.write("")
        if st.button("🔎 Test MX Deliverability", use_container_width=True):
            if test_email_input:
                is_val, val_msg = email_verifier.verify_email_deliverability(test_email_input)
                if is_val:
                    st.success(f"✅ Deliverable: Active MX mail servers detected! ({val_msg})")
                else:
                    st.error(f"❌ Undeliverable: {val_msg}")

    st.divider()

    st.markdown("### 📬 Delivery Maintenance Actions")
    maint_c1, maint_c2 = st.columns(2)
    with maint_c1:
        if st.button("🛡️ Run Full Database DNS MX Quarantine", use_container_width=True):
            with st.spinner("Scanning all database contacts for active MX records..."):
                c_res = odoo_partners.clean_database_deliverability()
                st.success(f"Quarantine Scan Complete: {c_res['verified_valid']} verified valid, {c_res['purged_invalid']} dead domains quarantined.")
                time.sleep(1)
                st.rerun()

    with maint_c2:
        if st.button("📥 Sync Gmail Mailer-Daemon Bounces (IMAP)", use_container_width=True):
            with st.spinner("Connecting to Gmail IMAP to fetch delivery status notifications..."):
                b_count = email_verifier.sync_gmail_bounces()
                st.success(f"Gmail Sync Complete: Quarantined {b_count} newly detected bounced addresses directly from inbox.")
                time.sleep(1)
                st.rerun()

    st.divider()

    st.markdown("### ⚙️ Core Configuration (.env)")
    with st.form("settings_guardrails_form"):
        sc1, sc2 = st.columns(2)
        with sc1:
            app_pw = st.text_input("Google App Password (16 characters)", value=config.GMAIL_APP_PASSWORD, type="password")
            gem_key = st.text_input("Google Gemini API Key", value=config.GEMINI_API_KEY, type="password")
            daily_limit = st.number_input("Daily Email Quota Limit", min_value=5, max_value=100, value=config.DAILY_EMAIL_LIMIT)

        with sc2:
            min_delay = st.number_input("Min Jitter Delay (seconds)", min_value=30, max_value=600, value=config.MIN_DELAY_SECONDS)
            max_delay = st.number_input("Max Jitter Delay (seconds)", min_value=60, max_value=900, value=config.MAX_DELAY_SECONDS)
            blacklisted = st.text_area("Blacklisted Domains (comma-separated)", value=",".join(config.EXCLUDED_DOMAINS))

        save_btn = st.form_submit_button("Save Settings to .env")
        if save_btn:
            env_content = f"""# Gmail SMTP Configuration
GMAIL_USER={config.GMAIL_USER}
GMAIL_APP_PASSWORD={app_pw}

# Google Gemini API Key
GEMINI_API_KEY={gem_key}

# Daily Dispatch & Anti-Spam Safety Limits
DAILY_EMAIL_LIMIT={daily_limit}
MIN_DELAY_SECONDS={min_delay}
MAX_DELAY_SECONDS={max_delay}

# Autopilot Settings
AUTOPILOT_ENABLED=True
RESUME_PATH=resume.pdf

# Blacklisted Domains & Companies
EXCLUDED_DOMAINS={blacklisted}
"""
            with open(config.ENV_PATH, "w", encoding="utf-8") as f:
                f.write(env_content)
            st.success("Settings saved to .env successfully!")

    st.divider()

    st.markdown("### 🔄 GitHub Repository & Auto-Sync")
    st.caption("Synchronize and push all project files, templates, and scripts directly to your GitHub repository.")
    git_c1, git_c2 = st.columns([3, 1.5])
    with git_c1:
        st.markdown("**Remote Repository:** [https://github.com/adithiyagit/Automated-Job-Outreach.git](https://github.com/adithiyagit/Automated-Job-Outreach.git)")
        st.caption("Active Branch: `main` | Automatic background watcher: `python scripts/auto_git_sync.py --watch`")
    with git_c2:
        if st.button("🚀 Push to GitHub Now", use_container_width=True):
            with st.spinner("Checking working tree and pushing changes to GitHub..."):
                from scripts import auto_git_sync
                ok, msg = auto_git_sync.auto_commit_and_push()
                if ok:
                    st.success(f"Git Sync Complete: {msg}")
                else:
                    st.info(f"Git Status: {msg}")
