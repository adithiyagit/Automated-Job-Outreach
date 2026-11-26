"""
Unit Tests for Mailer MIME Builder and Attachment Handling
"""
import unittest
from pathlib import Path
from core import mailer
import config

class TestMailer(unittest.TestCase):
    def test_validate_email_syntax(self):
        self.assertTrue(mailer.validate_email_syntax("careers@bistasolutions.com"))
        self.assertTrue(mailer.validate_email_syntax("adithiyavinu.b@gmail.com"))
        self.assertFalse(mailer.validate_email_syntax("invalid_email"))
        self.assertFalse(mailer.validate_email_syntax("user@"))
        self.assertFalse(mailer.validate_email_syntax("@domain.com"))
        self.assertFalse(mailer.validate_email_syntax(""))

    def test_create_email_message_attachment(self):
        msg = mailer.create_email_message(
            sender="adithiyavinu.b@gmail.com",
            recipient="test@example.com",
            subject="Test Subject",
            body_text="Test Body Text",
            resume_path=config.RESUME_PATH
        )
        self.assertEqual(msg["To"], "test@example.com")
        self.assertIn("Adithiya B Vinu", msg["From"])

        # Check for attachment parts
        payloads = msg.get_payload()
        self.assertGreaterEqual(len(payloads), 2, "Message should contain text body and attachment")

        attachment_part = payloads[1]
        self.assertEqual(attachment_part.get_content_type(), "application/pdf")
        self.assertIn("Resume_Adithiya_B_Vinu.pdf", attachment_part.get("Content-Disposition", ""))

if __name__ == "__main__":
    unittest.main()
