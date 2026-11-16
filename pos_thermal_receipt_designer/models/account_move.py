# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    thermal_template_id = fields.Many2one(
        'pos.thermal.template',
        string="Template Struk Thermal",
        copy=False,
        help="Pilih format struk thermal 58mm atau 80mm untuk pencetakan faktur ini."
    )

    def action_print_thermal_receipt(self):
        """Buka laporan struk kasir thermal 58mm atau 80mm siap cetak."""
        self.ensure_one()
        template = self.thermal_template_id or self.env['pos.thermal.template'].search([
            ('company_id', '=', self.company_id.id),
            ('is_default', '=', True)
        ], limit=1)

        if not template:
            template = self.env['pos.thermal.template'].search([
                ('company_id', '=', self.company_id.id)
            ], limit=1)

        if not template:
            raise UserError(_("Belum ada Template Struk Thermal yang dikonfigurasi untuk perusahaan ini."))

        report_xmlid = 'pos_thermal_receipt_designer.action_report_thermal_58mm' if template.paper_width == '58mm' else 'pos_thermal_receipt_designer.action_report_thermal_80mm'
        return self.env.ref(report_xmlid).report_action(self)
