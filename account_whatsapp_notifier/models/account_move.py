# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    whatsapp_status = fields.Selection([
        ('not_sent', 'Belum Terkirim'),
        ('sent', 'Terkirim via WhatsApp'),
        ('failed', 'Gagal Terkirim'),
    ], string='Status WhatsApp', default='not_sent', copy=False, tracking=True)

    whatsapp_sent_date = fields.Datetime(
        string='Waktu Kirim WhatsApp',
        readonly=True,
        copy=False
    )

    def action_open_whatsapp_composer(self):
        """
        Open the interactive WhatsApp composer wizard pre-filled with invoice data.
        """
        self.ensure_one()
        # Find default template for this document type
        tmpl = self.env['account.whatsapp.template'].search([
            ('document_type', '=', self.move_type if self.move_type in ('out_invoice', 'out_refund') else 'out_invoice'),
            ('company_id', 'in', (self.company_id.id, False))
        ], limit=1)

        phone = self.partner_id.whatsapp_number or self.partner_id.mobile or self.partner_id.phone
        phone_clean = self.env['res.partner'].clean_whatsapp_number(phone) or phone or ''
        rendered_body = tmpl.render_template(self) if tmpl else ''

        return {
            'name': _('Kirim Faktur via WhatsApp'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.whatsapp.composer',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_phone': phone_clean,
                'default_template_id': tmpl.id if tmpl else False,
                'default_message': rendered_body,
                'default_device_id': self.company_id.gowa_device_id or '',
                'default_attach_pdf': self.company_id.gowa_attach_pdf,
            }
        }

    def action_post(self):
        """
        Inherit action_post to optionally auto-dispatch WhatsApp notifications when configured.
        """
        res = super().action_post()
        for move in self:
            if move.is_sale_document() and move.company_id.auto_send_on_post:
                move._action_auto_send_whatsapp()
        return res

    def _action_auto_send_whatsapp(self):
        """
        Headless automated WhatsApp dispatch triggered on invoice confirmation.
        """
        self.ensure_one()
        phone = self.partner_id.whatsapp_number or self.partner_id.mobile or self.partner_id.phone
        if not phone:
            return False

        tmpl = self.env['account.whatsapp.template'].search([
            ('document_type', '=', self.move_type),
            ('company_id', 'in', (self.company_id.id, False))
        ], limit=1)
        if not tmpl:
            return False

        msg = tmpl.render_template(self)
        gateway = self.env['account.whatsapp.gateway']
        res = gateway.dispatch_message(self, phone, msg, attach_pdf=self.company_id.gowa_attach_pdf)

        if res.get('success'):
            self.write({
                'whatsapp_status': 'sent',
                'whatsapp_sent_date': fields.Datetime.now()
            })
            self.message_post(
                body=_("<b>Pesan WhatsApp Terkirim Otomatis:</b><br/>%s") % msg.replace('\n', '<br/>'),
                subtype_xmlid='mail.mt_note'
            )
        else:
            self.write({'whatsapp_status': 'failed'})
            self.message_post(
                body=_("<b>Gagal Kirim WhatsApp Otomatis:</b> %s") % res.get('error', 'Unknown Error'),
                subtype_xmlid='mail.mt_note'
            )
        return True
