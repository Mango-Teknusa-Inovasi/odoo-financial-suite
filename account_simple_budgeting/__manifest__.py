# -*- coding: utf-8 -*-
{
    'name': 'Simple Visual Budgeting',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Visual budgeting & expense target progress',
    'description': """
Simple Visual Budgeting & Real-Time Target Progress
===================================================
Visual budgeting engine comparing planned budgets against actual General Ledger
postings with real-time gauges, traffic lights, and soft warning vendor bill guards.
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
        'security/budget_security.xml',
        'views/account_budget_category_views.xml',
        'views/account_simple_budget_views.xml',
        'views/account_move_views.xml',
        'wizard/account_budget_excel_export_wizard_views.xml',
        'views/menu_views.xml',
        'reports/report_budget_realization.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
