# -*- coding: utf-8 -*-
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .qris_emvco import generate_dynamic_qris, generate_qr_image_base64, DEFAULT_MOCK_STATIC_QRIS

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    qris_payload = fields.Text(
        string="Dynamic QRIS Payload",
        copy=False,
        help="Raw dynamic EMVCo QRIS string encoding the exact invoice nominal amount."
    )

    qris_image = fields.Binary(
        string="QRIS QR Code",
        copy=False,
        attachment=True,
        help="Scannable 2D barcode image of the dynamic QRIS payload."
    )

    qris_status = fields.Selection([
        ('none', 'Not Generated'),
        ('pending', 'Waiting for Payment'),
        ('paid', 'Paid / Reconciled'),
        ('expired', 'Expired'),
    ], string="QRIS Status", default='none', copy=False, tracking=True)

    qris_unique_code = fields.Integer(
        string="QBiz Unique Suffix",
        default=0,
        copy=False,
        help="3-digit anti-collision suffix appended by QBiz middleware to uniquely match bank mutations."
    )

    qris_total_amount = fields.Monetary(
        string="QRIS Payable Amount",
        currency_field='currency_id',
        copy=False,
        help="Exact amount to be paid by the customer including the unique anti-collision code."
    )

    qris_invoice_id = fields.Char(
        string="QBiz Transaction ID",
        copy=False,
        help="Reference ID returned by QBiz middleware (e.g. inv_1785738263024_587)."
    )

    qris_checkout_url = fields.Char(
        string="QBiz Checkout URL",
        copy=False,
        help="Hosted mobile checkout link with real-time countdown timer."
    )

    qris_expiry_date = fields.Datetime(
        string="QRIS Expiration",
        copy=False,
        help="Timestamp when the dynamic QRIS transaction expires."
    )

    def action_generate_dynamic_qris(self):
        """
        Generate dynamic QRIS for customer invoice adhering to active company mode.
        """
        for move in self:
            if move.move_type not in ('out_invoice', 'out_refund'):
                continue
            if move.state != 'posted':
                raise UserError(_("Please post the invoice before generating a dynamic QRIS payment."))
            if move.payment_state in ('paid', 'in_payment'):
                raise UserError(_("This invoice is already paid."))

            company = move.company_id
            payable_nominal = move.amount_residual or move.amount_total

            if company.qris_mode == 'standalone':
                # Mode A: Pure Python Local EMVCo Engine
                raw_static = company.qris_static_payload or DEFAULT_MOCK_STATIC_QRIS
                dynamic_str = generate_dynamic_qris(raw_static, payable_nominal)
                
                qr_base64 = generate_qr_image_base64(dynamic_str)
                move.write({
                    'qris_payload': dynamic_str,
                    'qris_image': qr_base64,
                    'qris_status': 'pending',
                    'qris_unique_code': 0,
                    'qris_total_amount': payable_nominal,
                    'qris_expiry_date': fields.Datetime.now() + timedelta(minutes=15),
                })
                move.message_post(body=_(
                    "<b>Dynamic QRIS Generated (Standalone Local Engine)</b><br/>"
                    "• Amount: %s %s<br/>"
                    "• Status: Waiting for customer payment scan."
                ) % (move.currency_id.symbol or "Rp", f"{payable_nominal:,.0f}"))

            elif company.qris_mode == 'qbiz_api':
                # Mode B: Connected to QBiz Middleware Server
                move._generate_qbiz_api_qris(payable_nominal)

        return True

    def _generate_qbiz_api_qris(self, payable_nominal):
        """Call QBiz REST API to generate an invoice with anti-collision unique code."""
        self.ensure_one()
        company = self.company_id
        
        base_url = (company.qbiz_base_url or "http://localhost:8000").rstrip("/")
        api_url = f"{base_url}/api/v1/invoices"
        
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', 'http://localhost:8069')
        callback_url = f"{web_base_url.rstrip('/')}/api/v1/webhook/qris"
        
        req_data = {
            "amount": int(round(payable_nominal)),
            "order_id": self.name or f"INV-{self.id}",
            "merchant_id": company.qbiz_merchant_id or "mrc_toko_1",
            "customer_name": self.partner_id.name or "Pelanggan",
            "customer_phone": self.partner_id.phone or self.partner_id.mobile or "",
            "customer_email": self.partner_id.email or "",
            "callback_url": callback_url,
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {company.qbiz_api_key or ''}"
        }
        
        try:
            req = urllib.request.Request(
                api_url,
                data=json.dumps(req_data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = json.loads(response.read().decode('utf-8'))
                
            if res_body.get('success'):
                inv_data = res_body.get('invoice', {})
                qris_payload = inv_data.get('qris_payload', '')
                qr_base64 = generate_qr_image_base64(qris_payload)
                
                self.write({
                    'qris_payload': qris_payload,
                    'qris_image': qr_base64,
                    'qris_status': 'pending',
                    'qris_invoice_id': inv_data.get('id', ''),
                    'qris_unique_code': inv_data.get('unique_code', 0),
                    'qris_total_amount': inv_data.get('total_amount', payable_nominal),
                    'qris_checkout_url': inv_data.get('checkout_url', ''),
                    'qris_expiry_date': fields.Datetime.now() + timedelta(minutes=5),
                })
                
                self.message_post(body=_(
                    "<b>QBiz Dynamic QRIS Invoice Created</b><br/>"
                    "• Transaction ID: <code>%s</code><br/>"
                    "• Base Amount: Rp %s<br/>"
                    "• Unique Anti-Collision Code: +%s<br/>"
                    "• <b>Total Payable: Rp %s</b><br/>"
                    "• Checkout URL: <a href='%s' target='_blank'>%s</a>"
                ) % (
                    inv_data.get('id'),
                    f"{payable_nominal:,.0f}",
                    inv_data.get('unique_code', 0),
                    f"{inv_data.get('total_amount', payable_nominal):,.0f}",
                    inv_data.get('checkout_url'),
                    inv_data.get('checkout_url')
                ))
            else:
                raise UserError(_("QBiz API Error: %s") % res_body.get('message', 'Unknown response'))
        except Exception as e:
            _logger.exception("Failed to connect to QBiz API: %s", e)
            # Graceful fallback to standalone engine
            raw_static = company.qris_static_payload or DEFAULT_MOCK_STATIC_QRIS
            dynamic_str = generate_dynamic_qris(raw_static, payable_nominal)
            qr_base64 = generate_qr_image_base64(dynamic_str)
            self.write({
                'qris_payload': dynamic_str,
                'qris_image': qr_base64,
                'qris_status': 'pending',
                'qris_unique_code': 0,
                'qris_total_amount': payable_nominal,
                'qris_expiry_date': fields.Datetime.now() + timedelta(minutes=15),
            })
            self.message_post(body=_(
                "<b>QBiz API unreachable (%s). Fallback to Standalone Local Engine.</b>"
            ) % str(e))

    def action_qris_mark_paid(self, settlement_journal=None, external_ref=None):
        """
        Register payment and reconcile invoice automatically upon QRIS settlement.
        """
        self.ensure_one()
        if self.payment_state in ('paid', 'in_payment'):
            return True

        journal = settlement_journal or self.company_id.qris_default_journal_id
        if not journal:
            # Fallback to first active bank/cash journal
            journal = self.env['account.journal'].search([
                ('company_id', '=', self.company_id.id),
                ('type', 'in', ('bank', 'cash'))
            ], limit=1)

        if not journal:
            raise UserError(_("No active Bank or Cash journal found for QRIS settlement."))

        payment_amount = self.amount_residual or self.amount_total
        payment_method_line = journal.inbound_payment_method_line_ids[:1]

        # Register payment via standard Odoo payment register wizard
        payment_register = self.env['account.payment.register'].with_context(
            active_model='account.move',
            active_ids=self.ids
        ).create({
            'journal_id': journal.id,
            'amount': payment_amount,
            'payment_date': fields.Date.context_today(self),
            'payment_method_line_id': payment_method_line.id if payment_method_line else False,
            'communication': f"QRIS {self.name} {external_ref or self.qris_invoice_id or ''}".strip(),
        })

        payment_register.action_create_payments()

        self.write({
            'qris_status': 'paid',
        })

        self.message_post(body=_(
            "<b>🎉 Dynamic QRIS Payment Settled & Reconciled!</b><br/>"
            "• Amount: %s %s<br/>"
            "• Settlement Journal: %s<br/>"
            "• Invoice is now marked as PAID."
        ) % (self.currency_id.symbol or "Rp", f"{payment_amount:,.0f}", journal.name))

        return True

    def action_post(self):
        """Auto-generate dynamic QRIS upon invoice confirmation if configured."""
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.move_type == 'out_invoice' and move.amount_residual > 0:
                try:
                    move.action_generate_dynamic_qris()
                except Exception as e:
                    _logger.warning("Auto QRIS generation skipped for %s: %s", move.name, e)
        return res
