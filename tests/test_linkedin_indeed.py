"""
Unit Tests for LinkedIn & Indeed Radar Integration Engines
"""
import unittest
from pathlib import Path
from core import linkedin_engine, indeed_engine, db

class TestLinkedInIndeed(unittest.TestCase):

    def test_connection_note_length_under_300_chars(self):
        """Free LinkedIn connection notes MUST be strictly <= 300 characters."""
        test_cases = [
            ("Alpha Retail Corp", "Priya Sharma", "Odoo Functional Consultant", "high_impact"),
            ("Super Long Global Enterprise Technologies International FZ-LLC", "Alexander Von Humboldt", "Junior Project Manager / ERP Functional Consultant", "high_impact"),
            ("Swiss Cloud Consulting AG", "Markus", "Business Analyst", "role_focused"),
            ("Gulf ERP Systems Dubai", "Sarah", "Odoo Implementation Specialist", "recruiter_inquiry"),
            ("Generic Tech Ltd", "", "", "default")
        ]

        for company, recruiter, role, style in test_cases:
            note = linkedin_engine.generate_connection_note(
                company_name=company,
                recruiter_name=recruiter,
                target_role=role,
                style=style
            )
            self.assertLessEqual(
                len(note), 300,
                f"Note exceeded 300 chars ({len(note)} chars) for {company} - '{note}'"
            )
            self.assertTrue(len(note) > 50, f"Note too short: '{note}'")

    def test_connection_note_highlights_profile(self):
        """Note must mention 9-store rollout, Odoo, or immediate availability."""
        note = linkedin_engine.generate_connection_note(
            company_name="Tech Solutions",
            recruiter_name="Rahul",
            style="high_impact"
        )
        self.assertIn("9-store", note)
        self.assertIn("Odoo", note)
        self.assertIn("Rahul", note)
        self.assertLessEqual(len(note), 300)

    def test_inmail_pitch_structure(self):
        """InMail pitch must have subject, body, and contact information."""
        pitch = linkedin_engine.generate_inmail_pitch(
            company_name="Apex ERP Systems",
            recruiter_name="Jennifer",
            target_role="Junior Project Manager",
            country="Germany"
        )
        self.assertIn("subject", pitch)
        self.assertIn("body", pitch)
        self.assertIn("Apex ERP Systems", pitch["body"])
        self.assertIn("Adithiya B Vinu", pitch["body"])
        self.assertIn("adithiyavinu.b@gmail.com", pitch["body"])
        self.assertIn("9 store branches", pitch["body"])
        self.assertTrue(100 <= pitch["word_count"] <= 260)

    def test_recruiter_xray_urls(self):
        """Google X-Ray and LinkedIn People search URLs must be properly formed."""
        urls = linkedin_engine.build_recruiter_search_urls(
            company_name="Kardex Systems",
            country="Switzerland",
            role_focus="Odoo"
        )
        self.assertIn("google_xray_url", urls)
        self.assertIn("linkedin_people_url", urls)
        self.assertIn("google.com/search?q=", urls["google_xray_url"])
        self.assertIn("site%3Alinkedin.com%2Fin%2F", urls["google_xray_url"])
        self.assertIn("Kardex+Systems", urls["google_xray_url"])
        self.assertIn("linkedin.com/search/results/people/", urls["linkedin_people_url"])

    def test_indeed_url_country_mapping(self):
        """Indeed search URLs must resolve to localized country domains."""
        url_in = indeed_engine.get_indeed_search_url("Odoo", "India", "Bangalore")
        self.assertTrue(url_in.startswith("https://in.indeed.com/jobs?q=Odoo&l=Bangalore"))

        url_ae = indeed_engine.get_indeed_search_url("ERP", "United Arab Emirates", "Dubai")
        self.assertTrue(url_ae.startswith("https://ae.indeed.com/jobs?q=ERP&l=Dubai"))

        url_de = indeed_engine.get_indeed_search_url("Odoo", "Germany", "")
        self.assertTrue(url_de.startswith("https://de.indeed.com/jobs?q=Odoo"))

        url_ch = indeed_engine.get_indeed_search_url("Odoo", "Switzerland", "")
        self.assertTrue(url_ch.startswith("https://ch.indeed.com/jobs?q=Odoo"))

        url_uk = indeed_engine.get_indeed_search_url("Odoo", "UK", "London")
        self.assertTrue(url_uk.startswith("https://uk.indeed.com/jobs?q=Odoo&l=London"))

    def test_queue_company_to_outreach(self):
        """Queuing a company into outreach pipeline must add to database."""
        test_db = Path("data/test_radar_automation.db")
        if test_db.exists():
            test_db.unlink()
        db.init_db(test_db)

        # Patch db.add_partner to use test_db for this test
        orig_add = db.add_partner
        try:
            db.add_partner = lambda **kwargs: orig_add(**{**kwargs, "db_path": test_db})
            
            res = indeed_engine.queue_company_to_outreach(
                company_name="Apex ERP Swiss AG",
                website="https://apex-erp-swiss-example.ch",
                country="Switzerland",
                job_title="Odoo Consultant"
            )
            self.assertTrue(res["success"])
            self.assertIsNotNone(res["partner_id"])

            # Deduplication check
            res_dup = indeed_engine.queue_company_to_outreach(
                company_name="Apex ERP Swiss AG",
                website="https://apex-erp-swiss-example.ch",
                country="Switzerland",
                job_title="Odoo Consultant"
            )
            self.assertFalse(res_dup["success"])
        finally:
            db.add_partner = orig_add
            if test_db.exists():
                test_db.unlink()

if __name__ == "__main__":
    unittest.main()
