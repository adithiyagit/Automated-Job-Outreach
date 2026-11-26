"""
Central Configuration Module for Global Job Application Automation
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Candidate Credentials & Profile
CANDIDATE_NAME = "Adithiya B Vinu"
CANDIDATE_EMAIL = "adithiyavinu.b@gmail.com"
CANDIDATE_PHONE = "+91 96337 83038"
CANDIDATE_LINKEDIN = "https://linkedin.com/in/adithiya-b-vinu"
GMAIL_USER = os.getenv("GMAIL_USER", CANDIDATE_EMAIL)
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Safety & Anti-Spam Throttling Limits
DAILY_EMAIL_LIMIT = int(os.getenv("DAILY_EMAIL_LIMIT", "50"))
MIN_DELAY_SECONDS = int(os.getenv("MIN_DELAY_SECONDS", "90"))
MAX_DELAY_SECONDS = int(os.getenv("MAX_DELAY_SECONDS", "240"))

# Operational Settings
AUTOPILOT_ENABLED = os.getenv("AUTOPILOT_ENABLED", "True").lower() in ("true", "1", "yes")
RESUME_PATH = BASE_DIR / os.getenv("RESUME_PATH", "resume.pdf")
DATABASE_PATH = DATA_DIR / "automation.db"
LOG_PATH = DATA_DIR / "automation.log"

# Blacklisted domains (past employers, generic email services, etc.)
raw_exclusions = os.getenv("EXCLUDED_DOMAINS", "empireae.com,turqosoft.com,turqosoftsolutions.com")
EXCLUDED_DOMAINS = [d.strip().lower() for d in raw_exclusions.split(",") if d.strip()]

# Target Role Keywords
TARGET_ROLES = [
    "Junior Project Manager",
    "ERP Functional Consultant",
    "Odoo Functional Consultant",
    "Business Analyst",
    "QA & UAT Consultant",
    "Odoo Implementation Specialist",
    "Associate Project Manager"
]

TARGET_MODULES = [
    "CRM", "Sales", "Purchase", "Inventory", "Accounts", "Manufacturing", "HR"
]
