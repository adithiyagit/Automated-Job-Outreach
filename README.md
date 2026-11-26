# 🚀 Global Odoo & ERP Job Outreach Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![Deliverability Guard](https://img.shields.io/badge/DNS%20MX-Enforced%20(0%25%20Bounce)-success.svg)]()
[![Theme](https://img.shields.io/badge/UI-High--Contrast%20Dark%20Mode-0B0F19.svg)]()

An autonomous, 24/7 intelligent cold outreach and job application system built for **Adithiya B Vinu** to target corporate Odoo implementation partners and ERP openings (Junior Project Manager, ERP Functional Consultant, Business Analyst, QA & UAT).

Repository: [https://github.com/adithiyagit/Automated-Job-Outreach.git](https://github.com/adithiyagit/Automated-Job-Outreach.git)

---

## 🌟 Key Capabilities

1. **24/7 Zero-Click Background Autopilot**:
   - Fully automated daemon continuously scouting for new postings, verifying mail servers, and applying without requiring any manual button clicks.
   - Built-in anti-duplicate lock prevents double-sends across all background cycles.

2. **Ultra-High-Contrast Native Dark Mode Dashboard**:
   - Executive mission control interface on `http://127.0.0.1:8501`.
   - Real-time live activity terminal streaming events with vivid color-coding (`[DISPATCH]`, `[BOUNCE-GUARD]`, `[REPLENISH]`, `[SLEEP]`).
   - Global HR Radar Ribbon displaying live world clocks and morning prime windows for 7 key regions (India, Switzerland, Germany, UAE, Saudi Arabia, UK, US).

3. **0% Bounce Guarantee & DNS MX Guard**:
   - Pre-send DNS MX lookup verifies recipient mail exchangers before any email is dispatched.
   - Automatic Gmail IMAP failure scanner parses Mailer-Daemon bounce notifications and isolates dead addresses into `bounced_emails.json`.
   - Strict deliverability accounting: bounced emails are quarantined as `status = 'bounced'` and automatically excluded from daily sent quotas.

4. **Multi-Country Outreach & Dynamic 1-Click Dispatch**:
   - Curated directory of 90+ verified corporate consultancies across Switzerland (DACH), Germany, UAE (Dubai), Saudi Arabia, Belgium, Netherlands, UK, US, Canada, Australia, Singapore, and India.
   - Intelligent round-robin interleaving ensures balanced multi-country delivery.
   - **1-Click Direct Country Dispatch**: Target any specific destination country on demand.

5. **AI Resume & Regional Pitch Tailoring**:
   - Customizes tone, cultural expectations, and value propositions by destination country.
   - Highlights candidate's live 9-store Odoo rollout across 6 core modules (CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, HR), BRD/FRD SOP authoring, UAT sign-offs, and immediate 0-day notice period.

6. **Automated Git Sync**:
   - Built-in watcher script (`scripts/auto_git_sync.py`) and PowerShell script (`scripts/git_sync.ps1`) to automatically stage, commit, and push all codebase improvements.

---

## 🛠️ Quick Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/adithiyagit/Automated-Job-Outreach.git
cd Automated-Job-Outreach
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `.env`
Create a `.env` file from `.env.example`:
```env
# Gmail SMTP & IMAP Configuration
GMAIL_USER=adithiyavinu.b@gmail.com
GMAIL_APP_PASSWORD=your_16_char_google_app_password

# Google Gemini API Key (https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# Safety & Anti-Spam Quotas
DAILY_EMAIL_LIMIT=50
MIN_DELAY_SECONDS=90
MAX_DELAY_SECONDS=240

# Autopilot Settings
AUTOPILOT_ENABLED=True
RESUME_PATH=resume.pdf

# Blacklisted Domains (past employers, generic aggregators)
EXCLUDED_DOMAINS=empireae.com,turqosoft.com,turqosoftsolutions.com
```

---

## 🖥️ Launching the Mission Control Dashboard

```bash
streamlit run app.py
```
Open **`http://127.0.0.1:8501`** in your browser.

* **Top Action Bar:** Click `🔄 Refresh View`, trigger `⚡ Run Instant Cycle`, or target any country directly with `⚡ Apply to [Country] Now`.
* **Tab 1: 📊 Mission Control & Analytics:** Visual outreach funnel, country distribution charts, and live monospace activity console.
* **Tab 2: 🏢 Lead Pipeline CRM:** Search leads, filter by country/status, export CSV, or add custom targets with real-time MX validation.
* **Tab 3: 📜 Sent Applications CRM:** Audit history of all delivered and quarantined emails, inspect rendered pitch bodies, and export CSV.
* **Tab 4: 🔥 Live Job Feed & Scout:** Real-time job boards crawler (RemoteOK, Remotive, Jobicy).
* **Tab 5: 📄 AI Pitch Studio:** Compare regional pitch archetypes and preview tailored cover letters.
* **Tab 6: ⚙️ Safety & Guardrails:** Live DNS MX tester, manual Gmail bounce sync, and daily limit controls.

---

## 🔄 Automated Git Commit & Push

To commit and push all current project changes with an automated timestamp:
```bash
python scripts/auto_git_sync.py
```
Or on Windows PowerShell:
```powershell
.\scripts\git_sync.ps1
```

To run continuous background auto-sync (monitors and auto-commits changes every 60 seconds):
```bash
python scripts/auto_git_sync.py --watch --interval 60
```

---

## 🧪 Testing

Run the full automated test suite (18 unit tests):
```bash
python -m unittest discover -s tests -v
```

---

## 📁 Repository Structure

```
Automated-Job-Outreach/
├── app.py                      # Next-Gen Streamlit Dark Mode Dashboard
├── cli.py                      # Headless CLI Runner
├── config.py                   # Central Configuration & Safety Limits
├── resume.pdf                  # Attached Candidate Resume PDF
├── .env.example                # Template for Environment Credentials
├── .gitignore                  # Security Rules (protects .env and database)
├── core/
│   ├── ai_drafter.py           # Country-Specific AI Pitch Generation
│   ├── autonomous_worker.py    # 24/7 Zero-Click Background Worker
│   ├── candidate_profile.py    # Structured Candidate Metadata & Experience
│   ├── db.py                   # SQLite WAL Database Manager & Migrations
│   ├── email_finder.py         # Website Scraping & Email Extractor
│   ├── email_verifier.py       # DNS MX Verifier & Gmail IMAP Bounce Quarantine
│   ├── mailer.py               # Gmail SMTP Dispatcher & Anti-Spam Throttler
│   └── timezone_scheduler.py   # Global HR Working Hours & Round-Robin Logic
├── scrapers/
│   ├── job_boards.py           # RemoteOK, Remotive & Jobicy Job Feed Crawler
│   └── odoo_partners.py        # 100% MX-Verified Partner Directory & Auto-Replenishment
├── scripts/
│   ├── auto_git_sync.py        # Automated Git Watcher & Commit Utility
│   └── git_sync.ps1            # Windows PowerShell 1-Click Sync
└── tests/                      # Comprehensive Unit Test Suite
```

---

## 🛡️ License
Private project for personal job search automation.
