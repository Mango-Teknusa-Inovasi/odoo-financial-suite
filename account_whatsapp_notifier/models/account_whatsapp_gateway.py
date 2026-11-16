# -*- coding: utf-8 -*-
import json
import urllib.parse
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountWhatsAppGateway(models.AbstractModel):
    _name = 'account.whatsapp.gateway'
    _description = 'WhatsApp Gateway Dispatcher Engine'

    @api.model
    def dispatch_message(self, move, phone, message, attach_pdf=True, device_id=None):
        """
        Route message dispatch to the configured provider: GOWA, Meta Official, or Click-to-Chat.
        """
        company = move.company_id if move else self.env.company
        provider = company.whatsapp_provider or 'click_to_chat'

        if provider == 'gowa':
            return self._dispatch_gowa(move, phone, message, attach_pdf=attach_pdf, device_id=device_id)
        elif provider == 'meta_official':
            return self._dispatch_meta(move, phone, message)
        elif provider == 'custom_api':
            return self._dispatch_custom(move, phone, message)
        else:
            return self._dispatch_click_to_chat(phone, message)

    @api.model
    def _dispatch_click_to_chat(self, phone, message):
        """
        Generate direct client-side WhatsApp Web click-to-chat URL.
        """
        clean_phone = self.env['res.partner'].clean_whatsapp_number(phone)
        encoded_text = urllib.parse.quote(message or '')
        url = f"https://wa.me/{clean_phone}?text={encoded_text}"
        return {
            'success': True,
            'mode': 'click_to_chat',
            'url': url,
            'message': _('Tautan WhatsApp Web berhasil dibuat.'),
        }

    @api.model
    def _dispatch_gowa(self, move, phone, message, attach_pdf=True, device_id=None):
        """
        Send text or binary PDF file via aldinokemal/go-whatsapp-web-multidevice REST API.
        """
        company = move.company_id if move else self.env.company
        server_url = (company.gowa_server_url or 'http://localhost:3000').rstrip('/')
        clean_phone = self.env['res.partner'].clean_whatsapp_number(phone)

        if not clean_phone:
            raise UserError(_("Nomor WhatsApp penerima tidak valid: %s") % phone)

        headers = {}
        target_device = device_id or company.gowa_device_id
        if target_device:
            headers['X-Device-Id'] = str(target_device).strip()

        auth = None
        if company.gowa_username and company.gowa_password:
            auth = (company.gowa_username, company.gowa_password)

        target_jid = f"{clean_phone}@s.whatsapp.net"

        try:
            # Mode A: Send PDF invoice directly as file attachment
            if attach_pdf and move:
                endpoint = f"{server_url}/send/file"
                report_action = self.env.ref('account.account_invoices', raise_if_not_found=False)
                pdf_bin = False
                if report_action:
                    pdf_bin, _ = self.env['ir.actions.report']._render_qweb_pdf(report_action, [move.id])

                if pdf_bin:
                    clean_name = (move.name or 'Invoice').replace('/', '_')
                    files = {
                        'file': (f"{clean_name}.pdf", pdf_bin, 'application/pdf')
                    }
                    data = {
                        'phone': target_jid,
                        'caption': message or ''
                    }
                    resp = requests.post(endpoint, data=data, files=files, headers=headers, auth=auth, timeout=20)
                else:
                    # Fallback to text message if PDF rendering returns empty
                    endpoint = f"{server_url}/send/message"
                    headers['Content-Type'] = 'application/json'
                    payload = {'phone': target_jid, 'message': message or ''}
                    resp = requests.post(endpoint, json=payload, headers=headers, auth=auth, timeout=15)
            else:
                # Mode B: Send plain text message
                endpoint = f"{server_url}/send/message"
                headers['Content-Type'] = 'application/json'
                payload = {'phone': target_jid, 'message': message or ''}
                resp = requests.post(endpoint, json=payload, headers=headers, auth=auth, timeout=15)

            if resp.status_code in (200, 201):
                res_data = resp.json() if resp.text else {}
                return {
                    'success': True,
                    'mode': 'gowa',
                    'response': res_data,
                    'message': _('Pesan berhasil terkirim melalui server GOWA.')
                }
            else:
                return {
                    'success': False,
                    'mode': 'gowa',
                    'error': f"HTTP {resp.status_code}: {resp.text}",
                    'fallback_url': self._dispatch_click_to_chat(phone, message)['url'],
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'mode': 'gowa',
                'error': str(e),
                'fallback_url': self._dispatch_click_to_chat(phone, message)['url'],
            }

    @api.model
    def _dispatch_meta(self, move, phone, message):
        """
        Meta Official WhatsApp Cloud API Dispatcher placeholder.
        """
        clean_phone = self.env['res.partner'].clean_whatsapp_number(phone)
        company = move.company_id if move else self.env.company
        phone_id = company.meta_phone_number_id
        token = company.meta_token

        if not phone_id or not token:
            return {
                'success': False,
                'mode': 'meta_official',
                'error': _('Konfigurasi Meta WhatsApp Cloud API belum lengkap (Phone ID / Token kosong).'),
                'fallback_url': self._dispatch_click_to_chat(phone, message)['url'],
            }

        endpoint = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
        headers = {
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json'
        }
        payload = {
            'messaging_product': 'whatsapp',
            'to': clean_phone,
            'type': 'text',
            'text': {'body': message or ''}
        }
        try:
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=15)
            if resp.status_code in (200, 201):
                return {'success': True, 'mode': 'meta_official', 'response': resp.json()}
            return {
                'success': False,
                'mode': 'meta_official',
                'error': f"HTTP {resp.status_code}: {resp.text}",
                'fallback_url': self._dispatch_click_to_chat(phone, message)['url']
            }
        except Exception as e:
            return {
                'success': False,
                'mode': 'meta_official',
                'error': str(e),
                'fallback_url': self._dispatch_click_to_chat(phone, message)['url']
            }

    @api.model
    def _dispatch_custom(self, move, phone, message):
        """
        Custom Webhook / Third-Party Gateway Dispatcher (Fonnte, Wablas, etc.)
        """
        company = move.company_id if move else self.env.company
        endpoint = company.custom_webhook_url
        if not endpoint:
            return {
                'success': False,
                'mode': 'custom_api',
                'error': _('URL Webhook Kustom belum dikonfigurasi.'),
                'fallback_url': self._dispatch_click_to_chat(phone, message)['url'],
            }

        clean_phone = self.env['res.partner'].clean_whatsapp_number(phone)
        headers = {'Content-Type': 'application/json'}
        if company.custom_webhook_token:
            headers['Authorization'] = company.custom_webhook_token

        payload = {
            'target': clean_phone,
            'phone': clean_phone,
            'message': message,
            'invoice_id': move.id if move else False,
            'invoice_name': move.name if move else False,
        }
        try:
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=15)
            return {'success': resp.status_code in (200, 201), 'mode': 'custom_api', 'response': resp.text}
        except Exception as e:
            return {'success': False, 'mode': 'custom_api', 'error': str(e), 'fallback_url': self._dispatch_click_to_chat(phone, message)['url']}

    @api.model
    def test_gowa_connection(self, server_url, username=None, password=None, device_id=None):
        """
        Ping GOWA server to verify reachability and active multi-device session status.
        """
        url = (server_url or 'http://localhost:3000').rstrip('/')
        auth = (username, password) if username and password else None
        headers = {}
        if device_id:
            headers['X-Device-Id'] = str(device_id).strip()

        try:
            # GOWA endpoints for status/devices
            ping_url = f"{url}/app/devices"
            resp = requests.get(ping_url, headers=headers, auth=auth, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return {'success': True, 'message': _('Koneksi GOWA Berhasil! Server aktif dan merespons (HTTP 200).'), 'data': data}
            else:
                return {'success': False, 'message': _('Server GOWA merespons dengan status HTTP %s: %s') % (resp.status_code, resp.text)}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'message': _('Gagal menghubungi server GOWA di %s: %s') % (url, str(e))}
