# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    whatsapp_provider = fields.Selection([
        ('click_to_chat', 'WhatsApp Web / Desktop (Gratis - wa.me)'),
        ('gowa', 'GOWA - go-whatsapp-web-multidevice (Self-Hosted)'),
        ('meta_official', 'Meta WhatsApp Cloud API (Resmi)'),
        ('custom_api', 'Custom REST Webhook (Fonnte / Wablas / Lainnya)'),
    ], string='WhatsApp Engine Provider', default='click_to_chat', required=True)

    # GOWA (aldinokemal/go-whatsapp-web-multidevice) Configuration
    gowa_server_url = fields.Char(
        string='GOWA Server URL',
        default='http://localhost:3000',
        help='URL endpoint server GOWA (contoh: http://localhost:3000 atau http://gowa:3000).'
    )
    gowa_username = fields.Char(string='GOWA Basic Auth User')
    gowa_password = fields.Char(string='GOWA Basic Auth Password')
    gowa_device_id = fields.Char(
        string='GOWA Default Device ID',
        help='Device ID atau nomor HP terhubung pada GOWA multi-device (header X-Device-Id).'
    )
    gowa_attach_pdf = fields.Boolean(
        string='Lampirkan PDF Faktur via GOWA',
        default=True,
        help='Otomatis melampirkan berkas fisik PDF faktur resmi ke chat WhatsApp.'
    )

    # Automated Workflow Settings
    auto_send_on_post = fields.Boolean(
        string='Kirim Otomatis saat Faktur Diposting',
        default=False,
        help='Otomatis mengirimkan WhatsApp via GOWA/API ketika faktur penjualan divalidasi (Posted).'
    )

    # Meta WhatsApp Cloud API Configuration
    meta_phone_number_id = fields.Char(string='Meta Phone Number ID')
    meta_token = fields.Char(string='Meta Access Token')

    # Custom Gateway Configuration
    custom_webhook_url = fields.Char(string='Custom Webhook URL')
    custom_webhook_token = fields.Char(string='Custom Authorization Token')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    whatsapp_provider = fields.Selection(
        related='company_id.whatsapp_provider',
        readonly=False,
        string='WhatsApp Engine'
    )
    gowa_server_url = fields.Char(
        related='company_id.gowa_server_url',
        readonly=False,
        string='GOWA Server Endpoint'
    )
    gowa_username = fields.Char(
        related='company_id.gowa_username',
        readonly=False,
        string='GOWA User'
    )
    gowa_password = fields.Char(
        related='company_id.gowa_password',
        readonly=False,
        string='GOWA Password'
    )
    gowa_device_id = fields.Char(
        related='company_id.gowa_device_id',
        readonly=False,
        string='GOWA Device ID'
    )
    gowa_attach_pdf = fields.Boolean(
        related='company_id.gowa_attach_pdf',
        readonly=False,
        string='Lampirkan PDF Faktur via GOWA'
    )
    auto_send_on_post = fields.Boolean(
        related='company_id.auto_send_on_post',
        readonly=False,
        string='Kirim Otomatis saat Faktur Diposting'
    )
    meta_phone_number_id = fields.Char(
        related='company_id.meta_phone_number_id',
        readonly=False,
        string='Meta Phone Number ID'
    )
    meta_token = fields.Char(
        related='company_id.meta_token',
        readonly=False,
        string='Meta Access Token'
    )
    custom_webhook_url = fields.Char(
        related='company_id.custom_webhook_url',
        readonly=False,
        string='Custom Webhook URL'
    )
    custom_webhook_token = fields.Char(
        related='company_id.custom_webhook_token',
        readonly=False,
        string='Custom Webhook Token'
    )

    def action_test_gowa_connection(self):
        """Action button to test connectivity to GOWA server."""
        self.ensure_one()
        gateway = self.env['account.whatsapp.gateway']
        result = gateway.test_gowa_connection(
            self.gowa_server_url,
            username=self.gowa_username,
            password=self.gowa_password,
            device_id=self.gowa_device_id
        )
        if result.get('success'):
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Koneksi GOWA Berhasil'),
                    'message': result.get('message'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Koneksi GOWA Gagal'),
                    'message': result.get('message'),
                    'type': 'danger',
                    'sticky': True,
                }
            }
