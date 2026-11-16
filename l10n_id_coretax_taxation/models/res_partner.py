# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_id_npwp16 = fields.Char(
        string='NPWP 16 Digits',
        size=16,
        help='16-digit format Indonesian Tax Identification Number (NIK / NPWP 16).'
    )
    l10n_id_nitku = fields.Char(
        string='NITKU (22 Digits)',
        size=22,
        help='Nomor Induk Tempat Kegiatan Usaha (22 Digits) for branch or workplace identification.'
    )
    l10n_id_taxpayer_type = fields.Selection([
        ('badan', 'Corporate (Badan)'),
        ('orang_pribadi', 'Individual (Orang Pribadi)'),
        ('pemerintah', 'Government (Instansi Pemerintah)'),
    ], string='Taxpayer Category', default='badan', required=True)

    l10n_id_has_skb = fields.Boolean(
        string='Has SKB Facility',
        help='Indicates whether partner holds a valid Tax Exemption Certificate (Surat Keterangan Bebas).'
    )
    l10n_id_skb_number = fields.Char(
        string='SKB Certificate Number'
    )
    l10n_id_skb_valid_until = fields.Date(
        string='SKB Expiration Date'
    )

    @api.onchange('l10n_id_npwp16')
    def _onchange_l10n_id_npwp16(self):
        if self.l10n_id_npwp16:
            # Strip non-digits
            cleaned = re.sub(r'\D', '', self.l10n_id_npwp16)
            self.l10n_id_npwp16 = cleaned

    @api.onchange('l10n_id_nitku')
    def _onchange_l10n_id_nitku(self):
        if self.l10n_id_nitku:
            # Strip non-digits
            cleaned = re.sub(r'\D', '', self.l10n_id_nitku)
            self.l10n_id_nitku = cleaned

    @api.constrains('l10n_id_npwp16')
    def _check_l10n_id_npwp16(self):
        for partner in self:
            if partner.l10n_id_npwp16 and len(partner.l10n_id_npwp16) != 16:
                raise ValidationError(_("NPWP 16 must consist of exactly 16 numeric digits."))

    @api.constrains('l10n_id_nitku')
    def _check_l10n_id_nitku(self):
        for partner in self:
            if partner.l10n_id_nitku and len(partner.l10n_id_nitku) != 22:
                raise ValidationError(_("NITKU must consist of exactly 22 numeric digits."))
