"""
Unit Tests for Deliverability Verifier, Timezone Scheduler, and Regional Templates
"""
import unittest
from core import email_verifier, timezone_scheduler, ai_drafter

class TestVerifierAndTimezone(unittest.TestCase):
    def test_email_verifier_valid_mx(self):
        # Gmail has active MX
        valid, reason = email_verifier.verify_email_deliverability("adithiyavinu.b@gmail.com")
        self.assertTrue(valid, f"Expected gmail.com to have valid MX: {reason}")

    def test_email_verifier_dead_domain(self):
        # Fake nonexistent domain has no MX
        valid, reason = email_verifier.verify_email_deliverability("hr@nonexistent-fake-domain-999.xyz")
        self.assertFalse(valid, "Expected fake domain to fail MX check")
        self.assertIn("no active MX", reason)

    def test_email_verifier_blocked_prefix(self):
        valid, reason = email_verifier.verify_email_deliverability("noreply@gmail.com")
        self.assertFalse(valid, "Expected noreply@ to be blocked")

    def test_email_verifier_known_bounce(self):
        valid, reason = email_verifier.verify_email_deliverability("hr@techultrasolutions.com")
        self.assertFalse(valid, "Expected known bounced address to be blocked")
        self.assertIn("quarantined", reason.lower())

    def test_email_verifier_aggregator_domain(self):
        valid, reason = email_verifier.verify_email_deliverability("hi@jobicy.com")
        self.assertFalse(valid, "Expected aggregator domain to be blocked")

    def test_timezone_resolution(self):
        uae_tz = timezone_scheduler.resolve_country_timezone("United Arab Emirates")
        self.assertEqual(str(uae_tz), "Asia/Dubai")

        swiss_tz = timezone_scheduler.resolve_country_timezone("Switzerland")
        self.assertEqual(str(swiss_tz), "Europe/Zurich")

        uk_tz = timezone_scheduler.resolve_country_timezone("United Kingdom")
        self.assertEqual(str(uk_tz), "Europe/London")

    def test_regional_template_variation(self):
        # Middle East template
        draft_me = ai_drafter.generate_regional_template("Plennix Dubai", country="United Arab Emirates")
        self.assertEqual(draft_me["region"], "middle_east")
        self.assertIn("on-ground and functional experience", draft_me["body"])
        self.assertIn("Indian national", draft_me["body"])

        # DACH Europe (Switzerland) template
        draft_dach = ai_drafter.generate_regional_template("Camptocamp", country="Switzerland")
        self.assertEqual(draft_dach["region"], "dach_europe")
        self.assertIn("Functional Specification & Gap Analysis", draft_dach["body"])
        self.assertIn("curriculum vitae", draft_dach["body"])

        # North America template
        draft_na = ai_drafter.generate_regional_template("Open Source Integrators", country="United States")
        self.assertEqual(draft_na["region"], "north_america")
        self.assertIn("Hi Hiring Team", draft_na["body"])

if __name__ == "__main__":
    unittest.main()
