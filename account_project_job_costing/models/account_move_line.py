# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    project_job_id = fields.Many2one(
        'account.job.costing',
        string="Proyek",
        index=True,
        copy=False,
        help="Penanda proyek untuk alokasi biaya baris spesifik."
    )
    job_cost_type = fields.Selection([
        ('revenue', 'Pendapatan (Revenue)'),
        ('material', 'Material & Bahan Baku'),
        ('labor', 'Subkon & Upah Mandor'),
        ('overhead', 'Operasional & Overhead')
    ], string="Tipe Biaya Proyek", default='material', help="Kategori biaya untuk alokasi lembar biaya proyek.")

    @api.onchange('product_id')
    def _onchange_product_id_job_cost(self):
        """Deteksi tipe biaya otomatis berdasarkan tipe transaksi."""
        if self.move_id.move_type in ('out_invoice', 'out_refund'):
            self.job_cost_type = 'revenue'
        elif self.move_id.move_type in ('in_invoice', 'in_refund') and not self.job_cost_type:
            self.job_cost_type = 'material'
