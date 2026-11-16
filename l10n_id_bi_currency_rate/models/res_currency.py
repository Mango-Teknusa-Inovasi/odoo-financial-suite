# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResCurrencyRate(models.Model):
    _inherit = 'res.currency.rate'

    idr_rate = fields.Float(
        string="Kurs Rupiah (Rp)",
        digits=(16, 2),
        compute='_compute_idr_rate',
        inverse='_inverse_idr_rate',
        store=True,
        help="Nilai tukar dalam Rupiah (misal: Rp 16.250 untuk 1 USD)."
    )
    rate_source = fields.Selection([
        ('bi_middle', 'Kurs Tengah BI (Komersial)'),
        ('jisdor', 'JISDOR Bank Indonesia (USD)'),
        ('kmk_tax', 'Kurs Pajak KMK (Fiskal / PPN)'),
        ('manual', 'Manual')
    ], string="Sumber Kurs", default='manual', tracking=True)

    source_reference = fields.Char(
        string="Referensi Sumber / No. KMK",
        help="Nomor Keputusan Menteri Keuangan atau tanggal publikasi BI."
    )

    @api.depends('rate', 'company_id.currency_id')
    def _compute_idr_rate(self):
        """Konversi otomatis dari rate Odoo (1/IDR) ke representasi Rupiah komersial."""
        for rec in self:
            if rec.rate and rec.rate > 0:
                rec.idr_rate = round(1.0 / rec.rate, 2)
            else:
                rec.idr_rate = 0.0

    def _inverse_idr_rate(self):
        """Konversi saat pengguna mengetik nominal Rupiah langsung (misal: 16250 -> 0.000061538)."""
        for rec in self:
            if rec.idr_rate and rec.idr_rate > 0:
                rec.rate = 1.0 / rec.idr_rate
