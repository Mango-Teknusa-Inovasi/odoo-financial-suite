# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountOpeningCashLine(models.TransientModel):
    _name = 'account.opening.cash.line'
    _description = 'Opening Balance Cash and Bank Line'

    wizard_id = fields.Many2one('account.opening.balance.wizard', string='Wizard Reference', required=True, ondelete='cascade')
    journal_id = fields.Many2one(
        'account.journal',
        string='Bank or Cash Journal',
        required=True,
        domain="[('type', 'in', ('bank', 'cash'))]"
    )
    account_id = fields.Many2one(
        'account.account',
        string='GL Account',
        required=True,
        domain="[('deprecated', '=', False)]"
    )
    amount = fields.Monetary(string='Opening Balance (Saldo Awal)', required=True)
    currency_id = fields.Many2one('res.currency', related='wizard_id.currency_id')

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if self.journal_id and self.journal_id.default_account_id:
            self.account_id = self.journal_id.default_account_id

class AccountOpeningReceivableLine(models.TransientModel):
    _name = 'account.opening.receivable.line'
    _description = 'Opening Balance Customer Receivable Line'

    wizard_id = fields.Many2one('account.opening.balance.wizard', string='Wizard Reference', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer (Pelanggan)', required=True)
    invoice_ref = fields.Char(string='Old Invoice Ref (No. Faktur)', required=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.context_today)
    due_date = fields.Date(string='Due Date (Jatuh Tempo)', default=fields.Date.context_today)
    amount = fields.Monetary(string='Unpaid Amount (Sisa Piutang)', required=True)
    currency_id = fields.Many2one('res.currency', related='wizard_id.currency_id')

class AccountOpeningPayableLine(models.TransientModel):
    _name = 'account.opening.payable.line'
    _description = 'Opening Balance Vendor Payable Line'

    wizard_id = fields.Many2one('account.opening.balance.wizard', string='Wizard Reference', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Vendor (Pemasok)', required=True)
    bill_ref = fields.Char(string='Vendor Bill Ref (No. Tagihan)', required=True)
    bill_date = fields.Date(string='Bill Date', default=fields.Date.context_today)
    due_date = fields.Date(string='Due Date (Jatuh Tempo)', default=fields.Date.context_today)
    amount = fields.Monetary(string='Unpaid Amount (Sisa Hutang)', required=True)
    currency_id = fields.Many2one('res.currency', related='wizard_id.currency_id')

class AccountOpeningStockLine(models.TransientModel):
    _name = 'account.opening.stock.line'
    _description = 'Opening Balance Inventory Stock Line'

    wizard_id = fields.Many2one('account.opening.balance.wizard', string='Wizard Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True, domain="[('type', '=', 'consu')]")
    location_id = fields.Many2one('stock.location', string='Warehouse Location', domain="[('usage', '=', 'internal')]")
    quantity = fields.Float(string='Physical Quantity', required=True, default=1.0)
    unit_cost = fields.Monetary(string='Unit Cost (HPP)', currency_field='currency_id', required=True)
    total_value = fields.Monetary(string='Total Valuation', currency_field='currency_id', compute='_compute_total_value', store=True)
    currency_id = fields.Many2one('res.currency', related='wizard_id.currency_id')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_cost = self.product_id.standard_price

    @api.depends('quantity', 'unit_cost')
    def _compute_total_value(self):
        for line in self:
            line.total_value = round(line.quantity * line.unit_cost, 2)

class AccountOpeningAssetWizardLine(models.TransientModel):
    _name = 'account.opening.asset.wizard.line'
    _description = 'Opening Balance Fixed Asset Line'

    wizard_id = fields.Many2one('account.opening.balance.wizard', string='Wizard Reference', required=True, ondelete='cascade')
    name = fields.Char(string='Asset Name (Nama Aktiva Tetap)', required=True)
    asset_group = fields.Selection([
        ('group_1', 'Kelompok 1 (4 Tahun: 25% Garis Lurus)'),
        ('group_2', 'Kelompok 2 (8 Tahun: 12.5% Garis Lurus)'),
        ('group_3', 'Kelompok 3 (16 Tahun: 6.25% Garis Lurus)'),
        ('group_4', 'Kelompok 4 (20 Tahun: 5% Garis Lurus)'),
        ('building_permanent', 'Bangunan Permanen (20 Tahun: 5%)'),
        ('building_non_permanent', 'Bangunan Tidak Permanen (10 Tahun: 10%)'),
        ('custom', 'Kustom'),
    ], string='Tax Category (PPh 11)', default='group_1', required=True)

    acquisition_date = fields.Date(string='Acquisition Date', required=True, default=fields.Date.context_today)
    original_cost = fields.Monetary(string='Acquisition Cost (Harga Perolehan)', currency_field='currency_id', required=True)
    past_accumulated_depreciation = fields.Monetary(string='Past Acc. Depreciation', currency_field='currency_id', default=0.0)
    net_book_value = fields.Monetary(string='Net Book Value (Nilai Buku)', currency_field='currency_id', compute='_compute_nbv', store=True)
    currency_id = fields.Many2one('res.currency', related='wizard_id.currency_id')

    asset_account_id = fields.Many2one('account.account', string='Asset Account', domain="[('deprecated', '=', False)]")
    accumulated_account_id = fields.Many2one('account.account', string='Accumulated Account', domain="[('deprecated', '=', False)]")
    expense_account_id = fields.Many2one('account.account', string='Expense Account', domain="[('deprecated', '=', False)]")

    @api.depends('original_cost', 'past_accumulated_depreciation')
    def _compute_nbv(self):
        for line in self:
            line.net_book_value = max(0.0, line.original_cost - line.past_accumulated_depreciation)
