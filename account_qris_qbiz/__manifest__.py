# -*- coding: utf-8 -*-
{
    'name': 'QBiz Dynamic QRIS',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Dynamic QRIS payment generation with pre-filled Tag 54 nominal and QBiz auto-reconciliation webhook',
    'description': """
QBiz Dynamic QRIS Payment Engine
================================
Automated dynamic QRIS payments for Indonesian commerce, powered by the open-source QBiz engine.

Key Highlights:
1. Dual Operating Modes:
   - Mode A (Standalone Local Engine): Pure Python EMVCo Tag 54 nominal injector with CCITT-16 CRC recalculation (zero external dependencies).
   - Mode B (QBiz Server API Connector): Interfacing with QBiz middleware for anti-collision unique code suffixes (e.g., Rp 50,002).
2. Universal Indonesian Interoperability:
   - 100% compliant with ASPI / Bank Indonesia QRIS standards.
   - Pre-fills exact payment amount across BCA Mobile, Livin' Mandiri, BRImo, BNI Mobile, GoPay, OVO, DANA, and ShopeePay.
3. Webhook Auto-Reconciliation:
   - Dedicated webhook controller (/api/v1/webhook/qris) receiving mutation alerts and automatically registering payment to mark customer invoices as PAID.
4. Multichannel Touchpoints:
   - High-resolution dynamic QR code rendered on customer invoice PDFs, customer web portals, and POS screens.
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
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
        'views/report_invoice_qris.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
