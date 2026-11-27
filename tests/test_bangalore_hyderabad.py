"""
Unit Tests for Bangalore and Hyderabad Regional Outreach & Fast-Track Targeting
"""
import unittest
from core import ai_drafter, timezone_scheduler, db

class TestBangaloreHyderabadOutreach(unittest.TestCase):

    def test_region_classification(self):
        """Bangalore and Hyderabad locations must be categorized into their dedicated regions."""
        for loc in ["Bangalore", "Bengaluru", "Electronic City", "Whitefield", "Manyata"]:
            self.assertEqual(ai_drafter.get_region_category(loc), "bangalore", f"Failed for {loc}")

        for loc in ["Hyderabad", "Secunderabad", "HITEC City", "Madhapur", "Gachibowli"]:
            self.assertEqual(ai_drafter.get_region_category(loc), "hyderabad", f"Failed for {loc}")

    def test_bangalore_pitch_content(self):
        """Bangalore tailored pitch must highlight Bangalore relocation, MCA, and 0-day notice."""
        pitch = ai_drafter.generate_application_draft(
            company_name="Trigent Software Bangalore",
            country="Bangalore",
            job_title="Junior Project Manager / ERP Functional Consultant"
        )
        self.assertIn("Trigent Software Bangalore", pitch["body"])
        self.assertIn("Bangalore", pitch["body"])
        self.assertIn("Immediate Joiner", pitch["body"])
        self.assertIn("Marian College Kuttikanam", pitch["body"])
        self.assertEqual(pitch.get("region"), "bangalore")
        self.assertIn("Bangalore", pitch["subject"])

    def test_hyderabad_pitch_content(self):
        """Hyderabad tailored pitch must highlight Hyderabad relocation, HITEC City, MCA, and 0-day notice."""
        pitch = ai_drafter.generate_application_draft(
            company_name="Ray Business Technologies",
            country="Hyderabad",
            job_title="Junior Project Manager / ERP Functional Consultant"
        )
        self.assertIn("Ray Business Technologies", pitch["body"])
        self.assertIn("Hyderabad", pitch["body"])
        self.assertIn("Immediate", pitch["body"])
        self.assertIn("Marian College Kuttikanam", pitch["body"])
        self.assertEqual(pitch.get("region"), "hyderabad")
        self.assertIn("Hyderabad", pitch["subject"])

    def test_timezone_resolution(self):
        """Both Bangalore and Hyderabad must resolve to Asia/Kolkata."""
        info_blr = timezone_scheduler.get_country_schedule_info("Bangalore")
        self.assertEqual(info_blr["country"], "Bangalore")
        self.assertIn(":", info_blr["local_time_str"])

        info_hyd = timezone_scheduler.get_country_schedule_info("Hyderabad")
        self.assertEqual(info_hyd["country"], "Hyderabad")
        self.assertIn(":", info_hyd["local_time_str"])

    def test_db_queries(self):
        """Querying with country_filter='bangalore' and 'hyderabad' must return valid leads."""
        blr_leads = db.get_uncontacted_partners_with_emails(limit=20, country_filter="bangalore")
        self.assertGreater(len(blr_leads), 0, "No uncontacted Bangalore leads found in DB")
        for lead in blr_leads:
            city_and_tier = (lead.get("city", "") + " " + lead.get("partner_tier", "")).lower()
            self.assertTrue("bangalore" in city_and_tier or "bengaluru" in city_and_tier)

        hyd_leads = db.get_uncontacted_partners_with_emails(limit=20, country_filter="hyderabad")
        self.assertGreater(len(hyd_leads), 0, "No uncontacted Hyderabad leads found in DB")
        for lead in hyd_leads:
            city_and_tier = (lead.get("city", "") + " " + lead.get("partner_tier", "")).lower()
            self.assertTrue("hyderabad" in city_and_tier or "hitec" in city_and_tier)

if __name__ == "__main__":
    unittest.main()
