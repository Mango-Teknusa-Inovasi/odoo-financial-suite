# -*- coding: utf-8 -*-
{
    'name': 'POS Thermal Receipt',
    'version': '20.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Perancang struk kasir thermal 58/80mm & ESC/POS',
    'description': """
POS Thermal Receipt Designer & ESC/POS Engine
=============================================
Perancang dan generator struk thermal 58mm & 80mm untuk printer Bluetooth dan desktop counter di Indonesia.
Mendukung QRIS dinamis, logo monokrom 1-bit dithering, layout anti-terpotong (adaptive dual-line), dan cetak langsung dari faktur maupun POS.
    """,
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/mangotek/odoo-finance',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': [
        'base',
        'account',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/thermal_security.xml',
        'reports/report_paperformat.xml',
        'reports/report_thermal_receipt.xml',
        'data/default_thermal_templates.xml',
        'views/pos_thermal_template_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
