# -*- coding: utf-8 -*-
{
    'name': 'F&B Recipe HPP',
    'version': '1.0.0',
    'category': 'Point of Sale',
    'summary': 'Lightweight recipe costing, portion HPP, gross margin calculation & culinary BOM without heavy MRP',
    'description': """
F&B Recipe HPP & Menu Costing Engine
====================================
Designed specifically for cafés, bakeries, cloud kitchens, and restaurants:
- Portion HPP calculation from raw ingredient purchase units.
- Trimming, shrinkage, and preparation waste factor (%) adjustments.
- Dedicated packaging & disposable supplies costing layer.
- Interactive selling price & gross profit margin simulator.
- Visual health badges (Optimal >= 65%, Moderate 50-64%, Underpriced < 50%).
- 1-Click synchronization with Odoo POS and Sales catalog products.
- Multi-company enabled with zero heavy MRP complexity.
    """,
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite',
    'support': 'billing@ppti.me',
    'license': 'LGPL-3',
    'depends': ['base', 'product', 'mail'],
    'data': [
        'security/fnb_security.xml',
        'security/ir.model.access.csv',
        'data/fnb_demo_data.xml',
        'views/fnb_recipe_category_views.xml',
        'views/fnb_recipe_views.xml',
        'views/fnb_recipe_simulate_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
