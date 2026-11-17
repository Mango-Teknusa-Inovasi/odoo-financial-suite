# -*- coding: utf-8 -*-
import io
import csv
import base64
from odoo import models, fields, api, _

class AccountBudgetExcelExportWizard(models.TransientModel):
    _name = 'account.budget.excel.export.wizard'
    _description = 'Wizard Ekspor Realisasi Anggaran ke Excel'

    budget_id = fields.Many2one(
        'account.simple.budget',
        string="Dokumen Anggaran",
        required=True
    )
    export_format = fields.Selection([
        ('xlsx', 'Excel Spreadsheet (.xlsx)'),
        ('csv', 'Universal CSV (UTF-8 BOM)')
    ], string="Format File", default='xlsx', required=True)

    file_data = fields.Binary(string="File Unduhan", readonly=True)
    file_name = fields.Char(string="Nama File", readonly=True)

    def action_generate_export(self):
        """Bangun lembar kerja Excel atau CSV berisi realisasi 12 bulan dan metrik YTD."""
        self.ensure_one()
        budget = self.budget_id

        if self.export_format == 'xlsx':
            try:
                import openpyxl
                from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = f"Anggaran {budget.fiscal_year}"

                # Styling
                header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
                header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
                title_font = Font(name="Calibri", size=14, bold=True, color="0F172A")
                bold_font = Font(name="Calibri", size=11, bold=True)

                # Title & Metadata
                ws.cell(row=1, column=1, value=budget.name).font = title_font
                ws.cell(row=2, column=1, value=f"Perusahaan: {budget.company_id.name} | Tahun Fiskal: {budget.fiscal_year}").font = Font(size=10, italic=True)
                ws.cell(row=3, column=1, value=f"Status: {dict(budget._fields['state'].selection).get(budget.state)}").font = Font(size=10)

                # Table Header
                headers = [
                    "Kode", "Kategori Anggaran", "Tipe", "Plafon Tahunan",
                    "Jan (T)", "Jan (A)", "Feb (T)", "Feb (A)", "Mar (T)", "Mar (A)",
                    "Apr (T)", "Apr (A)", "Mei (T)", "Mei (A)", "Jun (T)", "Jun (A)",
                    "Jul (T)", "Jul (A)", "Agu (T)", "Agu (A)", "Sep (T)", "Sep (A)",
                    "Okt (T)", "Okt (A)", "Nov (T)", "Nov (A)", "Des (T)", "Des (A)",
                    "Realisasi YTD", "Sisa Plafon", "Progress (%)", "Status"
                ]

                row_idx = 5
                for col_idx, h in enumerate(headers, 1):
                    cell = ws.cell(row=row_idx, column=col_idx, value=h)
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")

                # Data Rows
                row_idx = 6
                for line in budget.line_ids:
                    status_label = dict(line._fields['status'].selection).get(line.status, '')
                    type_label = "Beban" if line.budget_type == 'expense' else "Omset"
                    vals = [
                        line.category_id.code or '',
                        line.category_id.name,
                        type_label,
                        line.annual_target,
                        line.m1_target, line.m1_realized,
                        line.m2_target, line.m2_realized,
                        line.m3_target, line.m3_realized,
                        line.m4_target, line.m4_realized,
                        line.m5_target, line.m5_realized,
                        line.m6_target, line.m6_realized,
                        line.m7_target, line.m7_realized,
                        line.m8_target, line.m8_realized,
                        line.m9_target, line.m9_realized,
                        line.m10_target, line.m10_realized,
                        line.m11_target, line.m11_realized,
                        line.m12_target, line.m12_realized,
                        line.ytd_realized,
                        line.variance_amount,
                        line.achievement_pct,
                        status_label
                    ]
                    for col_idx, val in enumerate(vals, 1):
                        cell = ws.cell(row=row_idx, column=col_idx, value=val)
                        if isinstance(val, (int, float)) and col_idx not in (1, 30):
                            cell.number_format = "#,##0"
                    row_idx += 1

                out_io = io.BytesIO()
                wb.save(out_io)
                content = out_io.getvalue()
                filename = f"Realisasi_Anggaran_{budget.fiscal_year}.xlsx"

                self.write({
                    'file_data': base64.b64encode(content),
                    'file_name': filename
                })
            except Exception:
                # Fallback to CSV
                self.export_format = 'csv'

        if self.export_format == 'csv':
            out_str = io.StringIO()
            out_str.write('\ufeff')  # UTF-8 BOM
            writer = csv.writer(out_str, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            writer.writerow([budget.name])
            writer.writerow([f"Perusahaan: {budget.company_id.name}", f"Tahun: {budget.fiscal_year}"])
            writer.writerow([])
            writer.writerow([
                "Kode", "Kategori", "Tipe", "Plafon Tahunan",
                "Jan (T)", "Jan (A)", "Feb (T)", "Feb (A)", "Mar (T)", "Mar (A)",
                "Apr (T)", "Apr (A)", "Mei (T)", "Mei (A)", "Jun (T)", "Jun (A)",
                "Jul (T)", "Jul (A)", "Agu (T)", "Agu (A)", "Sep (T)", "Sep (A)",
                "Okt (T)", "Okt (A)", "Nov (T)", "Nov (A)", "Des (T)", "Des (A)",
                "Realisasi YTD", "Sisa Plafon", "Progress (%)", "Status"
            ])

            for line in budget.line_ids:
                status_label = dict(line._fields['status'].selection).get(line.status, '')
                type_label = "Beban" if line.budget_type == 'expense' else "Omset"
                writer.writerow([
                    line.category_id.code or '',
                    line.category_id.name,
                    type_label,
                    f"{line.annual_target:,.0f}",
                    f"{line.m1_target:,.0f}", f"{line.m1_realized:,.0f}",
                    f"{line.m2_target:,.0f}", f"{line.m2_realized:,.0f}",
                    f"{line.m3_target:,.0f}", f"{line.m3_realized:,.0f}",
                    f"{line.m4_target:,.0f}", f"{line.m4_realized:,.0f}",
                    f"{line.m5_target:,.0f}", f"{line.m5_realized:,.0f}",
                    f"{line.m6_target:,.0f}", f"{line.m6_realized:,.0f}",
                    f"{line.m7_target:,.0f}", f"{line.m7_realized:,.0f}",
                    f"{line.m8_target:,.0f}", f"{line.m8_realized:,.0f}",
                    f"{line.m9_target:,.0f}", f"{line.m9_realized:,.0f}",
                    f"{line.m10_target:,.0f}", f"{line.m10_realized:,.0f}",
                    f"{line.m11_target:,.0f}", f"{line.m11_realized:,.0f}",
                    f"{line.m12_target:,.0f}", f"{line.m12_realized:,.0f}",
                    f"{line.ytd_realized:,.0f}",
                    f"{line.variance_amount:,.0f}",
                    f"{line.achievement_pct:.1f}%",
                    status_label
                ])

            content = out_str.getvalue().encode('utf-8')
            filename = f"Realisasi_Anggaran_{budget.fiscal_year}.csv"

            self.write({
                'file_data': base64.b64encode(content),
                'file_name': filename
            })

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content?model=account.budget.excel.export.wizard&id={self.id}&field=file_data&filename_field=file_name&download=true",
            'target': 'self',
        }
