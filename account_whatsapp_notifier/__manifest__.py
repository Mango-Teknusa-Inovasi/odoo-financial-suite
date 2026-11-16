# -*- coding: utf-8 -*-
{
    'name': 'WhatsApp Finance Notifier',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': '1-Click WhatsApp Invoicing, GOWA Bridge, Meta Cloud API, and Direct PDF Dispatch',
    'description': """
WhatsApp Finance Notifier
=========================
Enterprise-grade WhatsApp document dispatch and customer notification engine for Odoo Accounting, designed specifically for Indonesian businesses, retail, and multichannel online merchants.

Key Highlights:
1. Multi-Engine Gateway Architecture:
   - Mode 1: Native Click-to-Chat (wa.me) - 100% free client-side WhatsApp Web / Desktop link with zero setup or API keys.
   - Mode 2: GOWA Connector - Native REST API integration with aldinokemal/go-whatsapp-web-multidevice for self-hosted automated messaging with zero Meta API fees.
   - Mode 3: Meta Official WhatsApp Cloud API - High-volume official Graph API integration with Bearer Token and Phone Number ID.
   - Mode 4: Custom REST Webhook - Generic JSON payload connector for Fonnte, Wablas, or proprietary proxies.
2. Direct PDF Document Dispatch:
   - Renders official QWeb invoice PDF reports directly in memory and uploads them via GOWA multipart /send/file endpoint with customized greeting captions.
3. Indonesian Mobile Number Normalizer:
   - Automatically sanitizes 08xx and +62 8xx numbers to international standard format with zero manual user friction.
4. Dynamic Placeholder Template Engine:
   - Pre-seeded Indonesian templates for New Invoices, Due Date Reminders, and Payment Confirmations with automatic field interpolation.
5. Smart Cross-Module Synergy:
   - Automatically includes dynamic QRIS payment instructions when account_qris_qbiz is active.
   - Displays official e-Meterai seal validation status when account_stamp_signature is active.
6. Full Audit Trail:
   - Automatically logs dispatched WhatsApp messages, delivery timestamps, and recipients to the invoice Chatter.
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
        'security/whatsapp_security.xml',
        'data/default_templates_data.xml',
        'views/account_whatsapp_template_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_whatsapp_composer_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
