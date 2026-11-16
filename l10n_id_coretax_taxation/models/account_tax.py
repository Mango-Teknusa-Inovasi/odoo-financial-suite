# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountTax(models.Model):
    _inherit = 'account.tax'

    l10n_id_tax_type = fields.Selection([
        ('ppn', 'PPN (Value Added Tax)'),
        ('pph21', 'PPh 21 (Personal Income & Wages)'),
        ('pph22', 'PPh 22 (Procurement & Import)'),
        ('pph23', 'PPh 23 (Services, Rentals & Royalties)'),
        ('pph4_2', 'PPh 4 ayat (2) (Final Tax / Land & Building / Construction)'),
        ('pph_final_umkm', 'PPh Final UMKM 0.5% (PP 20/2026)'),
        ('pph15', 'PPh 15 (Shipping & International Transportation)'),
        ('pph26', 'PPh 26 (Non-Resident Foreign Taxpayer)'),
    ], string='Indonesian Tax Classification', help='Regulatory classification for DJP Coretax reporting.')

    l10n_id_tax_object_code = fields.Char(
        string='Kode Objek Pajak (KOP)',
        help='Official tax object code according to DJP Coretax guidelines (e.g. 24-104-01).'
    )
    l10n_id_is_withholding = fields.Boolean(
        string='Is Withholding Tax',
        default=False,
        help='Indicates this tax is deducted from invoice payment rather than added to the total.'
    )
