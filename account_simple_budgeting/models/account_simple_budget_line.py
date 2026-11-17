# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import date
from odoo import models, fields, api, _

class AccountSimpleBudgetLine(models.Model):
    _name = 'account.simple.budget.line'
    _description = 'Baris Kategori Anggaran Keuangan'
    _order = 'budget_type desc, category_id asc'

    budget_id = fields.Many2one(
        'account.simple.budget',
        string="Rencana Anggaran",
        required=True,
        ondelete='cascade'
    )
    category_id = fields.Many2one(
        'account.budget.category',
        string="Kategori Anggaran",
        required=True
    )
    budget_type = fields.Selection(
        related='category_id.budget_type',
        string="Tipe Anggaran",
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        related='budget_id.currency_id',
        string="Mata Uang",
        readonly=True
    )

    annual_target = fields.Monetary(
        string="Target Plafon Tahunan",
        required=True,
        default=0.0,
        currency_field='currency_id'
    )

    # 12-Month Target Distribution Slots
    m1_target = fields.Monetary(string="Jan", currency_field='currency_id')
    m2_target = fields.Monetary(string="Feb", currency_field='currency_id')
    m3_target = fields.Monetary(string="Mar", currency_field='currency_id')
    m4_target = fields.Monetary(string="Apr", currency_field='currency_id')
    m5_target = fields.Monetary(string="Mei", currency_field='currency_id')
    m6_target = fields.Monetary(string="Jun", currency_field='currency_id')
    m7_target = fields.Monetary(string="Jul", currency_field='currency_id')
    m8_target = fields.Monetary(string="Agu", currency_field='currency_id')
    m9_target = fields.Monetary(string="Sep", currency_field='currency_id')
    m10_target = fields.Monetary(string="Okt", currency_field='currency_id')
    m11_target = fields.Monetary(string="Nov", currency_field='currency_id')
    m12_target = fields.Monetary(string="Des", currency_field='currency_id')

    # 12-Month Realized Actuals from General Ledger (account.move.line)
    m1_realized = fields.Monetary(string="Jan (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m2_realized = fields.Monetary(string="Feb (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m3_realized = fields.Monetary(string="Mar (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m4_realized = fields.Monetary(string="Apr (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m5_realized = fields.Monetary(string="Mei (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m6_realized = fields.Monetary(string="Jun (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m7_realized = fields.Monetary(string="Jul (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m8_realized = fields.Monetary(string="Agu (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m9_realized = fields.Monetary(string="Sep (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m10_realized = fields.Monetary(string="Okt (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m11_realized = fields.Monetary(string="Nov (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')
    m12_realized = fields.Monetary(string="Des (Aktual)", compute='_compute_realization', store=True, currency_field='currency_id')

    # YTD Cumulative Metrics
    ytd_realized = fields.Monetary(
        string="Total Realisasi YTD",
        compute='_compute_realization',
        store=True,
        currency_field='currency_id'
    )
    variance_amount = fields.Monetary(
        string="Sisa Plafon / Selisih",
        compute='_compute_realization',
        store=True,
        currency_field='currency_id'
    )
    achievement_pct = fields.Float(
        string="Progress / Rasio (%)",
        compute='_compute_realization',
        store=True
    )
    status = fields.Selection([
        ('healthy', 'Aman'),
        ('warning', 'Waspada'),
        ('critical', 'Over Budget / Kurang')
    ], string="Status", compute='_compute_realization', store=True)

    @api.onchange('annual_target')
    def _onchange_annual_target(self):
        """Bagi rata plafon tahunan ke 12 slot bulan secara proporsional."""
        if self.annual_target:
            monthly_slice = round(self.annual_target / 12.0, 2)
            self.m1_target = monthly_slice
            self.m2_target = monthly_slice
            self.m3_target = monthly_slice
            self.m4_target = monthly_slice
            self.m5_target = monthly_slice
            self.m6_target = monthly_slice
            self.m7_target = monthly_slice
            self.m8_target = monthly_slice
            self.m9_target = monthly_slice
            self.m10_target = monthly_slice
            self.m11_target = monthly_slice
            self.m12_target = monthly_slice

    @api.depends(
        'category_id.account_ids',
        'annual_target',
        'budget_id.fiscal_year',
        'budget_id.company_id'
    )
    def _compute_realization(self):
        """
        Hitung realisasi buku besar aktual dari account.move.line
        untuk masing-masing bulan 1 sampai 12 pada tahun fiskal terkait.
        """
        MoveLine = self.env['account.move.line']
        for rec in self:
            year = rec.budget_id.fiscal_year or date.today().year
            company = rec.budget_id.company_id
            accounts = rec.category_id.account_ids

            monthly_actuals = [0.0] * 12
            if accounts and company:
                for m in range(1, 13):
                    _, last_day = monthrange(year, m)
                    d_from = date(year, m, 1)
                    d_to = date(year, m, last_day)

                    lines = MoveLine.search([
                        ('account_id', 'in', accounts.ids),
                        ('company_id', '=', company.id),
                        ('parent_state', '=', 'posted'),
                        ('date', '>=', d_from),
                        ('date', '<=', d_to)
                    ])

                    if rec.budget_type == 'expense':
                        # Untuk beban: Debit menambah pengeluaran, Credit mengurangi
                        val = sum(lines.mapped('debit')) - sum(lines.mapped('credit'))
                    else:
                        # Untuk pendapatan: Credit menambah omset, Debit mengurangi
                        val = sum(lines.mapped('credit')) - sum(lines.mapped('debit'))

                    monthly_actuals[m - 1] = max(val, 0.0)

            rec.m1_realized = monthly_actuals[0]
            rec.m2_realized = monthly_actuals[1]
            rec.m3_realized = monthly_actuals[2]
            rec.m4_realized = monthly_actuals[3]
            rec.m5_realized = monthly_actuals[4]
            rec.m6_realized = monthly_actuals[5]
            rec.m7_realized = monthly_actuals[6]
            rec.m8_realized = monthly_actuals[7]
            rec.m9_realized = monthly_actuals[8]
            rec.m10_realized = monthly_actuals[9]
            rec.m11_realized = monthly_actuals[10]
            rec.m12_realized = monthly_actuals[11]

            tot_actual = sum(monthly_actuals)
            rec.ytd_realized = tot_actual

            target = rec.annual_target or 0.0
            if rec.budget_type == 'expense':
                rec.variance_amount = target - tot_actual
                pct = (tot_actual / target * 100.0) if target > 0 else 0.0
                rec.achievement_pct = round(pct, 1)

                if pct > 100.0:
                    rec.status = 'critical'
                elif pct > 85.0:
                    rec.status = 'warning'
                else:
                    rec.status = 'healthy'
            else:
                rec.variance_amount = tot_actual - target
                pct = (tot_actual / target * 100.0) if target > 0 else 0.0
                rec.achievement_pct = round(pct, 1)

                if pct >= 100.0:
                    rec.status = 'healthy'
                elif pct >= 75.0:
                    rec.status = 'warning'
                else:
                    rec.status = 'critical'
