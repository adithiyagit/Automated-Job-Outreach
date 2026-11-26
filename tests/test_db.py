"""
Unit Tests for Database Operations and Safety Limits
"""
import unittest
import tempfile
from pathlib import Path
from core import db
import config

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_automation.db"
        db.init_db(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_partner_and_domain_extraction(self):
        pid = db.add_partner(
            company_name="Test Odoo Partner",
            website="https://www.testodoo.com/en",
            contact_email="careers@testodoo.com",
            country="United Arab Emirates",
            db_path=self.db_path
        )
        self.assertIsNotNone(pid)

        # Adding same domain should be deduplicated
        pid_dup = db.add_partner(
            company_name="Test Odoo Duplicate",
            website="https://testodoo.com/contact",
            contact_email="jobs@testodoo.com",
            db_path=self.db_path
        )
        self.assertIsNone(pid_dup)

    def test_blacklist_exclusion(self):
        # Empire AE should be blocked
        pid = db.add_partner(
            company_name="Empire AE IT Services",
            website="https://empireae.com",
            contact_email="hr@empireae.com",
            db_path=self.db_path
        )
        self.assertIsNone(pid, "Blacklisted domain should not be inserted into partners table")

    def test_daily_stats_tracking(self):
        count_init = db.get_today_sent_count(self.db_path)
        self.assertEqual(count_init, 0)

        db.record_email_sent(self.db_path)
        db.record_email_sent(self.db_path)
        count_after = db.get_today_sent_count(self.db_path)
        self.assertEqual(count_after, 2)

    def test_domain_contacted_check(self):
        self.assertFalse(db.is_domain_contacted("testdomain.com", self.db_path))

        db.record_application(
            recipient_email="hr@testdomain.com",
            company_name="Test Domain Co",
            subject="Test Application",
            body="Test Body",
            domain="testdomain.com",
            status="sent",
            db_path=self.db_path
        )
        self.assertTrue(db.is_domain_contacted("testdomain.com", self.db_path))

    def test_stats_summary_and_uncontacted_count(self):
        stats = db.get_stats_summary(self.db_path)
        self.assertIn("uncontacted_count", stats)
        self.assertIn("daily_limit", stats)
        self.assertEqual(stats["daily_limit"], 50)
        self.assertEqual(stats["uncontacted_count"], 0)

        # Add an uncontacted partner
        db.add_partner(
            company_name="Fresh Partner",
            website="https://freshpartner.com",
            contact_email="careers@freshpartner.com",
            country="India",
            db_path=self.db_path
        )
        stats_updated = db.get_stats_summary(self.db_path)
        self.assertEqual(stats_updated["uncontacted_count"], 1)

if __name__ == "__main__":
    unittest.main()
