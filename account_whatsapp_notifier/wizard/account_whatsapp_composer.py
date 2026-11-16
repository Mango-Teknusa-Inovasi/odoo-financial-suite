# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountWhatsAppComposer(models.TransientModel):
    _name = 'account.whatsapp.composer'
    _description = 'Interactive WhatsApp Message Composer'

    move_id = fields.Many2one('account.move', string='Faktur Tagihan', required=True)
    partner_id = fields.Many2one('res.partner', string='Penerima (Pelanggan / Vendor)', required=True)
    phone = fields.Char(string='Nomor WhatsApp Tujuan', required=True)
    template_id = fields.Many2one('account.whatsapp.template', string='Template Pesan')
    message = fields.Text(string='Isi Pesan WhatsApp', required=True)
    attach_pdf = fields.Boolean(string='Lampirkan Berkas PDF Faktur', default=True)
    device_id = fields.Char(
        string='Sender Device ID (GOWA)',
        help='Override nomor/device pengirim jika menggunakan GOWA multi-device.'
    )
    gateway_provider = fields.Selection(
        related='move_id.company_id.whatsapp_provider',
        string='Metode Pengiriman Aktif',
        readonly=True
    )

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id and self.move_id:
            self.message = self.template_id.render_template(self.move_id)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            p = self.partner_id.whatsapp_number or self.partner_id.mobile or self.partner_id.phone
            self.phone = self.env['res.partner'].clean_whatsapp_number(p) or p or ''

    def action_send_gowa_or_api(self):
        """
        Dispatch message via active API engine (GOWA / Meta / Custom) with graceful wa.me fallback.
        """
        self.ensure_one()
        clean_phone = self.env['res.partner'].clean_whatsapp_number(self.phone)
        if not clean_phone:
            raise UserError(_("Nomor WhatsApp tidak valid. Pastikan nomor diawali dengan 08 atau 62 (minimal 10 digit)."))

        gateway = self.env['account.whatsapp.gateway']
        res = gateway.dispatch_message(
            self.move_id,
            clean_phone,
            self.message,
            attach_pdf=self.attach_pdf,
            device_id=self.device_id
        )

        if res.get('success'):
            self.move_id.write({
                'whatsapp_status': 'sent',
                'whatsapp_sent_date': fields.Datetime.now(),
            })
            self.move_id.message_post(
                body=_("<b>Pesan WhatsApp Terkirim via %s ke %s:</b><br/>%s") % (
                    res.get('mode', 'Gateway').upper(),
                    clean_phone,
                    self.message.replace('\n', '<br/>')
                ),
                subtype_xmlid='mail.mt_note'
            )
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('WhatsApp Terkirim'),
                    'message': _('Pesan faktur berhasil dikirimkan ke %s.') % clean_phone,
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            # Graceful Fallback: Log error to chatter and present immediate click-to-chat action
            err_msg = res.get('error', 'Gagal terhubung ke gateway')
            self.move_id.write({'whatsapp_status': 'failed'})
            self.move_id.message_post(
                body=_("<b>Gagal Kirim WhatsApp (%s):</b> %s") % (res.get('mode', 'Gateway'), err_msg),
                subtype_xmlid='mail.mt_note'
            )
            fallback_url = res.get('fallback_url')
            if fallback_url:
                return {
                    'type': 'ir.actions.act_url',
                    'url': fallback_url,
                    'target': 'new',
                }
            raise UserError(_("Gagal mengirim WhatsApp: %s") % err_msg)

    def action_send_whatsapp_web(self):
        """
        Directly launch WhatsApp Web click-to-chat in new browser tab.
        """
        self.ensure_one()
        clean_phone = self.env['res.partner'].clean_whatsapp_number(self.phone)
        if not clean_phone:
            raise UserError(_("Nomor WhatsApp tidak valid: %s") % self.phone)

        gateway = self.env['account.whatsapp.gateway']
        res = gateway._dispatch_click_to_chat(clean_phone, self.message)

        self.move_id.write({
            'whatsapp_status': 'sent',
            'whatsapp_sent_date': fields.Datetime.now(),
        })
        self.move_id.message_post(
            body=_("<b>Pesan WhatsApp Dibuka via WhatsApp Web (wa.me) ke %s:</b><br/>%s") % (
                clean_phone,
                self.message.replace('\n', '<br/>')
            ),
            subtype_xmlid='mail.mt_note'
        )

        return {
            'type': 'ir.actions.act_url',
            'url': res.get('url'),
            'target': 'new',
        }
