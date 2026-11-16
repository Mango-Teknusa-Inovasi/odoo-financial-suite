{
    'name': 'Sample App',
    'version': '1.0.0',
    'summary': 'Starter template modul Odoo 20 untuk testing & development',
    'description': """
Sample App Module
=================
Modul contoh untuk development plugin/addon Odoo 18.
Fitur:
- Manajemen Task sederhana
- Model, View (Tree, Form, Search), Action, dan Menu
- Hak akses Security (ir.model.access.csv)
    """,
    'category': 'Extra Tools',
    'author': 'Your Name / Team',
    'website': 'https://www.odoo.com',
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
