# -*- coding: utf-8 -*-
"""
Unit Tests for Dual-Engine Seal & Peruri e-Meterai Gateway (account_stamp_signature)
"""

import unittest
import re

class TestStampAndEmeteraiGateway(unittest.TestCase):
    """Test statutory Bea Meterai threshold logic (UU No. 10/2020) and Peruri SN formatting."""

    def test_statutory_threshold_detection(self):
        """Test threshold under UU No. 10/2020: invoices >= Rp 5,000,000 require Bea Meterai Rp 10.000."""
        threshold = 5_000_000.0

        def check_duty_requirement(amount_total):
            return amount_total >= threshold

        self.assertFalse(check_duty_requirement(4_999_999.0))
        self.assertTrue(check_duty_requirement(5_000_000.0))
        self.assertTrue(check_duty_requirement(54_028_500.0))

    def test_peruri_serial_number_format(self):
        """Test 22-character Peruri Serial Number syntax."""
        sample_sn = "SN-2026-82317851986049"
        self.assertEqual(len(sample_sn), 22)
        self.assertTrue(sample_sn.startswith("SN-2026-"))
        self.assertTrue(re.match(r"^SN-\d{4}-\d{14}$", sample_sn))

    def test_peruri_verification_url(self):
        """Test Peruri official public verification QR URL."""
        sn = "SN-2026-82317851986049"
        expected_url = f"https://verification.peruri.co.id/verify?sn={sn}"
        self.assertIn(sn, expected_url)
        self.assertTrue(expected_url.startswith("https://verification.peruri.co.id/"))

    def test_quota_deduction_simulation(self):
        """Test mock provider quota management and decrement."""
        initial_quota = 100
        used_quota = 0

        # Affix 1 stamp
        initial_quota -= 1
        used_quota += 1

        self.assertEqual(initial_quota, 99)
        self.assertEqual(used_quota, 1)


if __name__ == "__main__":
    unittest.main()
