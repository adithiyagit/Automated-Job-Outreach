"""
Unit Tests for AI Drafting & Smart Fallback Templates
"""
import unittest
from core import ai_drafter, candidate_profile

class TestAIDrafter(unittest.TestCase):
    def test_fallback_draft_structure(self):
        draft = ai_drafter.generate_fallback_draft(
            company_name="Azkatech Odoo Experts",
            country="United Arab Emirates",
            job_title="Junior Project Manager / ERP Functional Consultant"
        )
        self.assertIn("subject", draft)
        self.assertIn("body", draft)
        self.assertIn("match_score", draft)

        # Verify subject line contains candidate name and clean application title
        self.assertIn("Adithiya B Vinu", draft["subject"])
        self.assertIn("Application:", draft["subject"])
        self.assertNotIn("(Live 9-Store Odoo Rollout & UAT Experience)", draft["subject"])

        # Verify body contains critical rollout metrics and modules
        self.assertIn("Azkatech Odoo Experts", draft["body"])
        self.assertIn("store locations", draft["body"])
        self.assertIn("CRM, Sales, Purchase, Inventory, Accounts, Manufacturing, and HR", draft["body"])
        self.assertIn("BRD/FRD-aligned SOPs", draft["body"])
        self.assertIn("UAT", draft["body"])

    def test_candidate_summary_generation(self):
        text = candidate_profile.get_candidate_summary_text()
        self.assertIn("Adithiya B Vinu", text)
        self.assertIn("adithiyavinu.b@gmail.com", text)
        self.assertIn("Empire AE IT Services", text)
        self.assertIn("Jewellery Retail ERP Implementation", text)

if __name__ == "__main__":
    unittest.main()
