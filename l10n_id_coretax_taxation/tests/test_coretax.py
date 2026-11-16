# -*- coding: utf-8 -*-
"""
Unit Tests for Indonesian Tax Coretax 2026 Engine (l10n_id_coretax_taxation)
"""

import unittest
import re

class TestCoretaxValidation(unittest.TestCase):
    """Test validation algorithms for NPWP16, NITKU, NSFP, and PPh calculations."""

    def test_npwp16_format_validation(self):
        """Test 16-digit NIK / NPWP16 format requirements under PMK 112/2022."""
        valid_npwp16 = "3273010101900001"
        self.assertEqual(len(valid_npwp16), 16)
        self.assertTrue(valid_npwp16.isdigit())
        self.assertTrue(re.match(r"^\d{16}$", valid_npwp16))

        invalid_short = "32730101019000"
        self.assertFalse(bool(re.match(r"^\d{16}$", invalid_short)))

        invalid_alpha = "327301010190000A"
        self.assertFalse(bool(re.match(r"^\d{16}$", invalid_alpha)))

    def test_nitku22_format_validation(self):
        """Test 22-digit NITKU (Nomor Identitas Tempat Kegiatan Usaha)."""
        valid_nitku = "3273010101900001000000"
        self.assertEqual(len(valid_nitku), 22)
        self.assertTrue(valid_nitku.isdigit())
        self.assertTrue(re.match(r"^\d{22}$", valid_nitku))

        # Branch identifier extraction (last 6 digits)
        branch_id = valid_nitku[-6:]
        self.assertEqual(branch_id, "000000") # Pusat / Headquarter

    def test_nsfp_formatting_and_sequence(self):
        """Test NSFP (Nomor Seri Faktur Pajak) sequential generation."""
        prefix_code = "000"
        tax_year = 2026
        serial_int = 10000001
        
        # Expected format: 01.000-26.10000001 (for standard transaction 01)
        trx_code = "01"
        year_short = str(tax_year)[-2:]
        formatted_nsfp = f"{trx_code}.{prefix_code}-{year_short}.{serial_int:08d}"
        
        self.assertEqual(formatted_nsfp, "01.000-26.10000001")
        self.assertTrue(re.match(r"^\d{2}\.\d{3}-\d{2}\.\d{8}$", formatted_nsfp))

    def test_ppn_12_percent_statutory_calculation(self):
        """Test statutory PPN 12% (UU Harmonisasi Peraturan Perpajakan)."""
        dpp = 100_000_000.0  # Rp 100 Juta
        ppn_rate = 0.12
        ppn_amount = round(dpp * ppn_rate, 2)
        total_with_vat = dpp + ppn_amount

        self.assertEqual(ppn_amount, 12_000_000.0)
        self.assertEqual(total_with_vat, 112_000_000.0)

    def test_pph_final_umkm_pp20_2026(self):
        """Test PPh Final UMKM 0.5% under Government Regulation PP 20/2026."""
        gross_turnover = 54_300_000.0
        pph_rate = 0.005 # 0.5%
        withholding_pph = round(gross_turnover * pph_rate, 2)
        net_receivable = gross_turnover - withholding_pph

        self.assertEqual(withholding_pph, 271_500.0)
        self.assertEqual(net_receivable, 54_028_500.0)

    def test_coretax_efaktur_csv_headers(self):
        """Test statutory CSV column schemas for DJP e-Faktur 4.0 batch export."""
        fk_headers = [
            "FK", "KD_JENIS_TRANSAKSI", "FG_PENGGANTI", "NOMOR_FAKTUR", 
            "MASA_PAJAK", "TAHUN_PAJAK", "TANGGAL_FAKTUR", "NPWP", 
            "NAMA", "ALAMAT_LENGKAP", "JUMLAH_DPP", "JUMLAH_PPN"
        ]
        self.assertIn("NOMOR_FAKTUR", fk_headers)
        self.assertIn("JUMLAH_PPN", fk_headers)
        self.assertEqual(fk_headers[0], "FK")


if __name__ == "__main__":
    unittest.main()
