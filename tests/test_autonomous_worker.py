"""
Unit Tests for Autonomous 24/7 Worker Daemon
"""
import unittest
import time
from core import autonomous_worker

class TestAutonomousDaemon(unittest.TestCase):
    def test_daemon_instance(self):
        daemon = autonomous_worker.get_daemon()
        self.assertIsNotNone(daemon)

        # Verify initial status structure
        status = daemon.get_status()
        self.assertIn("is_running", status)
        self.assertIn("interval_minutes", status)
        self.assertIn("log_count", status)

    def test_daemon_logging(self):
        daemon = autonomous_worker.get_daemon()
        test_msg = "Test autonomous event entry"
        daemon.log(test_msg)

        logs = daemon.get_logs()
        self.assertTrue(any(test_msg in l for l in logs), "Expected test message in daemon logs")

if __name__ == "__main__":
    unittest.main()
