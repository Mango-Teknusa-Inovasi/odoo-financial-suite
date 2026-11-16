# -*- coding: utf-8 -*-
import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class QBizQRISWebhookController(http.Controller):

    @http.route('/api/v1/webhook/qris', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_qris_webhook_json(self, **kwargs):
        """
        Inbound webhook endpoint for QBiz Dynamic QRIS middleware.
        Receives notification when a bank/e-wallet mutation is matched to an active invoice.
        """
        try:
            data = request.jsonrequest or {}
            _logger.info("QBiz QRIS Webhook Received: %s", data)
            return self._process_webhook_payload(data)
        except Exception as e:
            _logger.exception("Error processing QBiz QRIS Webhook: %s", e)
            return {"success": False, "error": str(e)}

    @http.route('/api/v1/webhook/qris/http', type='http', auth='public', methods=['POST'], csrf=False)
    def handle_qris_webhook_http(self, **post):
        """
        Alternative HTTP POST endpoint accepting raw body.
        """
        try:
            raw_body = request.httprequest.data.decode('utf-8')
            data = json.loads(raw_body) if raw_body else post
            _logger.info("QBiz QRIS HTTP Webhook Received: %s", data)
            result = self._process_webhook_payload(data)
            return request.make_response(
                json.dumps(result),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            _logger.exception("Error processing QBiz QRIS HTTP Webhook: %s", e)
            return request.make_response(
                json.dumps({"success": False, "error": str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=400
            )

    def _process_webhook_payload(self, data):
        """
        Locates the target customer invoice and auto-reconciles payment.
        """
        order_id = data.get('order_id')
        invoice_id = data.get('invoice_id') or data.get('id')
        status = data.get('status', '').upper()
        amount = data.get('amount')

        if not order_id and not invoice_id:
            return {"success": False, "message": "Missing order_id or invoice_id"}

        # Search matching invoice
        domain = ['|', ('name', '=', order_id), ('qris_invoice_id', '=', invoice_id)]
        move = request.env['account.move'].sudo().search(domain, limit=1)

        if not move:
            _logger.warning("QBiz Webhook: No matching invoice found for order_id=%s, invoice_id=%s", order_id, invoice_id)
            return {"success": False, "message": "Invoice not found"}

        if move.payment_state in ('paid', 'in_payment'):
            return {"success": True, "message": "Invoice already settled"}

        if status in ('PAID', 'SUCCESS', 'SETTLED'):
            try:
                move.action_qris_mark_paid(external_ref=invoice_id)
                return {
                    "success": True,
                    "reconciled": True,
                    "invoice_number": move.name,
                    "message": "Payment registered and reconciled successfully"
                }
            except Exception as e:
                _logger.exception("Failed to auto-reconcile invoice %s: %s", move.name, e)
                return {"success": False, "error": str(e)}
        else:
            _logger.info("QBiz Webhook: Received non-paid status '%s' for invoice %s", status, move.name)
            return {"success": True, "message": f"Status '{status}' acknowledged"}
