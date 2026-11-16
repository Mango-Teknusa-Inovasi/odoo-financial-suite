# -*- coding: utf-8 -*-
import io
import csv
import base64
from odoo import models, fields, api, _

class AccountJobExcelExportWizard(models.TransientModel):
    _name = 'account.job.excel.export.wizard'
    _description = 'Ekspor Rincian Transaksi Proyek ke Excel'

    project_job_id = fields.Many2one(
        'account.job.costing',
        string="Proyek",
        required=True,
        readonly=True
    )
    file_data = fields.Binary(
        string="Berkas Excel",
        readonly=True
    )
    file_name = fields.Char(
        string="Nama Berkas",
        readonly=True
    )

    def action_generate_excel(self):
        """Generate formatted Excel spreadsheet containing full project cost sheet."""
        self.ensure_one()
        project = self.project_job_id
        symbol = project.currency_id.symbol or 'IDR'

        # Check for openpyxl
        has_openpyxl = False
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            has_openpyxl = True
        except ImportError:
            has_openpyxl = False

        if has_openpyxl:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Project Cost Sheet"

            # Fonts and styles
            header_font = Font(name="Calibri", size=14, bold=True, color="1E293B")
            sec_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            sec_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
            sub_fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
            bold_font = Font(name="Calibri", size=10, bold=True)
            norm_font = Font(name="Calibri", size=10)

            ws.cell(row=1, column=1, value=f"LEMBAR BIAYA & PROFITABILITAS PROYEK - {project.name}").font = header_font
            ws.cell(row=2, column=1, value=f"Kode: {project.code} | Klien: {project.partner_id.name} | PIC: {project.user_id.name or '-'}").font = bold_font

            # Section 1: Dual-Metric Summary
            ws.cell(row=4, column=1, value="RINGKASAN METRIK FINANSIAL").font = sec_font
            ws.cell(row=4, column=1).fill = sec_fill
            ws.merge_cells("A4:E4")

            ws.cell(row=5, column=1, value="Metrik Akrual").font = bold_font
            ws.cell(row=5, column=2, value="Nilai (IDR)").font = bold_font
            ws.cell(row=5, column=4, value="Posisi Kas Nyata").font = bold_font
            ws.cell(row=5, column=5, value="Nilai (IDR)").font = bold_font

            ws.cell(row=6, column=1, value="Total Pendapatan Ditagih").font = norm_font
            ws.cell(row=6, column=2, value=project.actual_revenue).font = norm_font
            ws.cell(row=6, column=4, value="Kas Masuk Riil dari Klien").font = norm_font
            ws.cell(row=6, column=5, value=project.cash_received).font = norm_font

            ws.cell(row=7, column=1, value="Total Realisasi Biaya (HPP)").font = norm_font
            ws.cell(row=7, column=2, value=project.actual_total_cost).font = norm_font
            ws.cell(row=7, column=4, value="Kas Keluar Riil ke Vendor").font = norm_font
            ws.cell(row=7, column=5, value=project.cash_disbursed).font = norm_font

            ws.cell(row=8, column=1, value="Laba Bersih Akrual").font = bold_font
            ws.cell(row=8, column=2, value=project.accrual_profit).font = bold_font
            ws.cell(row=8, column=4, value="Arus Kas Bersih Riil").font = bold_font
            ws.cell(row=8, column=5, value=project.net_cash_flow).font = bold_font

            ws.cell(row=9, column=1, value="Margin Laba Akrual (%)").font = norm_font
            ws.cell(row=9, column=2, value=f"{project.accrual_margin_pct:.1f}%").font = norm_font
            ws.cell(row=9, column=4, value="Sisa Piutang Klien (AR)").font = norm_font
            ws.cell(row=9, column=5, value=project.uncollected_ar).font = norm_font

            ws.cell(row=10, column=4, value="Sisa Hutang Vendor (AP)").font = norm_font
            ws.cell(row=10, column=5, value=project.unpaid_ap).font = norm_font

            # Section 2: Budget vs Actual
            ws.cell(row=12, column=1, value="ANGGARAN PLAFON VS REALISASI BIAYA").font = sec_font
            ws.cell(row=12, column=1).fill = sec_fill
            ws.merge_cells("A12:E12")

            ws.cell(row=13, column=1, value="Kategori Biaya").font = bold_font
            ws.cell(row=13, column=2, value="Anggaran (Plafon)").font = bold_font
            ws.cell(row=13, column=3, value="Realisasi Aktual").font = bold_font
            ws.cell(row=13, column=4, value="Sisa Anggaran (Varian)").font = bold_font
            ws.cell(row=13, column=5, value="Burn Rate %").font = bold_font

            costs = [
                ("Material & Bahan", project.budget_material, project.actual_material, project.variance_material),
                ("Upah & Subkon", project.budget_labor, project.actual_labor, project.variance_labor),
                ("Overhead & Sewa", project.budget_overhead, project.actual_overhead, project.variance_overhead),
                ("TOTAL BIAYA HPP", project.budget_total_cost, project.actual_total_cost, project.variance_total)
            ]
            row_idx = 14
            for cat, bud, act, var in costs:
                f = bold_font if "TOTAL" in cat else norm_font
                ws.cell(row=row_idx, column=1, value=cat).font = f
                ws.cell(row=row_idx, column=2, value=bud).font = f
                ws.cell(row=row_idx, column=3, value=act).font = f
                ws.cell(row=row_idx, column=4, value=var).font = f
                burn = round((act / bud * 100.0), 1) if bud else 0.0
                ws.cell(row=row_idx, column=5, value=f"{burn}%").font = f
                row_idx += 1

            # Section 3: Detailed Transaction Lines
            row_idx += 1
            ws.cell(row=row_idx, column=1, value="RINCIAN BARIS TRANSAKSI TERHUBUNG").font = sec_font
            ws.cell(row=row_idx, column=1).fill = sec_fill
            ws.merge_cells(f"A{row_idx}:E{row_idx}")

            row_idx += 1
            headers = ["No. Faktur / Tagihan", "Tanggal", "Tipe Transaksi", "Kategori Biaya", "Nominal (Subtotal)"]
            for col_idx, h in enumerate(headers, 1):
                ws.cell(row=row_idx, column=col_idx, value=h).font = bold_font

            row_idx += 1
            for line in project.invoice_line_ids:
                move = line.move_id
                ws.cell(row=row_idx, column=1, value=move.name or move.ref or "-").font = norm_font
                ws.cell(row=row_idx, column=2, value=str(move.invoice_date or move.date)).font = norm_font
                ws.cell(row=row_idx, column=3, value=dict(move._fields['move_type'].selection).get(move.move_type, move.move_type)).font = norm_font
                ws.cell(row=row_idx, column=4, value=dict(line._fields['job_cost_type'].selection).get(line.job_cost_type, "-")).font = norm_font
                ws.cell(row=row_idx, column=5, value=line.price_subtotal).font = norm_font
                row_idx += 1

            output = io.BytesIO()
            wb.save(output)
            raw_bytes = output.getvalue()
            ext = "xlsx"
        else:
            # Fallback to UTF-8 BOM CSV for universal Excel opening
            output = io.StringIO()
            output.write('\ufeff')
            writer = csv.writer(output, delimiter=';')

            writer.writerow(["LEMBAR BIAYA & PROFITABILITAS PROYEK", project.name])
            writer.writerow(["Kode Proyek", project.code, "Klien", project.partner_id.name])
            writer.writerow([])
            writer.writerow(["RINGKASAN METRIK AKRUAL"])
            writer.writerow(["Total Pendapatan Ditagih", project.actual_revenue])
            writer.writerow(["Total Realisasi Biaya HPP", project.actual_total_cost])
            writer.writerow(["Laba Bersih Akrual", project.accrual_profit])
            writer.writerow(["Margin Laba Akrual (%)", f"{project.accrual_margin_pct:.1f}%"])
            writer.writerow([])
            writer.writerow(["POSISI KAS NYATA"])
            writer.writerow(["Kas Masuk Riil dari Klien", project.cash_received])
            writer.writerow(["Kas Keluar Riil ke Vendor", project.cash_disbursed])
            writer.writerow(["Arus Kas Bersih Riil", project.net_cash_flow])
            writer.writerow(["Sisa Piutang Klien (AR)", project.uncollected_ar])
            writer.writerow(["Sisa Hutang Vendor (AP)", project.unpaid_ap])
            writer.writerow([])
            writer.writerow(["ANGGARAN VS REALISASI BIAYA"])
            writer.writerow(["Kategori", "Anggaran (Plafon)", "Realisasi Aktual", "Sisa Anggaran (Varian)", "Burn Rate %"])
            writer.writerow(["Material & Bahan", project.budget_material, project.actual_material, project.variance_material, f"{project.burn_rate_pct:.1f}%"])
            writer.writerow(["Upah & Subkon", project.budget_labor, project.actual_labor, project.variance_labor, ""])
            writer.writerow(["Overhead & Sewa", project.budget_overhead, project.actual_overhead, project.variance_overhead, ""])
            writer.writerow(["TOTAL HPP", project.budget_total_cost, project.actual_total_cost, project.variance_total, ""])
            writer.writerow([])
            writer.writerow(["RINCIAN BARIS TRANSAKSI"])
            writer.writerow(["No. Faktur", "Tanggal", "Tipe Transaksi", "Kategori Biaya", "Subtotal"])
            for line in project.invoice_line_ids:
                move = line.move_id
                writer.writerow([
                    move.name or move.ref or "-",
                    str(move.invoice_date or move.date),
                    move.move_type,
                    line.job_cost_type or "-",
                    line.price_subtotal
                ])
            raw_bytes = output.getvalue().encode('utf-8-sig')
            ext = "csv"

        clean_code = (project.code or "PRJ").replace('/', '_')
        fname = f"CostSheet_{clean_code}.{ext}"
        self.write({
            'file_data': base64.b64encode(raw_bytes),
            'file_name': fname
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=account.job.excel.export.wizard&id={self.id}&field=file_data&filename_field=file_name&download=true',
            'target': 'self',
        }
