"""
Unit Tests for Kerala Regional Outreach & Fast-Track Targeting
"""
import unittest
from core import ai_drafter, timezone_scheduler, db

class TestKeralaOutreach(unittest.TestCase):

    def test_kerala_region_classification(self):
        """Kerala locations must be categorized into dedicated 'kerala' region."""
        for loc in ["Kerala", "Kochi, Kerala", "Infopark Kochi", "Technopark Trivandrum", "Cyberpark Calicut", "Ernakulam"]:
            self.assertEqual(
                ai_drafter.get_region_category(loc),
                "kerala",
                f"Failed to categorize '{loc}' as 'kerala'"
            )

    def test_kerala_cover_letter_content(self):
        """Kerala tailored pitch must highlight local Kochi presence, MCA from Marian College, and immediate 0-day joining."""
        pitch = ai_drafter.generate_application_draft(
            company_name="ZestyBeanz Technologies",
            country="Kerala",
            job_title="Junior Project Manager / ERP Functional Consultant"
        )
        self.assertIn("ZestyBeanz Technologies", pitch["body"])
        self.assertIn("Kochi, Kerala", pitch["body"])
        self.assertIn("Marian College Kuttikanam", pitch["body"])
        self.assertIn("Immediate", pitch["body"])
        self.assertIn("Infopark Kochi", pitch["body"])
        self.assertEqual(pitch.get("region"), "kerala")
        self.assertIn("Kochi, Kerala", pitch["subject"])

    def test_kerala_timezone_resolution(self):
        """Kerala must resolve to Asia/Kolkata timezone with proper schedule info."""
        info = timezone_scheduler.get_country_schedule_info("Kerala")
        self.assertEqual(info["country"], "Kerala")
        self.assertIn(":", info["local_time_str"])
        self.assertIsInstance(info["is_morning_window"], bool)

    def test_kerala_db_query(self):
        """Querying with country_filter='kerala' must return Kerala partners."""
        leads = db.get_uncontacted_partners_with_emails(limit=20, country_filter="kerala")
        self.assertGreater(len(leads), 0, "No uncontacted Kerala leads found in DB")
        for lead in leads:
            city_and_tier = (lead.get("city", "") + " " + lead.get("partner_tier", "")).lower()
            is_kerala = any(k in city_and_tier for k in ["kerala", "kochi", "trivandrum", "calicut", "ernakulam"])
            self.assertTrue(is_kerala, f"Lead {lead['company_name']} ({lead.get('city')}) is not a Kerala lead")

if __name__ == "__main__":
    unittest.main()
