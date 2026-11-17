# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountSimpleBudget(models.Model):
    _name = 'account.simple.budget'
    _description = 'Master Rencana Anggaran Keuangan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fiscal_year desc, id desc'

    name = fields.Char(
        string="Judul Anggaran",
        required=True,
        tracking=True,
        default=lambda self: f"Rencana Anggaran Keuangan {date.today().year}"
    )
    fiscal_year = fields.Integer(
        string="Tahun Fiskal",
        required=True,
        default=lambda self: date.today().year,
        tracking=True
    )
    date_from = fields.Date(
        string="Mulai Tanggal",
        required=True,
        default=lambda self: date(date.today().year, 1, 1)
    )
    date_to = fields.Date(
        string="Sampai Tanggal",
        required=True,
        default=lambda self: date(date.today().year, 12, 31)
    )
    company_id = fields.Many2one(
        'res.company',
        string="Perusahaan",
        required=True,
        default=lambda self: self.env.company
    )
    state = fields.Selection([
        ('draft', 'Draf Perencanaan'),
        ('confirmed', 'Aktif Berjalan'),
        ('closed', 'Ditutup / Selesai')
    ], string="Status Anggaran", default='draft', tracking=True, required=True)

    line_ids = fields.One2many(
        'account.simple.budget.line',
        'budget_id',
        string="Rincian Baris Anggaran"
    )

    # Executive KPI Summary Cards
    currency_id = fields.Many2one(
        related='company_id.currency_id',
        string="Mata Uang",
        readonly=True
    )

    total_budget_expense = fields.Monetary(
        string="Total Plafon Beban",
        compute='_compute_kpi_metrics',
        store=True,
        currency_field='currency_id'
    )
    total_realized_expense = fields.Monetary(
        string="Total Realisasi Beban",
        compute='_compute_kpi_metrics',
        store=True,
        currency_field='currency_id'
    )
    expense_burn_rate = fields.Float(
        string="Burn Rate Beban (%)",
        compute='_compute_kpi_metrics',
        store=True
    )

    total_budget_revenue = fields.Monetary(
        string="Total Target Omset",
        compute='_compute_kpi_metrics',
        store=True,
        currency_field='currency_id'
    )
    total_realized_revenue = fields.Monetary(
        string="Total Realisasi Omset",
        compute='_compute_kpi_metrics',
        store=True,
        currency_field='currency_id'
    )
    revenue_achievement_rate = fields.Float(
        string="Pencapaian Omset (%)",
        compute='_compute_kpi_metrics',
        store=True
    )

    overall_health_status = fields.Selection([
        ('healthy', 'Sehat (Aman)'),
        ('warning', 'Perhatian (Waspada)'),
        ('critical', 'Over Budget (Kritis)')
    ], string="Status Kesehatan Anggaran", compute='_compute_kpi_metrics', store=True)

    @api.onchange('fiscal_year')
    def _onchange_fiscal_year(self):
        """Otomatis atur batas tanggal 1 Januari sampai 31 Desember tahun fiskal."""
        if self.fiscal_year:
            self.date_from = date(self.fiscal_year, 1, 1)
            self.date_to = date(self.fiscal_year, 12, 31)

    @api.depends(
        'line_ids.annual_target',
        'line_ids.ytd_realized',
        'line_ids.budget_type'
    )
    def _compute_kpi_metrics(self):
        """Hitung ringkasan metrik eksekutif beban, omset, dan tingkat kesehatan."""
        for rec in self:
            expense_lines = rec.line_ids.filtered(lambda l: l.budget_type == 'expense')
            revenue_lines = rec.line_ids.filtered(lambda l: l.budget_type == 'revenue')

            tot_bud_exp = sum(expense_lines.mapped('annual_target'))
            tot_real_exp = sum(expense_lines.mapped('ytd_realized'))
            exp_burn = (tot_real_exp / tot_bud_exp * 100.0) if tot_bud_exp > 0 else 0.0

            tot_bud_rev = sum(revenue_lines.mapped('annual_target'))
            tot_real_rev = sum(revenue_lines.mapped('ytd_realized'))
            rev_achieve = (tot_real_rev / tot_bud_rev * 100.0) if tot_bud_rev > 0 else 0.0

            rec.total_budget_expense = tot_bud_exp
            rec.total_realized_expense = tot_real_exp
            rec.expense_burn_rate = round(exp_burn, 1)

            rec.total_budget_revenue = tot_bud_rev
            rec.total_realized_revenue = tot_real_rev
            rec.revenue_achievement_rate = round(rev_achieve, 1)

            # Evaluasi Lampu Indikator Lalu Lintas Anggaran
            if exp_burn > 100.0:
                rec.overall_health_status = 'critical'
            elif exp_burn > 85.0 or (tot_bud_rev > 0 and rev_achieve < 75.0):
                rec.overall_health_status = 'warning'
            else:
                rec.overall_health_status = 'healthy'

    def action_confirm(self):
        """Aktifkan rencana anggaran tahunan."""
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_("Tambahkan setidaknya satu baris kategori anggaran sebelum mengaktifkan."))
        self.action_recompute_realization()
        self.state = 'confirmed'

    def action_reset_draft(self):
        """Kembalikan status anggaran ke draf untuk penyesuaian target."""
        self.ensure_one()
        self.state = 'draft'

    def action_close(self):
        """Tutup anggaran tahunan setelah tutup buku tahun fiskal."""
        self.ensure_one()
        self.state = 'closed'

    def action_recompute_realization(self):
        """Paksa hitung ulang realisasi GL akun untuk seluruh 12 bulan."""
        self.ensure_one()
        for line in self.line_ids:
            line._compute_realization()

    def action_print_budget_report(self):
        """Buka laporan realisasi anggaran resmi QWeb PDF."""
        self.ensure_one()
        return self.env.ref('account_simple_budgeting.action_report_budget_realization').report_action(self)

    def action_export_excel(self):
        """Buka wizard ekspor spreadsheet audit Excel (.xlsx)."""
        self.ensure_one()
        return {
            'name': _('Ekspor Realisasi Anggaran (.xlsx)'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.budget.excel.export.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_budget_id': self.id}
        }
