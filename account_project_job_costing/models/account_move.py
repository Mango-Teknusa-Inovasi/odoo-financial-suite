# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    project_job_id = fields.Many2one(
        'account.job.costing',
        string="Proyek / Pekerjaan",
        copy=False,
        index=True,
        tracking=True,
        help="Hubungkan faktur atau tagihan vendor ini ke lembar biaya proyek terkait."
    )

    @api.onchange('project_job_id')
    def _onchange_project_job_id(self):
        """Alirkan penanda proyek secara otomatis ke seluruh baris faktur."""
        if self.project_job_id:
            for line in self.invoice_line_ids:
                if not line.project_job_id:
                    line.project_job_id = self.project_job_id

    def action_post(self):
        """Posting faktur dan pantau peringatan anggaran proyek secara non-blocking."""
        res = super().action_post()
        for move in self:
            if move.project_job_id and move.move_type in ('in_invoice', 'in_refund'):
                project = move.project_job_id
                # Soft audit alert if over budget
                if project.budget_total_cost > 0 and project.actual_total_cost > project.budget_total_cost:
                    project.message_post(
                        body=_(
                            "Peringatan Anggaran: Tagihan %(bill)s senilai %(amount)s telah diposting. "
                            "Total realisasi biaya proyek telah melebihi plafon anggaran (%(burn)s%%)."
                        ) % {
                            'bill': move.name or move.ref or _('Tagihan Vendor'),
                            'amount': f"{move.currency_id.symbol} {move.amount_total:,.2f}",
                            'burn': f"{project.burn_rate_pct:.1f}"
                        }
                    )
        return res
