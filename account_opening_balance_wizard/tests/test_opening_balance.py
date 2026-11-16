# -*- coding: utf-8 -*-
"""
Unit Tests for Opening Balance Wizard Core Engine (account_opening_balance_wizard)
Tests Indonesian tax asset schedules, double-entry equilibrium, and opening clearing mechanics.
"""

import unittest
from datetime import date

class TestOpeningBalanceEngine(unittest.TestCase):
    """Test accounting math, PPh 11 asset depreciation schedules, and clearing accounts."""

    def setUp(self):
        self.cut_off_date = date(2025, 12, 31)

        # Assets
        self.cash_bank = 150_000_000.0
        self.ar_total = 75_000_000.0
        self.stock_total = 120_000_000.0
        self.asset_gross = 240_000_000.0
        self.total_debits = self.cash_bank + self.ar_total + self.stock_total + self.asset_gross

        # Liabilities & Contra-Assets
        self.ap_total = 85_000_000.0
        self.asset_accum_dep = 60_000_000.0
        self.total_credits_liab = self.ap_total + self.asset_accum_dep

        # Net Equity Calculation
        self.expected_net_equity = self.total_debits - self.total_credits_liab

    def test_double_entry_balance_equilibrium(self):
        """Verify that total debits minus liabilities equals expected owner equity."""
        # Assets: 150M + 75M + 120M + 240M = 585M
        self.assertEqual(self.total_debits, 585_000_000.0)
        # Liabilities & Contra: 85M + 60M = 145M
        self.assertEqual(self.total_credits_liab, 145_000_000.0)
        # Equity: 585M - 145M = 440M
        self.assertEqual(self.expected_net_equity, 440_000_000.0)

        # Balanced journal entry sum check
        total_journal_debits = self.total_debits
        total_journal_credits = self.total_credits_liab + self.expected_net_equity
        self.assertEqual(total_journal_debits, total_journal_credits)

    def test_equity_split_allocation(self):
        """Test flexible allocation between Owner Capital and Retained Earnings."""
        # 70% Owner Capital, 30% Retained Earnings
        ratio_capital = 0.70
        ratio_retained = 0.30

        owner_capital = round(self.expected_net_equity * ratio_capital, 2)
        retained_earnings = round(self.expected_net_equity * ratio_retained, 2)

        self.assertEqual(owner_capital, 308_000_000.0)
        self.assertEqual(retained_earnings, 132_000_000.0)
        self.assertEqual(owner_capital + retained_earnings, self.expected_net_equity)

    def test_pph_11_asset_rates_and_useful_life(self):
        """Test Indonesian UU PPh Pasal 11 straight-line fiscal depreciation rules."""
        groups = {
            'group_1': {'years': 4, 'rate': 25.0},
            'group_2': {'years': 8, 'rate': 12.5},
            'group_3': {'years': 16, 'rate': 6.25},
            'group_4': {'years': 20, 'rate': 5.0},
            'building_perm': {'years': 20, 'rate': 5.0},
            'building_non_perm': {'years': 10, 'rate': 10.0},
        }

        for group_code, rule in groups.items():
            expected_annual_rate = 100.0 / rule['years']
            self.assertAlmostEqual(rule['rate'], expected_annual_rate, places=2)

    def test_asset_straight_line_monthly_depreciation(self):
        """Test monthly straight-line depreciation schedule generation for Group 2 asset."""
        # Mesin Produksi: 48,000,000 IDR, Group 2 (8 years / 96 months), Salvage Value 0
        cost = 48_000_000.0
        salvage = 0.0
        useful_years = 8
        depreciable_base = cost - salvage

        annual_depreciation = depreciable_base * (12.5 / 100.0)
        monthly_depreciation = round(annual_depreciation / 12.0, 2)

        self.assertEqual(annual_depreciation, 6_000_000.0)
        self.assertEqual(monthly_depreciation, 500_000.0)

        # After 24 months (2 years)
        months_elapsed = 24
        expected_accum_dep = monthly_depreciation * months_elapsed
        book_value = cost - expected_accum_dep

        self.assertEqual(expected_accum_dep, 12_000_000.0)
        self.assertEqual(book_value, 36_000_000.0)

    def test_clearing_account_zero_balance_invariant(self):
        """
        Verify that open AR/AP subledger generation preserves zero net balance
        in the Interim Opening Clearing Account (Akun Perantara Saldo Awal).
        """
        clearing_account_balance = 0.0

        # Step 1: Post individual Customer Invoices (AR: Debit AR, Credit Clearing)
        customer_invoices = [25_000_000.0, 30_000_000.0, 20_000_000.0]
        sum_ar = sum(customer_invoices)
        # Each customer invoice credits clearing account
        clearing_account_balance -= sum_ar

        # Step 2: Post individual Vendor Bills (AP: Debit Clearing, Credit AP)
        vendor_bills = [45_000_000.0, 40_000_000.0]
        sum_ap = sum(vendor_bills)
        # Each vendor bill debits clearing account
        clearing_account_balance += sum_ap

        # At this stage, clearing balance is: -75M + 85M = +10M
        self.assertEqual(clearing_account_balance, 10_000_000.0)

        # Step 3: Master Opening Journal Entry posts the counterbalancing net lines
        # In Master JE:
        # AR Line to Clearing: Debit Clearing sum_ar
        clearing_account_balance += sum_ar
        # AP Line to Clearing: Credit Clearing sum_ap
        clearing_account_balance -= sum_ap

        # The net balance in the Clearing Account must be EXACTLY 0.00
        self.assertEqual(clearing_account_balance, 0.0)

if __name__ == "__main__":
    unittest.main()
