# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    has_budget_warning = fields.Boolean(
        string="Peringatan Anggaran",
        compute='_compute_budget_warning'
    )
    budget_warning_message = fields.Text(
        string="Pesan Peringatan Anggaran",
        compute='_compute_budget_warning'
    )

    @api.depends('invoice_line_ids.account_id', 'invoice_line_ids.price_subtotal', 'invoice_date', 'date')
    def _compute_budget_warning(self):
        """
        Deteksi apakah nilai tagihan vendor berpotensi melampaui sisa plafon
        anggaran bulanan kategori yang dipetakan pada baris faktur.
        """
        for move in self:
            move.has_budget_warning = False
            move.budget_warning_message = False

            # Hanya pantau tagihan vendor (Beban / Biaya)
            if move.move_type not in ('in_invoice', 'in_refund'):
                continue

            ref_date = move.invoice_date or move.date or date.today()
            year = ref_date.year
            month = ref_date.month

            # Cari master anggaran aktif yang sesuai tahun dan perusahaan
            budget = self.env['account.simple.budget'].search([
                ('company_id', '=', move.company_id.id),
                ('fiscal_year', '=', year),
                ('state', '=', 'confirmed')
            ], limit=1)

            if not budget:
                continue

            warnings = []
            target_field = f"m{month}_target"
            realized_field = f"m{month}_realized"

            for line in move.invoice_line_ids:
                if not line.account_id or line.display_type:
                    continue

                # Cari baris anggaran yang memetakan akun ini
                budget_line = budget.line_ids.filtered(
                    lambda bl: bl.budget_type == 'expense' and line.account_id in bl.category_id.account_ids
                )
                if not budget_line:
                    continue

                b_line = budget_line[0]
                m_target = getattr(b_line, target_field, 0.0)
                m_realized = getattr(b_line, realized_field, 0.0)
                bill_amount = line.price_subtotal

                remaining = m_target - m_realized
                if m_target > 0 and (m_realized + bill_amount) > m_target:
                    over_amount = (m_realized + bill_amount) - m_target
                    warnings.append(
                        _("Kategori '%s' (Akun %s): Plafon Bln-%d Rp %s, Realisasi Rp %s. Tagihan ini melebihi plafon sebesar Rp %s.") % (
                            b_line.category_id.name,
                            line.account_id.code,
                            month,
                            f"{m_target:,.0f}",
                            f"{m_realized:,.0f}",
                            f"{over_amount:,.0f}"
                        )
                    )

            if warnings:
                move.has_budget_warning = True
                move.budget_warning_message = "\n".join(warnings)

    def action_post(self):
        """Konfirmasi faktur secara normal, dan catat peringatan ke Chatter jika anggaran terlampaui."""
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.has_budget_warning and move.budget_warning_message:
                move.message_post(
                    body=_(
                        "<strong>⚠️ Catatan Peringatan Anggaran:</strong><br/>%s"
                    ) % move.budget_warning_message.replace("\n", "<br/>"),
                    subtype_xmlid="mail.mt_note"
                )
        return res
