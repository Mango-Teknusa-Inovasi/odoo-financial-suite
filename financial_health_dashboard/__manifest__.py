# -*- coding: utf-8 -*-
{
    'name': 'Financial Health KPI',
    'version': '20.0.1.0.0',
    'category': 'Accounting/Reporting',
    'summary': 'Executive financial ratio indicators (Liquidity, Solvency, Margins) with visual traffic-light status cards',
    'description': """
Executive Financial Health & Ratio KPI Dashboard
================================================
Designed for CFOs, business founders, and finance executives:

1. Liquidity Health Metrics
---------------------------
- Current Ratio: Total Current Assets / Current Liabilities (Benchmark >= 2.0x).
- Quick Ratio (Acid-Test): (Cash + Trade Receivables) / Current Liabilities (Benchmark >= 1.0x).
- Cash Ratio: Cash & Bank / Current Liabilities (Benchmark >= 0.5x).

2. Solvency & Balance Sheet Leverage
------------------------------------
- Debt-to-Equity Ratio (DER): Total Liabilities / Total Equity (Benchmark <= 1.0x).
- Debt-to-Asset Ratio (DAR): Total Liabilities / Total Assets (Benchmark <= 0.4x).

3. Profitability & Operational Performance
------------------------------------------
- Gross Profit Margin (GPM %): Gross Profit / Turnover * 100%.
- Net Profit Margin (NPM %): Net Profit After Tax / Turnover * 100%.
- Net Working Capital: Real-time surplus of operating liquidity.

4. Educational Traffic-Light System
-----------------------------------
- 🟢 Optimal / Safe: Exceeds conservative industry safety benchmarks.
- 🟡 Moderate: Borderline reserves or delayed trade collections.
- 🔴 Critical Risk: Solvency pressure or thin operating margins.
- Automated Executive Advisory Synthesis with plain-language diagnostic takeaways.
    """,
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite',
    'support': 'billing@ppti.me',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'images': [
        'static/description/banner.png',
        'static/description/screenshot_1.png',
        'static/description/screenshot_2.png',
    ],
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/health_security.xml',
        'security/ir.model.access.csv',
        'views/financial_health_kpi_views.xml',
        'views/menu_views.xml',
        'data/financial_health_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
