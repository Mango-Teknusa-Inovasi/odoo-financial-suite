# -*- coding: utf-8 -*-
{
    'name': 'Project Job Costing',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Agile project job costing & dual-metric P&L',
    'description': """
Project Job Costing & Dual-Metric Financial Analysis
====================================================
Pelacak laba rugi akrual vs posisi kas nyata per proyek untuk UKM, kontraktor, dan agensi.
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
        'security/project_job_security.xml',
        'data/ir_sequence_data.xml',
        'wizard/account_job_close_wizard_views.xml',
        'views/account_job_costing_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
        'reports/report_job_costing.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
