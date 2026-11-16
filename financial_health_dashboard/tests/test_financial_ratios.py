# -*- coding: utf-8 -*-
"""
Unit Tests for Executive Financial Health & Ratio KPI Dashboard (financial_health_dashboard)
"""

import unittest

class TestFinancialRatios(unittest.TestCase):
    """Test financial KPI ratio formulas, liquidity indicators, and composite health scoring."""

    def setUp(self):
        # Demo Company Balance Sheet Snapshot
        self.cash = 0.0
        self.ar = 119_698_500.0
        self.inventory = 9_312_000.0
        self.current_assets = self.cash + self.ar + self.inventory # 129,010,500
        self.fixed_assets = 0.0
        self.total_assets = self.current_assets + self.fixed_assets

        self.current_liabilities = 62_060_000.0 # Trade Payables
        self.long_term_liabilities = 0.0
        self.total_liabilities = self.current_liabilities + self.long_term_liabilities

        self.equity = 66_950_500.0 # Net Profit + Retained Earnings

        # Income Statement
        self.revenue = 129_398_500.0
        self.cogs = 62_060_000.0
        self.gross_profit = self.revenue - self.cogs # 67,338,500
        self.operating_expenses = 388_000.0
        self.net_profit = self.gross_profit - self.operating_expenses # 66,950,500

    def test_current_ratio(self):
        """Test Current Ratio (Current Assets / Current Liabilities). Benchmark: >= 2.0x is Optimal."""
        cr = round(self.current_assets / self.current_liabilities, 2)
        self.assertEqual(cr, 2.08)
        self.assertGreaterEqual(cr, 2.0) # Optimal

    def test_quick_ratio(self):
        """Test Quick Ratio (Acid-Test: (Cash + AR) / Current Liabilities). Benchmark: >= 1.0x."""
        qr = round((self.cash + self.ar) / self.current_liabilities, 2)
        self.assertEqual(qr, 1.93)
        self.assertGreaterEqual(qr, 1.0) # Optimal

    def test_debt_to_equity_ratio(self):
        """Test Debt-to-Equity Ratio (Total Liabilities / Total Equity). Benchmark: <= 1.0x."""
        der = round(self.total_liabilities / self.equity, 2)
        self.assertEqual(der, 0.93)
        self.assertLessEqual(der, 1.0) # Conservative / Optimal

    def test_debt_to_asset_ratio(self):
        """Test Debt-to-Asset Ratio (Total Liabilities / Total Assets). Benchmark: 0.4 - 0.6."""
        dar = round(self.total_liabilities / self.total_assets, 2)
        self.assertEqual(dar, 0.48)
        self.assertTrue(0.4 <= dar <= 0.6) # Moderate

    def test_gross_and_net_profit_margins(self):
        """Test operating margin percentages."""
        gpm = round((self.gross_profit / self.revenue) * 100, 1)
        npm = round((self.net_profit / self.revenue) * 100, 1)

        self.assertEqual(gpm, 52.0)
        self.assertEqual(npm, 51.7)
        self.assertGreaterEqual(gpm, 40.0) # Strong Margin
        self.assertGreaterEqual(npm, 15.0) # Highly Profitable

    def test_net_working_capital_surplus(self):
        """Test Net Working Capital (Current Assets - Current Liabilities)."""
        nwc = self.current_assets - self.current_liabilities
        self.assertEqual(nwc, 66_950_500.0)
        self.assertGreater(nwc, 0) # Positive surplus

    def test_composite_health_score(self):
        """Test composite weighted health score (0 - 100 scale)."""
        score = 0
        # CR >= 2.0 -> 25 pts
        if (self.current_assets / self.current_liabilities) >= 2.0:
            score += 25
        # QR >= 1.0 -> 20 pts
        if ((self.cash + self.ar) / self.current_liabilities) >= 1.0:
            score += 20
        # DER <= 1.0 -> 25 pts
        if (self.total_liabilities / self.equity) <= 1.0:
            score += 25
        # NPM >= 15% -> 26 pts
        if ((self.net_profit / self.revenue) * 100) >= 15.0:
            score += 26

        self.assertEqual(score, 96) # 96 / 100 Excellent


if __name__ == "__main__":
    unittest.main()
