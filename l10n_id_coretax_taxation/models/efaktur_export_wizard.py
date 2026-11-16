# -*- coding: utf-8 -*-
import io
import csv
import re
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class L10nIdEfakturExportWizard(models.TransientModel):
    _name = 'l10n_id.efaktur.export.wizard'
    _description = 'DJP e-Faktur 4.0 & Coretax CSV Batch Exporter'

    date_from = fields.Date(
        string='Start Date',
        required=True,
        default=lambda self: fields.Date.today().replace(day=1)
    )
    date_to = fields.Date(
        string='End Date',
        required=True,
        default=fields.Date.today
    )
    invoice_ids = fields.Many2many(
        'account.move',
        string='Target Invoices',
        domain="[('move_type', 'in', ('out_invoice', 'out_refund')), ('state', '=', 'posted')]"
    )
    csv_file = fields.Binary(string='Generated e-Faktur CSV', readonly=True)
    file_name = fields.Char(string='File Name', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], default='draft')

    @api.onchange('date_from', 'date_to')
    def _onchange_dates(self):
        if self.date_from and self.date_to:
            self.invoice_ids = self.env['account.move'].search([
                ('move_type', 'in', ('out_invoice', 'out_refund')),
                ('state', '=', 'posted'),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to),
            ])

    def action_generate_csv(self):
        self.ensure_one()
        if not self.invoice_ids:
            raise UserError(_("No posted customer invoices found for the selected date range."))

        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Standard DJP e-Faktur 4.0 & Coretax CSV Header Schema
        writer.writerow([
            "FK", "KD_JENIS_TRANSAKSI", "FG_PENGGANTI", "NOMOR_FAKTUR",
            "MASA_PAJAK", "TAHUN_PAJAK", "TANGGAL_FAKTUR", "NPWP", "NAMA",
            "ALAMAT_LENGKAP", "JUMLAH_DPP", "JUMLAH_PPN", "JUMLAH_PPNBM",
            "ID_KETERANGAN_TAMBAHAN", "FG_UANG_MUKA", "UANG_MUKA_DPP",
            "UANG_MUKA_PPN", "UANG_MUKA_PPNBM", "REFERENSI", "KODE_DOKUMEN_PENDUKUNG"
        ])
        writer.writerow([
            "LT", "NPWP", "NAMA", "JALAN", "BLOK", "NOMOR", "RT", "RW",
            "KECAMATAN", "KELURAHAN", "KABUPATEN", "PROPINSI", "KODE_POS", "NOMOR_TELEPON"
        ])
        writer.writerow([
            "OF", "KODE_OBJEK", "NAMA", "HARGA_SATUAN", "JUMLAH_BARANG",
            "HARGA_TOTAL", "DISKON", "DPP", "PPN", "TARIF_PPNBM", "PPNBM"
        ])

        exported_count = 0
        for move in self.invoice_ids:
            partner = move.partner_id
            raw_npwp = partner.l10n_id_npwp16 or partner.vat or '0000000000000000'
            clean_npwp = re.sub(r'\D', '', raw_npwp)
            if len(clean_npwp) < 16:
                clean_npwp = clean_npwp.zfill(16)

            # Strip non-digits from NSFP
            raw_nsfp = move.l10n_id_faktur_pajak_number or ''
            clean_nsfp = re.sub(r'[^0-9]', '', raw_nsfp)
            if len(clean_nsfp) >= 13:
                clean_nsfp = clean_nsfp[-13:]
            else:
                clean_nsfp = f"00026{move.id:08d}"

            invoice_date = move.invoice_date or fields.Date.today()
            masa_pajak = invoice_date.month
            tahun_pajak = invoice_date.year

            # DPP and PPN totals
            dpp_total = sum(move.invoice_line_ids.filtered(lambda l: not l.display_type).mapped('price_subtotal'))
            ppn_total = sum(move.invoice_line_ids.filtered(lambda l: not l.display_type).mapped('price_total')) - dpp_total
            if ppn_total <= 0:
                ppn_total = int(round(dpp_total * 0.12))

            # 1. Output FK (Faktur Keluaran Header)
            writer.writerow([
                "FK",
                move.l10n_id_tax_transaction_code or "01",
                "0",
                clean_nsfp,
                masa_pajak,
                tahun_pajak,
                invoice_date.strftime("%d/%m/%Y"),
                clean_npwp,
                partner.l10n_id_tax_name or partner.name,
                partner.l10n_id_tax_address or partner.contact_address or "Indonesia",
                int(round(dpp_total)),
                int(round(ppn_total)),
                0,
                "",
                "0",
                0,
                0,
                0,
                move.name,
                ""
            ])

            # 2. Output OF (Objek Faktur Lines)
            for line in move.invoice_line_ids.filtered(lambda l: not l.display_type):
                price_subtotal = int(round(line.price_subtotal))
                line_ppn = int(round(price_subtotal * 0.12))
                writer.writerow([
                    "OF",
                    line.product_id.default_code or f"PROD-{line.product_id.id or 1}",
                    (line.name or 'Item').replace('\n', ' ')[:100],
                    int(round(line.price_unit)),
                    line.quantity,
                    price_subtotal,
                    0,
                    price_subtotal,
                    line_ppn,
                    0,
                    0
                ])

            move.l10n_id_efaktur_status = 'exported'
            exported_count += 1

        csv_bytes = output.getvalue().encode('utf-8')
        file_name = f"eFaktur_Coretax_{self.date_from}_{self.date_to}.csv"

        self.write({
            'csv_file': base64.b64encode(csv_bytes),
            'file_name': file_name,
            'state': 'done'
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'l10n_id.efaktur.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
