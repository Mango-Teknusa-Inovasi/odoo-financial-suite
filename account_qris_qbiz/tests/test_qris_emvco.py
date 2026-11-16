# -*- coding: utf-8 -*-
"""
Unit Tests for QBiz Dynamic QRIS Core Engine (account_qris_qbiz)
"""

import unittest
from account_qris_qbiz.models.qris_emvco import (
    compute_crc16,
    parse_emvco,
    generate_dynamic_qris,
    DEFAULT_MOCK_STATIC_QRIS,
)

class TestQBizQRISEngine(unittest.TestCase):
    """Test EMVCo QRIS parsing, Tag 54 injection, CCITT-16 CRC recalculation, and unique code logic."""

    def setUp(self):
        self.static_qris = DEFAULT_MOCK_STATIC_QRIS

    def test_crc16_known_vector(self):
        """Test CCITT-16 calculation against known EMVCo test payload."""
        # The payload of DEFAULT_MOCK_STATIC_QRIS before CRC tag is known
        payload_before_crc = self.static_qris[:self.static_qris.find("6304") + 4]
        crc = compute_crc16(payload_before_crc)
        self.assertEqual(crc, "2577")
        self.assertEqual(len(crc), 4)

    def test_emvco_parser_tag_sequence(self):
        """Test parsing of EMVCo TLV string preserving tag sequence."""
        tags = parse_emvco(self.static_qris)
        tag_dict = dict(tags)

        self.assertIn("00", tag_dict)
        self.assertEqual(tag_dict["00"], "01") # Payload Format Indicator
        self.assertIn("01", tag_dict)
        self.assertEqual(tag_dict["01"], "11") # Static QRIS
        self.assertIn("58", tag_dict)
        self.assertEqual(tag_dict["58"], "ID") # Country Code Indonesia
        self.assertIn("53", tag_dict)
        self.assertEqual(tag_dict["53"], "360") # Indonesian Rupiah currency code

    def test_dynamic_qris_tag54_injection(self):
        """Test converting static QRIS to dynamic QRIS with pre-filled Tag 54 nominal."""
        nominal = 75000.0
        dynamic_qris = generate_dynamic_qris(self.static_qris, nominal)

        self.assertTrue(dynamic_qris.startswith("000201010212")) # Tag 01 must be '12' (Dynamic)
        self.assertIn("540575000", dynamic_qris) # Tag 54, length 05, value '75000'
        self.assertIn("5802ID", dynamic_qris) # Tag 58 present

        # Verify Tag 54 precedes Tag 58
        idx_54 = dynamic_qris.find("540575000")
        idx_58 = dynamic_qris.find("5802ID")
        self.assertLess(idx_54, idx_58)

    def test_dynamic_qris_crc_validity(self):
        """Test that generated dynamic QRIS CRC16 checksum mathematically matches."""
        nominal = 125000.0
        dynamic_qris = generate_dynamic_qris(self.static_qris, nominal)

        idx_63 = dynamic_qris.find("6304")
        self.assertNotEqual(idx_63, -1)

        payload_part = dynamic_qris[:idx_63 + 4]
        stored_crc = dynamic_qris[idx_63 + 4:]

        calculated_crc = compute_crc16(payload_part)
        self.assertEqual(stored_crc, calculated_crc)

    def test_qbiz_unique_code_addition(self):
        """Test anti-collision unique code calculation invariant: Total = Base + Unique."""
        base_amount = 50000.0
        unique_code = 3
        total_amount = base_amount + unique_code

        self.assertEqual(total_amount, 50003.0)
        self.assertEqual(int(total_amount), 50003)

        dynamic_qris = generate_dynamic_qris(self.static_qris, total_amount)
        self.assertIn("540550003", dynamic_qris) # Encoded with exact Rp 50.003

    def test_empty_and_invalid_payload_safety(self):
        """Test error handling for empty or malformed input."""
        res_empty = generate_dynamic_qris("", 10000.0)
        self.assertEqual(res_empty, "")

        res_none = generate_dynamic_qris(None, 10000.0)
        self.assertEqual(res_none, "")


if __name__ == "__main__":
    unittest.main()
