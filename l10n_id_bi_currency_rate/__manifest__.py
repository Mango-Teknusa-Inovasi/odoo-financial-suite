# -*- coding: utf-8 -*-
{
    'name': 'BI Currency Rate Sync',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Sinkronisasi kurs valas Bank Indonesia & KMK',
    'description': """
Bank Indonesia & Kemenkeu Official Currency Rate Auto-Sync
==========================================================
Sinkronisasi harian otomatis nilai tukar valuta asing resmi dari Bank Indonesia (JISDOR untuk USD & Kurs Tengah Transaksi BI) serta Kurs Pajak Mingguan Kementerian Keuangan (KMK) untuk pelaporan PPN dan e-Faktur.
    """,
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/mangotek/odoo-finance',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/bi_rate_security.xml',
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml',
        'views/res_currency_views.xml',
        'views/bi_rate_sync_log_views.xml',
        'views/menu_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
