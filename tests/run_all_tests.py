#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Unit & Feature Test Runner for MangoTek Financial Suite (LGPL-3.0)
Discovers and executes tests across all 5 core modules with automatic Odoo mocking for standalone CI.
"""

import unittest
import sys
import os
from unittest.mock import MagicMock

# Mock odoo package if not available in the host/CI environment
if "odoo" not in sys.modules:
    odoo_mock = MagicMock()
    sys.modules["odoo"] = odoo_mock
    sys.modules["odoo.models"] = MagicMock()
    sys.modules["odoo.fields"] = MagicMock()
    sys.modules["odoo.api"] = MagicMock()
    sys.modules["odoo.tools"] = MagicMock()
    sys.modules["odoo.exceptions"] = MagicMock()
    sys.modules["odoo.http"] = MagicMock()

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

MODULE_TEST_PATHS = [
    "l10n_id_coretax_taxation.tests.test_coretax",
    "marketplace_settlement_sync.tests.test_settlement",
    "fnb_hpp_calculator.tests.test_fnb_hpp",
    "account_stamp_signature.tests.test_stamp_emeterai",
    "financial_health_kpi.tests.test_financial_ratios",
    "account_qris_qbiz.tests.test_qris_emvco",
    "account_opening_balance_wizard.tests.test_opening_balance",
    "account_whatsapp_notifier.tests.test_whatsapp_notifier",
    "account_project_job_costing.tests.test_project_job_costing",
    "pos_thermal_receipt_designer.tests.test_thermal_receipt",
]

def run_suite():
    print("=" * 65)
    print(" 🧪 RUNNING MANGOTEK FINANCIAL SUITE UNIT & FEATURE TESTS")
    print("=" * 65)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for mod_test in MODULE_TEST_PATHS:
        try:
            tests = loader.loadTestsFromName(mod_test)
            suite.addTests(tests)
            print(f"  📦 Loaded test suite: {mod_test}")
        except Exception as e:
            print(f"  ❌ Error loading {mod_test}: {e}")
            return 1

    print("\n" + "-" * 65)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("-" * 65)

    print(f"\n📊 RESULTS: {result.testsRun} tests run.")
    if result.wasSuccessful():
        print("🎉 ALL UNIT & FEATURE TESTS PASSED SUCCESSFULLY!")
        return 0
    else:
        print(f"🚨 FAILED: {len(result.failures)} failures, {len(result.errors)} errors.")
        return 1

if __name__ == "__main__":
    sys.exit(run_suite())
