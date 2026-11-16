# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    qris_mode = fields.Selection([
        ('standalone', 'Standalone Local Engine (Offline)'),
        ('qbiz_api', 'Connected to QBiz Server / API'),
    ], string="QRIS Operating Mode", default='standalone', required=True,
       help="Choose whether to generate dynamic QRIS offline locally or connect to a QBiz middleware server for automatic mutation matching.")

    qris_static_payload = fields.Text(
        string="Static QRIS Payload",
        help="Raw static QRIS string (starting with 000201010211...) obtained from your Indonesian merchant provider (BCA, Mandiri, GoPay, DANA, etc.)."
    )

    qris_merchant_name = fields.Char(
        string="QRIS Merchant Name",
        help="Merchant trade name displayed on the dynamic QRIS interface."
    )

    qris_merchant_city = fields.Char(
        string="QRIS Merchant City",
        help="City of operations conforming to ASPI standards (e.g. Jakarta, Surabaya)."
    )

    qris_default_journal_id = fields.Many2one(
        'account.journal',
        string="QRIS Settlement Journal",
        domain="[('type', 'in', ('bank', 'cash'))]",
        help="Bank or Cash journal where dynamic QRIS payments will be deposited upon settlement or auto-reconciliation."
    )

    # QBiz Middleware API Credentials
    qbiz_base_url = fields.Char(
        string="QBiz Base URL",
        default="http://localhost:8000",
        help="Endpoint of the running QBiz middleware server (e.g. http://localhost:8000 or https://qbiz.yourdomain.com)."
    )

    qbiz_api_key = fields.Char(
        string="QBiz API Key",
        help="Secret API Key generated from QBiz Developer Hub dashboard."
    )

    qbiz_merchant_id = fields.Char(
        string="QBiz Merchant ID",
        default="mrc_toko_1",
        help="Identifier of the target merchant profile configured inside QBiz."
    )

    qbiz_webhook_secret = fields.Char(
        string="QBiz Webhook Secret",
        help="Shared secret token used to verify inbound webhook requests from QBiz."
    )

    qbiz_auto_reconcile = fields.Boolean(
        string="Auto-Reconcile Invoices",
        default=True,
        help="When enabled, inbound webhook payment notifications from QBiz will automatically register payment and mark invoices as PAID."
    )
