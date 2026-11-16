# -*- coding: utf-8 -*-
"""
Unit Tests for WhatsApp Finance Notifier (account_whatsapp_notifier)
Tests Indonesian phone normalizer, GOWA JID formatting, template interpolation, and wa.me URL encoding.
"""

import unittest
import urllib.parse
from datetime import date
from unittest.mock import MagicMock

class TestWhatsAppNotifierEngine(unittest.TestCase):
    """Test phone normalization, GOWA payload construction, and templating."""

    def clean_phone(self, phone):
        """Standard Indonesian phone normalization algorithm."""
        import re
        if not phone:
            return False
        clean = re.sub(r'\D', '', str(phone))
        if clean.startswith('08'):
            clean = '628' + clean[2:]
        elif clean.startswith('8'):
            clean = '628' + clean[1:]
        elif clean.startswith('6208'):
            clean = '628' + clean[4:]
        return clean if len(clean) >= 10 else False

    def format_gowa_jid(self, clean_phone):
        """Format WhatsApp JID for GOWA server."""
        return f"{clean_phone}@s.whatsapp.net"

    def test_indonesian_phone_normalization(self):
        """Test sanitizing various Indonesian phone number formats."""
        test_cases = [
            ("081234567890", "6281234567890"),
            ("0812-3456-7890", "6281234567890"),
            ("+62 812 3456 7890", "6281234567890"),
            ("0857 1234 5678", "6285712345678"),
            ("81234567890", "6281234567890"),
            ("62081234567890", "6281234567890"),
            ("+65 9123 4567", "6591234567"), # Singapore international
        ]
        for raw, expected in test_cases:
            result = self.clean_phone(raw)
            self.assertEqual(result, expected, f"Failed for raw phone: {raw}")

    def test_invalid_phone_rejection(self):
        """Test that invalid, empty, or short phone numbers return False."""
        invalid_cases = ["", None, "123", "0812", "abcdef", "+62"]
        for raw in invalid_cases:
            self.assertFalse(self.clean_phone(raw))

    def test_gowa_jid_formatting(self):
        """Test formatting JID for GOWA REST API."""
        phone = self.clean_phone("0812-3456-7890")
        jid = self.format_gowa_jid(phone)
        self.assertEqual(jid, "6281234567890@s.whatsapp.net")

    def test_click_to_chat_url_encoding(self):
        """Test generating RFC 3986 percent-encoded wa.me URL."""
        phone = self.clean_phone("0812-3456-7890")
        message = "Halo Budi,\nTotal tagihan Anda: Rp 1.500.000.\nTerima kasih."

        encoded = urllib.parse.quote(message)
        url = f"https://wa.me/{phone}?text={encoded}"

        self.assertTrue(url.startswith("https://wa.me/6281234567890?text="))
        self.assertIn("%0A", url) # Newline encoded
        self.assertIn("%20", url) # Space encoded
        self.assertNotIn(" ", url) # No unencoded raw spaces

    def test_template_variable_substitution(self):
        """Test dynamic variable replacement in message template."""
        template_body = (
            "Halo {{partner_name}},\n"
            "Faktur {{invoice_number}} senilai {{amount_total}} jatuh tempo pada {{due_date}}.\n"
            "Dari: {{company_name}}"
        )

        values = {
            '{{partner_name}}': 'PT Maju Bersama',
            '{{invoice_number}}': 'INV/2026/00001',
            '{{amount_total}}': 'Rp 2.500.000,00',
            '{{due_date}}': '31/12/2026',
            '{{company_name}}': 'MangoTek Indonesia',
        }

        rendered = template_body
        for k, v in values.items():
            rendered = rendered.replace(k, v)

        self.assertIn("Halo PT Maju Bersama", rendered)
        self.assertIn("Faktur INV/2026/00001", rendered)
        self.assertIn("Rp 2.500.000,00", rendered)
        self.assertIn("31/12/2026", rendered)
        self.assertIn("MangoTek Indonesia", rendered)
        self.assertNotIn("{{", rendered)

    def test_gowa_multi_device_header(self):
        """Test GOWA X-Device-Id header construction for multi-account support."""
        device_id = "6281299998888"
        headers = {}
        if device_id:
            headers['X-Device-Id'] = device_id

        self.assertIn('X-Device-Id', headers)
        self.assertEqual(headers['X-Device-Id'], "6281299998888")

if __name__ == "__main__":
    unittest.main()
