# -*- coding: utf-8 -*-
try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    from datetime import timedelta
    def relativedelta(months=0, **kwargs):
        return timedelta(days=int(months * 30.4375))

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountSimpleAsset(models.Model):
    _name = 'account.simple.asset'
    _description = 'Lightweight Fixed Asset Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'acquisition_date desc, id desc'

    name = fields.Char(string='Asset Name', required=True, tracking=True)
    code = fields.Char(string='Asset Code or Serial')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string='Currency',
        readonly=True
    )
    
    # Indonesian Tax Classification (UU PPh Pasal 11)
    asset_group = fields.Selection([
        ('group_1', 'Kelompok 1 (4 Tahun: 25% Garis Lurus)'),
        ('group_2', 'Kelompok 2 (8 Tahun: 12.5% Garis Lurus)'),
        ('group_3', 'Kelompok 3 (16 Tahun: 6.25% Garis Lurus)'),
        ('group_4', 'Kelompok 4 (20 Tahun: 5% Garis Lurus)'),
        ('building_permanent', 'Bangunan Permanen (20 Tahun: 5%)'),
        ('building_non_permanent', 'Bangunan Tidak Permanen (10 Tahun: 10%)'),
        ('custom', 'Kustom (Berdasarkan Masa Manfaat Mandiri)'),
    ], string='Tax Category (PPh 11)', default='group_1', required=True, tracking=True)

    acquisition_date = fields.Date(string='Acquisition Date', required=True, default=fields.Date.context_today)
    start_depreciation_date = fields.Date(string='Depreciation Start Date', required=True, default=fields.Date.context_today)
    useful_life_months = fields.Integer(string='Useful Life (Months)', compute='_compute_useful_life', store=True, readonly=False)

    original_cost = fields.Monetary(string='Acquisition Cost', currency_field='currency_id', required=True, tracking=True)
    salvage_value = fields.Monetary(string='Salvage Value', currency_field='currency_id', default=0.0)
    past_accumulated_depreciation = fields.Monetary(
        string='Past Accumulated Depreciation',
        currency_field='currency_id',
        default=0.0,
        help='Accumulated depreciation already recognized prior to cut-off date.'
    )
    net_book_value = fields.Monetary(
        string='Net Book Value (NBV)',
        currency_field='currency_id',
        compute='_compute_depreciation_values',
        store=True
    )
    monthly_depreciation = fields.Monetary(
        string='Monthly Depreciation',
        currency_field='currency_id',
        compute='_compute_depreciation_values',
        store=True
    )

    asset_account_id = fields.Many2one('account.account', string='Asset Account', domain="[('deprecated', '=', False)]")
    accumulated_account_id = fields.Many2one('account.account', string='Accumulated Depreciation Account', domain="[('deprecated', '=', False)]")
    expense_account_id = fields.Many2one('account.account', string='Depreciation Expense Account', domain="[('deprecated', '=', False)]")

    line_ids = fields.One2many('account.simple.asset.depreciation.line', 'asset_id', string='Depreciation Schedule', copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Active / Running'),
        ('closed', 'Fully Depreciated / Disposed')
    ], string='Status', default='draft', tracking=True)

    @api.depends('asset_group')
    def _compute_useful_life(self):
        # Default useful life in months aligned with Indonesian statutory tax groups
        group_months_map = {
            'group_1': 48,
            'group_2': 96,
            'group_3': 192,
            'group_4': 240,
            'building_permanent': 240,
            'building_non_permanent': 120,
        }
        for asset in self:
            if asset.asset_group in group_months_map:
                asset.useful_life_months = group_months_map[asset.asset_group]
            elif not asset.useful_life_months:
                asset.useful_life_months = 48

    @api.depends('original_cost', 'salvage_value', 'past_accumulated_depreciation', 'useful_life_months')
    def _compute_depreciation_values(self):
        for asset in self:
            asset.net_book_value = max(0.0, asset.original_cost - asset.past_accumulated_depreciation)
            depreciable_base = max(0.0, asset.original_cost - asset.salvage_value)
            if asset.useful_life_months > 0:
                asset.monthly_depreciation = round(depreciable_base / asset.useful_life_months, 2)
            else:
                asset.monthly_depreciation = 0.0

    def action_compute_board(self):
        """Generate future straight-line monthly depreciation schedule lines."""
        self.ensure_one()
        if self.useful_life_months <= 0:
            raise ValidationError(_("Useful life must be greater than zero months."))
        if self.original_cost <= 0:
            raise ValidationError(_("Asset acquisition cost must be greater than zero."))

        # Clear existing unposted lines
        self.line_ids.unlink()

        depreciable_base = self.original_cost - self.salvage_value
        monthly_rate = round(depreciable_base / self.useful_life_months, 2)
        accumulated = self.past_accumulated_depreciation
        remaining = self.net_book_value
        start_date = self.start_depreciation_date or fields.Date.today()

        # Calculate remaining months based on past accumulated depreciation
        months_consumed = int(accumulated // monthly_rate) if monthly_rate > 0 else 0
        months_remaining = max(1, self.useful_life_months - months_consumed)

        lines_to_create = []
        for i in range(months_remaining):
            sched_date = start_date + relativedelta(months=i)
            # Final month absorbs any rounding discrepancy
            if i == months_remaining - 1 or remaining <= monthly_rate:
                current_dep = remaining
            else:
                current_dep = monthly_rate

            accumulated += current_dep
            remaining = max(0.0, remaining - current_dep)

            lines_to_create.append({
                'asset_id': self.id,
                'schedule_date': sched_date,
                'depreciation_amount': current_dep,
                'cumulative_depreciation': accumulated,
                'remaining_value': remaining,
            })
            if remaining <= 0:
                break

        self.env['account.simple.asset.depreciation.line'].create(lines_to_create)
        self.state = 'running'
        return True

class AccountSimpleAssetDepreciationLine(models.Model):
    _name = 'account.simple.asset.depreciation.line'
    _description = 'Asset Depreciation Schedule Line'
    _order = 'schedule_date asc, id asc'

    asset_id = fields.Many2one('account.simple.asset', string='Asset', required=True, ondelete='cascade')
    currency_id = fields.Many2one('res.currency', related='asset_id.currency_id')
    schedule_date = fields.Date(string='Schedule Date', required=True)
    depreciation_amount = fields.Monetary(string='Monthly Depreciation', currency_field='currency_id', required=True)
    cumulative_depreciation = fields.Monetary(string='Cumulative Depreciation', currency_field='currency_id')
    remaining_value = fields.Monetary(string='Remaining Book Value', currency_field='currency_id')
    move_id = fields.Many2one('account.move', string='Journal Entry', readonly=True)
    is_posted = fields.Boolean(string='Posted', default=False, readonly=True)
