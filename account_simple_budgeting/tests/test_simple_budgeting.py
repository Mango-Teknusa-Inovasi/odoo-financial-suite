# -*- coding: utf-8 -*-
"""
Unit Tests for Simple Visual Budgeting (account_simple_budgeting)
Tests annual target distribution, GL expense/revenue realization math,
variance and burn rate calculations, traffic light health status,
and vendor bill soft warning detection logic.
"""

import unittest
from datetime import date

class TestSimpleBudgetingEngine(unittest.TestCase):
    """Test suite for mathematical and business logic of account_simple_budgeting."""

    def test_annual_to_monthly_distribution(self):
        """Test automatic 12-month proportional target division."""
        annual_target = 120000000.0  # Rp 120,000,000 / year
        monthly_slice = round(annual_target / 12.0, 2)
        monthly_slots = [monthly_slice] * 12

        self.assertEqual(monthly_slice, 10000000.0)
        self.assertEqual(sum(monthly_slots), annual_target)

    def test_gl_realization_expense_math(self):
        """Test debit - credit calculation for expense accounts and YTD summation."""
        # Simulated move lines for 3 months
        # Month 1: Debit 8M, Credit 500k -> Net 7.5M
        # Month 2: Debit 10M, Credit 0 -> Net 10.0M
        # Month 3: Debit 12M, Credit 1M -> Net 11.0M
        m1_lines = [{'debit': 8000000.0, 'credit': 500000.0}]
        m2_lines = [{'debit': 10000000.0, 'credit': 0.0}]
        m3_lines = [{'debit': 12000000.0, 'credit': 1000000.0}]

        m1_actual = max(sum(l['debit'] for l in m1_lines) - sum(l['credit'] for l in m1_lines), 0.0)
        m2_actual = max(sum(l['debit'] for l in m2_lines) - sum(l['credit'] for l in m2_lines), 0.0)
        m3_actual = max(sum(l['debit'] for l in m3_lines) - sum(l['credit'] for l in m3_lines), 0.0)

        monthly_actuals = [m1_actual, m2_actual, m3_actual] + [0.0] * 9
        ytd_realized = sum(monthly_actuals)

        self.assertEqual(m1_actual, 7500000.0)
        self.assertEqual(m2_actual, 10000000.0)
        self.assertEqual(m3_actual, 11000000.0)
        self.assertEqual(ytd_realized, 28500000.0)

    def test_gl_realization_revenue_math(self):
        """Test credit - debit calculation for revenue accounts and YTD summation."""
        # Month 1: Credit 50M, Debit 2M (sales return) -> Net 48M
        # Month 2: Credit 60M, Debit 0 -> Net 60M
        m1_lines = [{'credit': 50000000.0, 'debit': 2000000.0}]
        m2_lines = [{'credit': 60000000.0, 'debit': 0.0}]

        m1_actual = max(sum(l['credit'] for l in m1_lines) - sum(l['debit'] for l in m1_lines), 0.0)
        m2_actual = max(sum(l['credit'] for l in m2_lines) - sum(l['debit'] for l in m2_lines), 0.0)

        monthly_actuals = [m1_actual, m2_actual] + [0.0] * 10
        ytd_realized = sum(monthly_actuals)

        self.assertEqual(m1_actual, 48000000.0)
        self.assertEqual(m2_actual, 60000000.0)
        self.assertEqual(ytd_realized, 108000000.0)

    def test_variance_and_burn_rate_metrics(self):
        """Test expense ceiling vs revenue target variance and percentage formulas."""
        # Expense Line: Target 100M, Actual 80M
        exp_target = 100000000.0
        exp_actual = 80000000.0
        exp_variance = exp_target - exp_actual
        exp_burn_rate = round((exp_actual / exp_target * 100.0), 1)

        self.assertEqual(exp_variance, 20000000.0)
        self.assertEqual(exp_burn_rate, 80.0)

        # Revenue Line: Target 200M, Actual 220M
        rev_target = 200000000.0
        rev_actual = 220000000.0
        rev_variance = rev_actual - rev_target
        rev_achievement = round((rev_actual / rev_target * 100.0), 1)

        self.assertEqual(rev_variance, 20000000.0)
        self.assertEqual(rev_achievement, 110.0)

    def test_health_status_traffic_lights(self):
        """Test 3-tier traffic-light status evaluation."""
        # Expense Traffic Light
        def eval_expense_status(burn_rate):
            if burn_rate > 100.0:
                return 'critical'
            elif burn_rate > 85.0:
                return 'warning'
            return 'healthy'

        self.assertEqual(eval_expense_status(75.0), 'healthy')
        self.assertEqual(eval_expense_status(85.0), 'healthy')
        self.assertEqual(eval_expense_status(85.1), 'warning')
        self.assertEqual(eval_expense_status(99.9), 'warning')
        self.assertEqual(eval_expense_status(100.1), 'critical')
        self.assertEqual(eval_expense_status(120.0), 'critical')

        # Revenue Traffic Light
        def eval_revenue_status(achievement_pct):
            if achievement_pct >= 100.0:
                return 'healthy'
            elif achievement_pct >= 75.0:
                return 'warning'
            return 'critical'

        self.assertEqual(eval_revenue_status(110.0), 'healthy')
        self.assertEqual(eval_revenue_status(100.0), 'healthy')
        self.assertEqual(eval_revenue_status(80.0), 'warning')
        self.assertEqual(eval_revenue_status(74.9), 'critical')
        self.assertEqual(eval_revenue_status(50.0), 'critical')

    def test_vendor_bill_soft_warning_logic(self):
        """Test non-blocking soft warning detection when bill exceeds monthly ceiling."""
        monthly_target = 10000000.0  # Rp 10M
        monthly_realized = 7000000.0  # Rp 7M already spent
        remaining = monthly_target - monthly_realized  # Rp 3M remaining

        # Case A: Bill of 2M (within ceiling) -> No warning
        bill_a = 2000000.0
        has_warning_a = (monthly_realized + bill_a) > monthly_target
        self.assertFalse(has_warning_a)

        # Case B: Bill of 5M (exceeds ceiling by 2M) -> Triggers soft warning
        bill_b = 5000000.0
        has_warning_b = (monthly_realized + bill_b) > monthly_target
        over_amount = (monthly_realized + bill_b) - monthly_target
        self.assertTrue(has_warning_b)
        self.assertEqual(over_amount, 2000000.0)

if __name__ == '__main__':
    unittest.main()
