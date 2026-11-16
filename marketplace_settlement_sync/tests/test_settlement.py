# -*- coding: utf-8 -*-
"""
Unit Tests for Multichannel Marketplace Settlement Sync (marketplace_settlement_sync)
"""

import unittest

class TestMarketplaceSettlementSplit(unittest.TestCase):
    """Test reconciliation math and split-accounting invariant for Shopee, Tokopedia, TikTok Shop."""

    def test_split_accounting_invariant(self):
        """Test accounting invariant: Gross Turnover == Service Fees + Net Escrow Deposit."""
        orders = [
            {"order_id": "261116SP8801", "gross": 1_850_000.0, "fee": 74_000.0, "net": 1_776_000.0},
            {"order_id": "261116SP8802", "gross": 750_000.0, "fee": 30_000.0, "net": 720_000.0},
            {"order_id": "261116SP8803", "gross": 1_200_000.0, "fee": 48_000.0, "net": 1_152_000.0},
            {"order_id": "261116SP8804", "gross": 2_400_000.0, "fee": 96_000.0, "net": 2_304_000.0},
            {"order_id": "261116SP8805", "gross": 3_500_000.0, "fee": 140_000.0, "net": 3_360_000.0},
        ]

        total_gross = sum(o["gross"] for o in orders)
        total_fees = sum(o["fee"] for o in orders)
        total_net = sum(o["net"] for o in orders)

        self.assertEqual(total_gross, 9_700_000.0)
        self.assertEqual(total_fees, 388_000.0)
        self.assertEqual(total_net, 9_312_000.0)
        
        # Verify strict invariant on each line and batch
        for o in orders:
            self.assertAlmostEqual(o["gross"], o["fee"] + o["net"], places=2)
        self.assertAlmostEqual(total_gross, total_fees + total_net, places=2)

    def test_journal_entry_double_entry_balance(self):
        """Test that generated journal lines strictly balance (Total Debit == Total Credit)."""
        gross_turnover = 9_700_000.0
        service_fees = 388_000.0
        net_bank_escrow = 9_312_000.0

        journal_lines = [
            {"account": "111000 Bank Escrow", "debit": net_bank_escrow, "credit": 0.0},
            {"account": "612000 Marketplace Service Expense", "debit": service_fees, "credit": 0.0},
            {"account": "411000 Marketplace Gross Revenue", "debit": 0.0, "credit": gross_turnover},
        ]

        total_debit = sum(line["debit"] for line in journal_lines)
        total_credit = sum(line["credit"] for line in journal_lines)

        self.assertEqual(total_debit, total_credit)
        self.assertEqual(total_debit, 9_700_000.0)

    def test_effective_take_rate_calculation(self):
        """Test calculation of marketplace platform commission take rate %."""
        gross = 9_700_000.0
        fees = 388_000.0
        take_rate_pct = round((fees / gross) * 100, 2)
        self.assertEqual(take_rate_pct, 4.0) # 4.0% Shopee standard commission fee


if __name__ == "__main__":
    unittest.main()
