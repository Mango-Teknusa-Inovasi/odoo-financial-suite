# -*- coding: utf-8 -*-
from odoo import models, fields

class MarketplaceSettlementLine(models.Model):
    _name = 'marketplace.settlement.line'
    _description = 'Marketplace Settlement Order Line'
    _order = 'order_date desc, id desc'

    batch_id = fields.Many2one(
        'marketplace.settlement.batch',
        string='Settlement Batch',
        required=True,
        ondelete='cascade',
        index=True
    )
    company_id = fields.Many2one(
        related='batch_id.company_id',
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        related='batch_id.currency_id',
        string='Currency',
        readonly=True
    )

    order_ref = fields.Char(string='Order ID / No. Pesanan', required=True, index=True)
    order_date = fields.Date(string='Order Date')
    customer_name = fields.Char(string='Buyer / Customer')

    gross_amount = fields.Monetary(string='Gross Sales (DPP)', default=0.0)
    service_fee = fields.Monetary(string='Service & Admin Fee', default=0.0)
    shipping_fee = fields.Monetary(string='Shipping Fee Deduction', default=0.0)
    net_amount = fields.Monetary(string='Net Settlement Amount', default=0.0)

    notes = fields.Char(string='Notes / Category')
