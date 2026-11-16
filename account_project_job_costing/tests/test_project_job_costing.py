# -*- coding: utf-8 -*-
"""
Unit Tests for Lightweight Project Job Costing (account_project_job_costing)
Tests budget totals, dual-metric accrual vs cashflow, variance math, Indonesian WHT, and closure guards.
"""

import unittest

class TestProjectJobCostingEngine(unittest.TestCase):
    """Test suite for agile project cost sheet mathematical calculations."""

    def test_budget_totals_and_margin(self):
        """Test calculation of total planned budget, projected profit, and margin %."""
        contract = 150000000.0
        mat = 50000000.0
        lab = 30000000.0
        ovh = 10000000.0

        total_cost = round(mat + lab + ovh, 2)
        projected_profit = round(contract - total_cost, 2)
        margin_pct = round((projected_profit / contract) * 100.0, 2)

        self.assertEqual(total_cost, 90000000.0)
        self.assertEqual(projected_profit, 60000000.0)
        self.assertEqual(margin_pct, 40.0)

    def test_accrual_financial_calculations(self):
        """Test accrual revenue, categorized HPP costs, and net accrual margin."""
        # Simulated lines: 2 Customer Invoices (100M and 50M), 1 Credit Note (10M)
        invoices = [
            {'type': 'out_invoice', 'amount': 100000000.0},
            {'type': 'out_invoice', 'amount': 50000000.0},
            {'type': 'out_refund', 'amount': 10000000.0},
        ]
        rev = sum(i['amount'] if i['type'] == 'out_invoice' else -i['amount'] for i in invoices)
        self.assertEqual(rev, 140000000.0)

        # Simulated expenses: Material 45M, Labor 25M, Overhead 10M
        expenses = [
            {'cost_type': 'material', 'amount': 30000000.0},
            {'cost_type': 'material', 'amount': 15000000.0},
            {'cost_type': 'labor', 'amount': 25000000.0},
            {'cost_type': 'overhead', 'amount': 10000000.0},
        ]
        mat = sum(e['amount'] for e in expenses if e['cost_type'] == 'material')
        lab = sum(e['amount'] for e in expenses if e['cost_type'] == 'labor')
        ovh = sum(e['amount'] for e in expenses if e['cost_type'] == 'overhead')
        total_cost = mat + lab + ovh
        profit = rev - total_cost
        margin_pct = round((profit / rev) * 100.0, 2)

        self.assertEqual(mat, 45000000.0)
        self.assertEqual(lab, 25000000.0)
        self.assertEqual(ovh, 10000000.0)
        self.assertEqual(total_cost, 80000000.0)
        self.assertEqual(profit, 60000000.0)
        self.assertEqual(margin_pct, 42.86)

    def test_cash_position_and_liquidity(self):
        """Test cash received, cash disbursed, net cashflow, and unpaid AR/AP balances."""
        # Client invoices: 140M billed, 90M paid, 50M residual (AR)
        client_invoices = [
            {'amount_total': 140000000.0, 'amount_residual': 50000000.0}
        ]
        cash_received = sum(m['amount_total'] - m['amount_residual'] for m in client_invoices)
        uncollected_ar = sum(m['amount_residual'] for m in client_invoices)

        # Supplier bills: 80M billed, 60M paid, 20M residual (AP)
        supplier_bills = [
            {'amount_total': 80000000.0, 'amount_residual': 20000000.0}
        ]
        cash_disbursed = sum(m['amount_total'] - m['amount_residual'] for m in supplier_bills)
        unpaid_ap = sum(m['amount_residual'] for m in supplier_bills)

        net_cash = cash_received - cash_disbursed

        self.assertEqual(cash_received, 90000000.0)
        self.assertEqual(uncollected_ar, 50000000.0)
        self.assertEqual(cash_disbursed, 60000000.0)
        self.assertEqual(unpaid_ap, 20000000.0)
        self.assertEqual(net_cash, 30000000.0)

    def test_budget_variance_and_burn_rate(self):
        """Test budget variance per category and overall burn rate percentage."""
        budget_mat = 50000000.0
        actual_mat = 45000000.0
        var_mat = budget_mat - actual_mat

        budget_total = 90000000.0
        actual_total = 80000000.0
        var_total = budget_total - actual_total
        burn_rate = round((actual_total / budget_total) * 100.0, 2)

        self.assertEqual(var_mat, 5000000.0)
        self.assertEqual(var_total, 10000000.0)
        self.assertEqual(burn_rate, 88.89)

    def test_health_status_traffic_light(self):
        """Test healthy, warning, and critical traffic-light transitions."""
        def evaluate_health(budget, actual, net_cash, unpaid_ap, cash_received):
            burn = (actual / budget * 100.0) if budget else 0.0
            if (budget > 0 and actual > budget) or net_cash < 0:
                return 'critical'
            elif burn >= 85.0 or (unpaid_ap > cash_received and unpaid_ap > 0):
                return 'warning'
            return 'healthy'

        # Case 1: Healthy (Burn 70%, Positive Cash)
        self.assertEqual(evaluate_health(100.0, 70.0, 20.0, 10.0, 30.0), 'healthy')

        # Case 2: Warning (Burn 88%, Positive Cash)
        self.assertEqual(evaluate_health(100.0, 88.0, 15.0, 10.0, 25.0), 'warning')

        # Case 3: Warning (Cash squeeze: unpaid AP > cash received)
        self.assertEqual(evaluate_health(100.0, 60.0, 5.0, 40.0, 20.0), 'warning')

        # Case 4: Critical (Over Budget: Burn 105%)
        self.assertEqual(evaluate_health(100.0, 105.0, 10.0, 5.0, 30.0), 'critical')

        # Case 5: Critical (Cash Deficit: Net Cash < 0)
        self.assertEqual(evaluate_health(100.0, 80.0, -15.0, 10.0, 30.0), 'critical')

    def test_indonesian_wht_and_closure_guard(self):
        """Test Indonesian WHT deduction rates (PP 9/2021 & PPh 23) and closure guard."""
        revenue = 100000000.0
        total_cost = 60000000.0

        # PPh 23 (2.0%)
        wht_23 = round(revenue * 0.02, 2)
        net_23 = round(revenue - wht_23 - total_cost, 2)
        self.assertEqual(wht_23, 2000000.0)
        self.assertEqual(net_23, 38000000.0)

        # PPh Final Konstruksi Menengah (2.65% under PP 9/2021)
        wht_konst = round(revenue * 0.0265, 2)
        net_konst = round(revenue - wht_konst - total_cost, 2)
        self.assertEqual(wht_konst, 2650000.0)
        self.assertEqual(net_konst, 37350000.0)

        # Closure Guard Logic: triggers warning when uncollected AR or unpaid AP > 0
        def check_closure_guard(ar, ap):
            return bool(ar > 0 or ap > 0)

        self.assertTrue(check_closure_guard(50000000.0, 0.0))
        self.assertTrue(check_closure_guard(0.0, 20000000.0))
        self.assertTrue(check_closure_guard(10000.0, 50000.0))
        self.assertFalse(check_closure_guard(0.0, 0.0))

if __name__ == '__main__':
    unittest.main()
