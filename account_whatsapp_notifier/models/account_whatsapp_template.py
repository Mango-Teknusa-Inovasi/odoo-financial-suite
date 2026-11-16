# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountWhatsAppTemplate(models.Model):
    _name = 'account.whatsapp.template'
    _description = 'WhatsApp Notification Message Template'
    _order = 'sequence asc, id desc'

    name = fields.Char(string='Template Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    code = fields.Char(string='Code', help='Unique internal template identifier')
    document_type = fields.Selection([
        ('out_invoice', 'Faktur Pelanggan (Customer Invoice)'),
        ('out_refund', 'Retur Penjualan (Credit Note)'),
        ('reminder', 'Pengingat Jatuh Tempo (Payment Reminder)'),
        ('receipt', 'Kuitansi Pembayaran Lunas (Payment Receipt)'),
        ('general', 'Pesan Finansial Umum (General Message)'),
    ], string='Document Context', default='out_invoice', required=True)

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    body = fields.Text(
        string='Message Template Body',
        required=True,
        help='Available variables: {{partner_name}}, {{invoice_number}}, {{amount_total}}, '
             '{{amount_residual}}, {{due_date}}, {{company_name}}, {{portal_url}}, {{qris_note}}, {{emeterai_status}}'
    )
    active = fields.Boolean(string='Active', default=True)

    def render_template(self, move):
        """
        Render template string substituting dynamic placeholder variables with live record values.
        """
        self.ensure_one()
        if not move:
            return self.body or ''

        partner_name = move.partner_id.name or _('Pelanggan')
        invoice_number = move.name or move.ref or _('Draft')
        currency = move.currency_id or self.env.company.currency_id
        amount_total_str = f"{currency.symbol or 'Rp'} {move.amount_total:,.2f}"
        amount_residual_str = f"{currency.symbol or 'Rp'} {move.amount_residual:,.2f}"
        due_date_str = move.invoice_date_due.strftime('%d/%m/%Y') if move.invoice_date_due else '-'
        company_name = move.company_id.name or self.env.company.name

        portal_url = move.get_portal_url() if hasattr(move, 'get_portal_url') else f"/my/invoices/{move.id}"
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        full_portal_url = f"{base_url.rstrip('/')}{portal_url}" if portal_url else ''

        # Smart Cross-Module Injection: QRIS (account_qris_qbiz)
        qris_note = ''
        if hasattr(move, 'qris_image') and move.qris_image and move.amount_residual > 0:
            qris_note = _("\n*Pembayaran Cepat QRIS:* Scan kode QRIS pada lampiran faktur via BCA, Mandiri, BRI, GoPay, OVO, atau DANA.")

        # Smart Cross-Module Injection: e-Meterai (account_stamp_signature)
        emeterai_status = ''
        if hasattr(move, 'emeterai_status') and move.emeterai_status == 'stamped':
            emeterai_status = _("\n*Status Dokumen:* Telah dibubuhi e-Meterai resmi Peruri sah.")

        rendered = self.body or ''
        replacements = {
            '{{partner_name}}': partner_name,
            '{{invoice_number}}': invoice_number,
            '{{amount_total}}': amount_total_str,
            '{{amount_residual}}': amount_residual_str,
            '{{due_date}}': due_date_str,
            '{{company_name}}': company_name,
            '{{portal_url}}': full_portal_url,
            '{{qris_note}}': qris_note,
            '{{emeterai_status}}': emeterai_status,
        }

        for placeholder, value in replacements.items():
            rendered = rendered.replace(placeholder, str(value or ''))

        return rendered.strip()
