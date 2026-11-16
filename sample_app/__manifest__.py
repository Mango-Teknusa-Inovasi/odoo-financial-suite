{
    'name': 'Sample Task App',
    'version': '1.0.0',
    'summary': 'Starter template module for testing, verification and scaffold development',
    'description': """
Sample Task App Module
======================
Lightweight baseline scaffold module for testing and verified development on Odoo 18.0 and 20.0.
Features:
- Task management baseline
- Model, Views (Tree, Form, Search), Action, and Menu items
- Security access rights configuration (ir.model.access.csv)
    """,
    'category': 'Extra Tools',
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite',
    'support': 'billing@ppti.me',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/sample_task_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
