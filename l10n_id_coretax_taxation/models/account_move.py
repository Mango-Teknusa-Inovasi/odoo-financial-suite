# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_id_bupot_number = fields.Char(
        string='No. Bukti Potong (Bupot)',
        copy=False,
        help='Official withholding tax slip number issued by DJP / counterparty.'
    )
    l10n_id_bupot_date = fields.Date(
        string='Tanggal Bukti Potong',
        copy=False
    )
    l10n_id_tax_object_code = fields.Char(
        string='Kode Objek Pajak (KOP)',
        help='Primary Tax Object Code associated with this invoice / bill.'
    )
    l10n_id_umkm_settlement_type = fields.Selection([
        ('self', 'Disetor Sendiri (Self-Remitted)'),
        ('withheld', 'Dipotong Lawan Transaksi (Withheld by Counterparty)'),
    ], string='PPh Final UMKM Settlement', default='self',
       help='Determination under PP 20/2026: whether tax is paid directly by taxpayer or withheld by counterparty.')

    l10n_id_coretax_exported = fields.Boolean(
        string='Coretax Exported',
        default=False,
        readonly=True,
        copy=False
    )
