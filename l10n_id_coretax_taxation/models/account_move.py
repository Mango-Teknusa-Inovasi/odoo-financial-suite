# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Withholding Tax (PPh) Fields
    l10n_id_bupot_number = fields.Char(
        string='No. Bukti Potong (Bupot)',
        copy=False,
        index=True,
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

    # e-Faktur & NSFP (PPN) Fields
    l10n_id_faktur_pajak_number = fields.Char(
        string='Nomor Faktur Pajak (NSFP)',
        copy=False,
        index=True,
        help='Official 16-digit formatted Faktur Pajak number (e.g. 01.000-26.00000001)'
    )
    l10n_id_tax_transaction_code = fields.Selection([
        ('01', '01 - Kepada Pihak Bukan Pemungut PPN (Standard)'),
        ('02', '02 - Kepada Pemungut Bendaharawan Pemerintah'),
        ('03', '03 - Kepada Pemungut BUMN / Badan Usaha Tertentu'),
        ('04', '04 - DPP Nilai Lain (Effective 11% / 12% Calculation)'),
        ('05', '05 - Besaran Tertentu (Pasal 9A UU PPN)'),
        ('07', '07 - Penyerahan yang PPN-nya Tidak Dipungut (Kawasan Berikat)'),
        ('08', '08 - Penyerahan yang Dibebaskan dari Pengenaan PPN'),
        ('09', '09 - Penyerahan Aktiva Pasal 16D UU PPN'),
    ], string='Kode Transaksi Faktur Pajak', default='01')

    l10n_id_faktur_date = fields.Date(
        string='Tanggal Faktur Pajak',
        default=fields.Date.context_today
    )
    l10n_id_efaktur_status = fields.Selection([
        ('unassigned', 'Belum Ada NSFP'),
        ('assigned', 'NSFP Assigned'),
        ('exported', 'Exported to e-Faktur CSV'),
        ('approved', 'Approved DJP Coretax'),
        ('cancelled', 'Dibatalkan'),
    ], string='Status e-Faktur', default='unassigned', copy=False)

    l10n_id_is_dpp_nilai_lain = fields.Boolean(
        string='Apply DPP Nilai Lain',
        default=False,
        help='Calculate PPN base using statutory deemed tax base formula (e.g. 11/12 ratio).'
    )
    l10n_id_dpp_factor = fields.Float(
        string='DPP Factor Ratio',
        default=0.9166666667,
        digits=(12, 10),
        help='Multiplier applied to gross amount to determine DPP Nilai Lain (default 11/12 = 0.9166666667)'
    )

    def action_assign_nsfp(self):
        """Allocate next available NSFP from the active range of the invoice company."""
        for move in self:
            if move.move_type not in ('out_invoice', 'out_refund'):
                continue
            if move.l10n_id_faktur_pajak_number:
                continue

            pool = self.env['l10n_id.nsfp.range'].search([
                ('company_id', '=', move.company_id.id),
                ('active', '=', True),
                ('remaining_quota', '>', 0)
            ], limit=1)

            if not pool:
                raise UserError(_(
                    "No active NSFP range with remaining quota found for company '%s'! "
                    "Please configure NSFP ranges under Invoicing > Pajak Indonesia > NSFP Pool.",
                    move.company_id.name
                ))

            raw_serial = pool.allocate_next_nsfp()
            # 16-digit standard NSFP: 2-digit trx code + 1-digit status ('0') + 3-digit prefix + 2-digit year + 8-digit serial
            full_nsfp = f"{move.l10n_id_tax_transaction_code}0.{raw_serial}"
            vals = {
                'l10n_id_faktur_pajak_number': full_nsfp,
                'l10n_id_efaktur_status': 'assigned',
                'l10n_id_faktur_date': move.invoice_date or fields.Date.today(),
            }
            # Bridge synchronization with standard Odoo l10n_id field (strictly requires 16 digits)
            if 'l10n_id_tax_number' in move._fields:
                vals['l10n_id_tax_number'] = full_nsfp
            move.write(vals)

    def action_post(self):
        """Auto-assign NSFP upon posting outgoing customer invoice if pool is available."""
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund') and not move.l10n_id_faktur_pajak_number:
                pool = self.env['l10n_id.nsfp.range'].search([
                    ('company_id', '=', move.company_id.id),
                    ('active', '=', True),
                    ('remaining_quota', '>', 0)
                ], limit=1)
                if pool:
                    move.action_assign_nsfp()
        return res
