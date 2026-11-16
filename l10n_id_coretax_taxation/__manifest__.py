{
    'name': 'Indonesian Tax Coretax',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Indonesian DJP Coretax & e-Faktur Engine: PPN 12%, NSFP Allocator, Withholding Tax (PPh 21/22/23/4(2)/Final UMKM PP 20/2026), 16-Digit NPWP/NIK & Coretax CSV',
    'description': """
Indonesian Taxation & Coretax Compliance Suite
==============================================
Statutory Indonesian Commercial Taxation & DJP Coretax Engine:
- Statutory PPN 12% (UU HPP) & DPP Nilai Lain calculation engine.
- Automated NSFP (Nomor Seri Faktur Pajak) sequential assignment pool.
- DJP e-Faktur 4.0 & Coretax CSV batch exporter (FK and OF schemas).
- 16-Digit NIK / NPWP16 & 22-Digit NITKU validation (PMK 112/PMK.03/2022).
- Withholding Tax (PPh 21, 22, 23, 4(2), and PPh Final UMKM 0.5% under PP 20/2026).
- Bukti Potong tracking & Kode Objek Pajak (KOP) on invoices and vendor bills.
- e-Bupot CSV monthly export wizard for DJP Coretax portal.
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
    'depends': ['base', 'account'],
    'data': [
        'security/l10n_id_security.xml',
        'security/ir.model.access.csv',
        'data/tax_data.xml',
        'views/nsfp_range_views.xml',
        'views/res_partner_views.xml',
        'views/account_tax_views.xml',
        'views/account_move_views.xml',
        'views/efaktur_export_wizard_views.xml',
        'views/coretax_export_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
