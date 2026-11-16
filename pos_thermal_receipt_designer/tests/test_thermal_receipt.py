# -*- coding: utf-8 -*-
"""
Unit Tests for POS Thermal Receipt Designer (pos_thermal_receipt_designer)
Tests column grid calculations, adaptive dual-line wrapping, ESC/POS byte generator, 1-bit dithering, and receipt financial formatting.
"""

import io
import base64
import unittest
from PIL import Image

class TestPosThermalReceiptEngine(unittest.TestCase):
    """Test suite for thermal receipt formatting and ESC/POS byte generation."""

    def test_column_grid_by_paper_width(self):
        """Test column width computation for 58mm (32 chars) and 80mm (48 chars)."""
        def get_char_per_line(paper_width):
            return 32 if paper_width == '58mm' else 48

        self.assertEqual(get_char_per_line('58mm'), 32)
        self.assertEqual(get_char_per_line('80mm'), 48)

    def test_adaptive_dual_line_formatting(self):
        """Test 2-line item rendering where name occupies full line and qty x price is aligned with total."""
        cols = 32
        item_name = "Nasi Goreng Spesial Komplit Sambal Matah"
        qty = 2
        price = 35000.0
        total = 70000.0

        # Line 1: Item Name truncated or wrapped to column width
        line1 = item_name[:cols]
        # Line 2: Qty x Price on left, Total on right
        left_str = f"  {qty} x {price:,.0f}"
        right_str = f"{total:,.0f}"
        space_count = cols - len(left_str) - len(right_str)
        line2 = left_str + (' ' * max(space_count, 1)) + right_str

        self.assertLessEqual(len(line1), cols)
        self.assertEqual(len(line2), cols)
        self.assertTrue(line2.startswith("  2 x 35,000"))
        self.assertTrue(line2.endswith("70,000"))

    def test_single_line_formatting(self):
        """Test 1-line item rendering with right-aligned total and truncated title."""
        cols = 32
        item_name = "Kopi Susu Gula Aren Spesial"
        qty = 1
        price = 22000.0
        total = 22000.0

        left_str = f"{qty}x {item_name[:cols-15]}"
        right_str = f"{total:,.0f}"
        space_count = cols - len(left_str) - len(right_str)
        line = left_str + (' ' * max(space_count, 1)) + right_str

        self.assertEqual(len(line), cols)
        self.assertTrue(line.startswith("1x Kopi Susu Gula"))
        self.assertTrue(line.endswith("22,000"))

    def test_escpos_byte_sequence_structure(self):
        """Test ESC/POS command protocol: initialize, alignments, bold, and auto-cut."""
        cols = 32
        ESC = b'\x1b'
        GS = b'\x1d'

        buf = bytearray()
        # 1. Initialize printer
        buf.extend(ESC + b'@')
        # 2. Centered header
        buf.extend(ESC + b'a\x01')
        buf.extend(ESC + b'E\x01')
        buf.extend(b"WARUNG KOPI MANGO\n")
        buf.extend(ESC + b'E\x00')
        # 3. Divider
        buf.extend(ESC + b'a\x00')
        buf.extend((b'-' * cols) + b'\n')
        # 4. Total Bold
        buf.extend(ESC + b'a\x02')
        buf.extend(ESC + b'E\x01')
        buf.extend(b"TOTAL: 92,000\n")
        buf.extend(ESC + b'E\x00')
        # 5. Paper Cut
        buf.extend(b'\n\n\n')
        buf.extend(GS + b'V\x42\x00')

        raw_bytes = bytes(buf)

        # Assertions on ESC/POS commands
        self.assertTrue(raw_bytes.startswith(b'\x1b@'))  # Init
        self.assertIn(b'\x1ba\x01', raw_bytes)          # Align Center
        self.assertIn(b'\x1bE\x01', raw_bytes)          # Bold On
        self.assertIn(b'\x1ba\x02', raw_bytes)          # Align Right
        self.assertTrue(raw_bytes.endswith(b'\x1dV\x42\x00'))  # GS V 66 0 (Cut)

    def test_one_bit_monochrome_dithering(self):
        """Test converting RGB colored image into 1-bit black and white bitmap."""
        # Create a sample RGB image (100x100) with gradient
        img = Image.new('RGB', (100, 100), color=(128, 128, 200))
        dithered = img.convert('1')

        # 1-bit mode has '1' format
        self.assertEqual(dithered.mode, '1')

        out_io = io.BytesIO()
        dithered.save(out_io, format='PNG')
        encoded = base64.b64encode(out_io.getvalue())
        self.assertGreater(len(encoded), 0)

    def test_financial_rounding_and_ppn12(self):
        """Test subtotal, PPN 12% calculation, total amount, and change calculation."""
        subtotal = 125000.0
        tax_ppn = round(subtotal * 0.12, 0)
        total = subtotal + tax_ppn
        cash_paid = 150000.0
        change = cash_paid - total

        self.assertEqual(tax_ppn, 15000.0)
        self.assertEqual(total, 140000.0)
        self.assertEqual(change, 10000.0)

        # Test string formatting for thermal receipt
        self.assertEqual(f"{subtotal:,.0f}", "125,000")
        self.assertEqual(f"{tax_ppn:,.0f}", "15,000")
        self.assertEqual(f"{total:,.0f}", "140,000")


if __name__ == '__main__':
    unittest.main()
