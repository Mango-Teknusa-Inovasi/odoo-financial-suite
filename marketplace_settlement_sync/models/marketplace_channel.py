# -*- coding: utf-8 -*-
from odoo import models, fields

class MarketplaceChannel(models.Model):
    _name = 'marketplace.channel'
    _description = 'Marketplace Sales Channel'

    name = fields.Char(string='Channel Name', required=True)
    platform = fields.Selection([
        ('shopee', 'Shopee'),
        ('tokopedia', 'Tokopedia'),
        ('tiktok', 'TikTok Shop'),
        ('blibli', 'Blibli'),
        ('lazada', 'Lazada'),
        ('custom', 'Other / Custom Platform'),
    ], string='Platform Type', required=True, default='shopee')

    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    # Accounting Mappings
    journal_id = fields.Many2one(
        'account.journal',
        string='Settlement Journal',
        required=True,
        domain="[('company_id', '=', company_id)]",
        help='Journal where marketplace summary entries will be recorded.'
    )
    escrow_account_id = fields.Many2one(
        'account.account',
        string='Clearing / Escrow Account (Asset)',
        required=True,
        help='Transit account representing funds held by the marketplace balance prior to bank disbursement.'
    )
    revenue_account_id = fields.Many2one(
        'account.account',
        string='Sales Revenue Account (Income)',
        required=True,
        help='Account credited for gross product sales turnover.'
    )
    fee_account_id = fields.Many2one(
        'account.account',
        string='Commission & Service Fee Account (Expense)',
        required=True,
        help='Account debited for marketplace transaction fees and seller commissions.'
    )
    shipping_account_id = fields.Many2one(
        'account.account',
        string='Shipping Adjustment Account (Expense)',
        help='Optional account for seller-paid shipping subsidies and logistics adjustments.'
    )
