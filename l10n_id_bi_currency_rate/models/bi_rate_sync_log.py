# -*- coding: utf-8 -*-
from odoo import models, fields

class BiRateSyncLog(models.Model):
    _name = 'bi.rate.sync.log'
    _description = 'Riwayat Sinkronisasi Kurs Bank Indonesia'
    _order = 'sync_date desc, id desc'

    name = fields.Char(
        string="No. Log",
        required=True,
        readonly=True,
        default="/"
    )
    sync_date = fields.Datetime(
        string="Waktu Eksekusi",
        default=fields.Datetime.now,
        readonly=True
    )
    target_date = fields.Date(
        string="Tanggal Efektif Kurs",
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company',
        string="Perusahaan",
        required=True,
        readonly=True,
        default=lambda self: self.env.company
    )
    status = fields.Selection([
        ('success', 'Berhasil'),
        ('warning', 'Peringatan / Fallback'),
        ('failed', 'Gagal')
    ], string="Status", required=True, readonly=True)

    source_used = fields.Char(
        string="Sumber Data Digunakan",
        readonly=True
    )
    currencies_updated = fields.Char(
        string="Daftar Valas Terbarui",
        readonly=True
    )
    currency_count = fields.Integer(
        string="Jumlah Valas",
        readonly=True
    )
    summary = fields.Text(
        string="Rincian Nilai Kurs",
        readonly=True
    )
    error_message = fields.Text(
        string="Catatan Error / Warning",
        readonly=True
    )
