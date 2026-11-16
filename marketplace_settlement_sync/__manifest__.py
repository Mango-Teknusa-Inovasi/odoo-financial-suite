{
    'name': 'Marketplace Settlement',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Automated settlement ingestion and journal generation for Shopee, Tokopedia, TikTok Shop & Indonesian marketplaces',
    'description': """
Multichannel Marketplace Settlement Sync
========================================
Eliminates manual bookkeeping of online marketplace orders and payouts:
- Flexible Channel configuration (Shopee, Tokopedia, TikTok Shop, Blibli, etc.).
- Direct file parser for Excel (.xlsx) and CSV settlement statements.
- Intelligent split-accounting: automatically separates Gross Turnover, Marketplace Service Fees, and Net Escrow Deposits into balanced journal entries.
- Audit trail with order-level line item drilldown and batch validation preview.
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
    ],
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/marketplace_security.xml',
        'security/ir.model.access.csv',
        'data/channel_data.xml',
        'views/marketplace_channel_views.xml',
        'views/marketplace_settlement_batch_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
