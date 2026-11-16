# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    bi_sync_enabled = fields.Boolean(
        string="Aktifkan Sinkronisasi Kurs BI",
        default=True,
        help="Aktifkan pembaruan otomatis kurs valas harian dari Bank Indonesia & Kemenkeu."
    )
    bi_rate_source = fields.Selection([
        ('dual_with_tax', 'Dual Sumber: JISDOR (USD) + Kurs Tengah BI + Kurs Pajak KMK'),
        ('jisdor_usd_bi_other', 'Komersial Saja: JISDOR (USD) & Kurs Tengah BI'),
        ('bi_middle', 'Kurs Tengah BI Murni (Beli + Jual)/2 untuk Semua Valas')
    ], string="Metode Penentuan Kurs", default='dual_with_tax', required=True)

    bi_last_sync_date = fields.Datetime(
        string="Terakhir Disinkronkan",
        readonly=True
    )
    bi_last_sync_status = fields.Selection([
        ('draft', 'Belum Pernah'),
        ('success', 'Berhasil'),
        ('warning', 'Peringatan (Fallback/Hari Libur)'),
        ('failed', 'Gagal')
    ], string="Status Sinkronisasi", default='draft', readonly=True)

    bi_last_sync_message = fields.Text(
        string="Catatan Sinkronisasi Terakhir",
        readonly=True
    )
