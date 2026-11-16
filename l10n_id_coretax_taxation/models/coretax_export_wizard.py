# -*- coding: utf-8 -*-
import io
import csv
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CoretaxExportWizard(models.TransientModel):
    _name = 'coretax.export.wizard'
    _description = 'Coretax DJP Withholding Tax Export Wizard'

    date_from = fields.Date(
        string='Start Date',
        required=True,
        default=lambda self: fields.Date.context_today(self).replace(day=1)
    )
    date_to = fields.Date(
        string='End Date',
        required=True,
        default=fields.Date.context_today
    )
    tax_category = fields.Selection([
        ('all', 'All Withholding Taxes'),
        ('pph23', 'PPh 23 (Services & Rentals)'),
        ('pph4_2', 'PPh 4(2) (Final Tax / Land & Building)'),
        ('pph_final_umkm', 'PPh Final UMKM 0.5% (PP 20/2026)'),
        ('pph22', 'PPh 22'),
    ], string='Tax Category', default='all', required=True)

    partner_id = fields.Many2one(
        'res.partner',
        string='Specific Partner (Optional)'
    )

    data_file = fields.Binary(string='Generated CSV File', readonly=True)
    file_name = fields.Char(string='File Name', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], default='draft')

    def action_generate_export(self):
        self.ensure_one()

        # Build domain on account.move
        domain = [
            ('state', '=', 'posted'),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
        ]
        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))

        moves = self.env['account.move'].search(domain)
        if not moves:
            raise UserError(_("No posted invoices or bills found in the selected date range."))

        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Coretax DJP CSV Header
        writer.writerow([
            'Invoice / Bill Number',
            'Document Date',
            'Partner Name',
            'NPWP 16',
            'NITKU',
            'Taxpayer Category',
            'Tax Category',
            'Kode Objek Pajak',
            'No. Bukti Potong',
            'Base Amount (DPP)',
            'Tax Rate (%)',
            'Tax Amount (PPh)',
            'Settlement Mode'
        ])

        record_count = 0
        for move in moves:
            partner = move.partner_id
            for line in move.invoice_line_ids:
                for tax in line.tax_ids:
                    # Filter by tax category if specified
                    if not tax.l10n_id_tax_type:
                        continue
                    if self.tax_category != 'all' and tax.l10n_id_tax_type != self.tax_category:
                        continue

                    # Calculate tax for this line
                    base_amount = line.price_subtotal
                    rate = abs(tax.amount)
                    tax_amount = round(base_amount * (rate / 100.0), 2)

                    writer.writerow([
                        move.name,
                        move.invoice_date.strftime('%Y-%m-%d') if move.invoice_date else '',
                        partner.name or '',
                        partner.l10n_id_npwp16 or '',
                        partner.l10n_id_nitku or '',
                        partner.l10n_id_taxpayer_type or '',
                        dict(tax._fields['l10n_id_tax_type'].selection).get(tax.l10n_id_tax_type, tax.l10n_id_tax_type),
                        move.l10n_id_tax_object_code or tax.l10n_id_tax_object_code or '',
                        move.l10n_id_bupot_number or '',
                        f"{base_amount:.2f}",
                        f"{rate:.2f}",
                        f"{tax_amount:.2f}",
                        move.l10n_id_umkm_settlement_type or ''
                    ])
                    record_count += 1

        if record_count == 0:
            raise UserError(_("No lines with matching Indonesian withholding tax were found."))

        # Encode and save file
        csv_data = output.getvalue().encode('utf-8')
        file_name = f"Coretax_Export_{self.date_from}_{self.date_to}.csv"

        self.write({
            'data_file': base64.b64encode(csv_data),
            'file_name': file_name,
            'state': 'done'
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'coretax.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
