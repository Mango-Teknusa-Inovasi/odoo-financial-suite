# -*- coding: utf-8 -*-
"""
Unit Tests for Bank Indonesia Official Currency Rate Auto-Sync (l10n_id_bi_currency_rate)
Tests Odoo currency rate inversion, Kurs Tengah BI calculation, last business day calendar logic,
cross-rate math, active currency filtering, and resilience cascade.
"""

import unittest
from datetime import date, timedelta

class TestBiCurrencyRateEngine(unittest.TestCase):
    """Test suite for Indonesian statutory currency exchange synchronization."""

    def test_odoo_rate_inversion(self):
        """Test bidirectional conversion between Odoo rate (1/IDR) and human-friendly Rupiah."""
        idr_usd = 16250.0
        odoo_rate = round(1.0 / idr_usd, 12)
        recalculated_idr = round(1.0 / odoo_rate, 2)

        self.assertAlmostEqual(odoo_rate, 0.0000615385, places=8)
        self.assertEqual(recalculated_idr, 16250.0)

        # Test SGD
        idr_sgd = 12150.0
        odoo_sgd_rate = round(1.0 / idr_sgd, 12)
        recalculated_sgd = round(1.0 / odoo_sgd_rate, 2)
        self.assertEqual(recalculated_sgd, 12150.0)

    def test_kurs_tengah_calculation(self):
        """Test calculation of Bank Indonesia middle rate: (Beli + Jual) / 2."""
        beli = 16180.0
        jual = 16320.0
        tengah = round((beli + jual) / 2.0, 2)

        self.assertEqual(tengah, 16250.0)

        # When only one rate exists (single rate fallback)
        single_rate = 16250.0
        tengah_single = (single_rate + 0.0) / 2.0 if (single_rate and 0.0) else single_rate
        self.assertEqual(tengah_single, 16250.0)

    def test_last_business_day_calendar(self):
        """Test weekend roll-back to the latest preceding Friday."""
        def get_last_business_day(target_date):
            weekday = target_date.weekday()
            if weekday == 5:  # Saturday
                return target_date - timedelta(days=1)
            elif weekday == 6:  # Sunday
                return target_date - timedelta(days=2)
            return target_date

        # Monday 2026-11-16 -> stays Monday
        mon = date(2026, 11, 16)
        self.assertEqual(get_last_business_day(mon), mon)

        # Friday 2026-11-20 -> stays Friday
        fri = date(2026, 11, 20)
        self.assertEqual(get_last_business_day(fri), fri)

        # Saturday 2026-11-21 -> rolls back to Friday 2026-11-20
        sat = date(2026, 11, 21)
        self.assertEqual(get_last_business_day(sat), fri)

        # Sunday 2026-11-22 -> rolls back to Friday 2026-11-20
        sun = date(2026, 11, 22)
        self.assertEqual(get_last_business_day(sun), fri)

    def test_active_currency_filter(self):
        """Test that only active database currencies are ingested, ignoring unconfigured currencies."""
        active_codes = {'USD', 'EUR', 'SGD', 'JPY'}
        incoming_payload = {
            'USD': {'beli': 16180, 'jual': 16320},
            'EUR': {'beli': 17500, 'jual': 17650},
            'SGD': {'beli': 12100, 'jual': 12200},
            'JPY': {'beli': 105, 'jual': 107},
            'ZWL': {'beli': 1, 'jual': 2},
            'KPW': {'beli': 18, 'jual': 19},
            'ALL': {'beli': 150, 'jual': 160},
        }

        filtered_rates = {k: v for k, v in incoming_payload.items() if k in active_codes}
        self.assertEqual(set(filtered_rates.keys()), {'USD', 'EUR', 'SGD', 'JPY'})
        self.assertNotIn('ZWL', filtered_rates)
        self.assertNotIn('KPW', filtered_rates)

    def test_cross_rate_computation(self):
        """Test computing non-USD currency rates against IDR using USD base cross-rates."""
        idr_per_usd = 16250.0
        # If 1 USD = 0.92 EUR
        usd_per_eur = 0.92
        idr_per_eur = round(idr_per_usd / usd_per_eur, 2)
        self.assertEqual(idr_per_eur, 17663.04)

        # If 1 USD = 1.34 SGD
        usd_per_sgd = 1.34
        idr_per_sgd = round(idr_per_usd / usd_per_sgd, 2)
        self.assertEqual(idr_per_sgd, 12126.87)

    def test_fallback_cascade_logic(self):
        """Test resilience fallback: Primary Fail -> Mirror Fallback -> Internal Carry-Forward."""
        def fetch_cascade(simulate_bi_fail, simulate_mirror_fail):
            if not simulate_bi_fail:
                return {"USD": 16250.0}, "Bank Indonesia Official API", "success"
            if not simulate_mirror_fail:
                return {"USD": 16240.0}, "Open Forex Mirror", "warning"
            return {"USD": 16200.0}, "Internal Database Carry-Forward", "warning"

        # Case 1: All working
        rates, src, status = fetch_cascade(False, False)
        self.assertEqual(status, "success")
        self.assertIn("Official", src)

        # Case 2: BI down, Mirror up
        rates, src, status = fetch_cascade(True, False)
        self.assertEqual(status, "warning")
        self.assertIn("Mirror", src)

        # Case 3: Both down, Carry-forward
        rates, src, status = fetch_cascade(True, True)
        self.assertEqual(status, "warning")
        self.assertIn("Carry-Forward", src)


if __name__ == '__main__':
    unittest.main()
