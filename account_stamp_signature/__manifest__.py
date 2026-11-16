# -*- coding: utf-8 -*-
{
    'name': 'Stamp & e-Meterai',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Dual-engine official company stamp, authorized signature overlay & Peruri e-Meterai gateway for Odoo invoices',
    'description': """
Dual-Engine Document Seal, Signature & Peruri e-Meterai Gateway
===============================================================
Designed for Indonesian legal and commercial documentation standards:

1. Engine A: Free & Offline Document Stamping
---------------------------------------------
- Transparent PNG corporate wet seal overlay with dynamic -6° rotation and opacity.
- Authorized executive digital signature block with name and official designation.
- Fully rendered directly in standard Odoo QWeb PDF invoice reports.
- 100% offline, zero API calls, free forever.

2. Engine B: Statutory Peruri e-Meterai Gateway (UU No. 10/2020)
---------------------------------------------------------------
- Automatic threshold detection: invoices >= Rp 5,000,000 flagged for Bea Meterai duty (Rp 10.000).
- Bring Your Own Key (BYOK) architecture supporting Peruri Digital Security (PDS), Mekari Sign, and PrivyID.
- Built-in Local Sandbox Engine (Mock Provider) for free testing and simulation.
- Affixes verifiable 22-digit Peruri Serial Number and public verification QR code.
- Automatic chatter audit trail and status tracking.
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
        'security/stamp_security.xml',
        'security/ir.model.access.csv',
        'views/emeterai_provider_views.xml',
        'views/res_company_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
        'report/invoice_report_templates.xml',
        'data/emeterai_demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
