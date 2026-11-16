{
    'name': 'Indonesian Taxation & Coretax Compliance',
    'version': '20.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Indonesian Withholding Tax (PPh 21/22/23/4(2)/Final UMKM PP 20/2026), 16-Digit NPWP, NITKU & Coretax Export',
    'description': """
Indonesian Taxation & Coretax Compliance Suite
==============================================
Empowers Odoo with comprehensive Indonesian tax localization:
- 16-Digit NPWP (NIK/NPWP16) & 22-Digit NITKU for partners.
- Withholding Tax (PPh 21, 22, 23, 4(2), and PPh Final UMKM 0.5% under PP 20/2026).
- Bukti Potong (Tax Withholding Slip) tracking & Kode Objek Pajak on invoices and vendor bills.
- Export wizard for DJP Coretax monthly e-Bupot integration.
    """,
    'author': 'Mango Teknusa Inovasi',
    'website': 'https://github.com/Mango-Teknusa-Inovasi/odoo-financial-suite',
    'license': 'LGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/tax_data.xml',
        'views/res_partner_views.xml',
        'views/account_tax_views.xml',
        'views/account_move_views.xml',
        'views/coretax_export_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
