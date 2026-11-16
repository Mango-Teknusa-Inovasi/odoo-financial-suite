# -*- coding: utf-8 -*-
from odoo import models, fields, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bi_sync_enabled = fields.Boolean(
        related='company_id.bi_sync_enabled',
        readonly=False,
        string="Aktifkan Sinkronisasi Kurs BI"
    )
    bi_rate_source = fields.Selection(
        related='company_id.bi_rate_source',
        readonly=False,
        string="Metode Penentuan Kurs"
    )
    bi_last_sync_date = fields.Datetime(
        related='company_id.bi_last_sync_date',
        readonly=True,
        string="Terakhir Disinkronkan"
    )
    bi_last_sync_status = fields.Selection(
        related='company_id.bi_last_sync_status',
        readonly=True,
        string="Status Sinkronisasi"
    )
    bi_last_sync_message = fields.Text(
        related='company_id.bi_last_sync_message',
        readonly=True,
        string="Catatan Sinkronisasi Terakhir"
    )

    def action_sync_bi_rates_now(self):
        """Memicu penarikan kurs resmi Bank Indonesia dan Kemenkeu secara instan."""
        service = self.env['bi.rate.sync.service']
        res = service.sync_rates_for_company(self.env.company)
        
        status_type = 'success' if res.get('status') == 'success' else ('warning' if res.get('status') == 'warning' else 'danger')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Sinkronisasi Kurs Selesai'),
                'message': res.get('message', _('Kurs valas berhasil diperbarui.')),
                'type': status_type,
                'sticky': False,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'}
            }
        }
