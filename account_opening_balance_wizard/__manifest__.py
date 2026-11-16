# -*- coding: utf-8 -*-
{
    'name': 'Opening Balance Wizard',
    'version': '20.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Single-window opening balance wizard with live balance bar, Excel import, and Indonesian tax asset register',
    'description': """
Opening Balance Setup Wizard
============================
Enterprise-grade initial balance setup engine for Odoo Accounting, designed specifically for Indonesian businesses, retail, F&B, and manufacturing enterprises migrating from legacy accounting systems (Accurate, Zahir, Jurnal, SAP, or Excel spreadsheets).

Key Capabilities:
1. Live Real-Time Balance Status Bar:
   - Dynamic real-time calculation of Total Debits, Total Credits, and Net Equity Difference.
   - Intelligent auto-balancing to Owner's Equity (Modal Pemilik) or Retained Earnings (Laba Ditahan).
2. Multi-Sheet Excel Import & Export:
   - Pre-formatted multi-sheet XLSX template for Cash/Bank, Customers (AR), Vendors (AP), Inventory, and Fixed Assets.
   - Bulk upload with data cleansing and duplicate prevention.
3. Indonesian Tax-Compliant Asset Register:
   - UU PPh Pasal 11 straight-line monthly depreciation scheduler (Kelompok 1 to 4, Bangunan Permanen).
   - Generates opening acquisition cost and accumulated depreciation journal items automatically.
4. Open Receivable & Payable Historical Line Generator:
   - Creates posted opening customer invoices and vendor bills tagged with opening balance indicator.
   - Uses zero-balance clearing accounts to maintain ledger integrity without double counting.
5. Warehouse Stock Quant Integration:
   - Optional automatic physical inventory stock valuation adjustment on cut-off date.
    """,
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite',
    'support': 'billing@ppti.me',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'images': [
        'static/description/banner.png',
    ],
    'depends': ['base', 'account', 'stock', 'mail'],
    'data': [
        'security/opening_balance_security.xml',
        'security/ir.model.access.csv',
        'views/account_simple_asset_views.xml',
        'views/account_opening_balance_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/opening_balance_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
