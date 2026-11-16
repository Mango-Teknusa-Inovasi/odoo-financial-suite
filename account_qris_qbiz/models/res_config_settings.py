# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    qris_mode = fields.Selection(
        related='company_id.qris_mode',
        readonly=False,
        string="QRIS Operating Mode"
    )

    qris_static_payload = fields.Text(
        related='company_id.qris_static_payload',
        readonly=False,
        string="Static QRIS Payload"
    )

    qris_merchant_name = fields.Char(
        related='company_id.qris_merchant_name',
        readonly=False,
        string="QRIS Merchant Name"
    )

    qris_merchant_city = fields.Char(
        related='company_id.qris_merchant_city',
        readonly=False,
        string="QRIS Merchant City"
    )

    qris_default_journal_id = fields.Many2one(
        related='company_id.qris_default_journal_id',
        readonly=False,
        string="QRIS Settlement Journal"
    )

    qbiz_base_url = fields.Char(
        related='company_id.qbiz_base_url',
        readonly=False,
        string="QBiz Base URL"
    )

    qbiz_api_key = fields.Char(
        related='company_id.qbiz_api_key',
        readonly=False,
        string="QBiz API Key"
    )

    qbiz_merchant_id = fields.Char(
        related='company_id.qbiz_merchant_id',
        readonly=False,
        string="QBiz Merchant ID"
    )

    qbiz_webhook_secret = fields.Char(
        related='company_id.qbiz_webhook_secret',
        readonly=False,
        string="QBiz Webhook Secret"
    )

    qbiz_auto_reconcile = fields.Boolean(
        related='company_id.qbiz_auto_reconcile',
        readonly=False,
        string="Auto-Reconcile Invoices"
    )
