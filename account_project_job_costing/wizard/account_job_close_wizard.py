# -*- coding: utf-8 -*-
from odoo import models, fields, _

class AccountJobCloseWizard(models.TransientModel):
    _name = 'account.job.close.wizard'
    _description = 'Audit Penutupan Proyek: Konfirmasi Saldo Tertunda'

    project_job_id = fields.Many2one(
        'account.job.costing',
        string="Proyek",
        required=True,
        readonly=True
    )
    uncollected_ar = fields.Monetary(
        related='project_job_id.uncollected_ar',
        string="Sisa Piutang Klien",
        readonly=True
    )
    unpaid_ap = fields.Monetary(
        related='project_job_id.unpaid_ap',
        string="Sisa Hutang Vendor",
        readonly=True
    )
    currency_id = fields.Many2one(
        related='project_job_id.currency_id',
        readonly=True
    )
    warning_message = fields.Text(
        string="Rincian Audit Finansial",
        readonly=True
    )
    manager_note = fields.Char(
        string="Alasan / Justifikasi Penutupan",
        required=True,
        default="Pekerjaan fisik selesai, sisa saldo dalam proses penagihan/pembayaran terpisah."
    )

    def action_confirm_close(self):
        """Konfirmasi penutupan proyek dan catat justifikasi manajer di chatter."""
        self.ensure_one()
        reason = f"{self.manager_note} (Piutang: {self.currency_id.symbol} {self.uncollected_ar:,.2f}, Hutang: {self.currency_id.symbol} {self.unpaid_ap:,.2f})"
        self.project_job_id.action_force_complete(reason=reason)
        return {'type': 'ir.actions.act_window_close'}
