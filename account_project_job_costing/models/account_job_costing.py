# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountJobCosting(models.Model):
    _name = 'account.job.costing'
    _description = 'Lembar Biaya & Profitabilitas Proyek'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string="Nama Proyek",
        required=True,
        tracking=True,
        help="Nama pekerjaan atau kontrak proyek (misal: Renovasi Ruko Kemang)."
    )
    code = fields.Char(
        string="Kode Proyek",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Baru'),
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Klien / Pemberi Kerja",
        required=True,
        tracking=True,
        help="Pelanggan atau pemberi tugas kontrak pekerjaan ini."
    )
    user_id = fields.Many2one(
        'res.users',
        string="Project Manager / PIC",
        default=lambda self: self.env.user,
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string="Perusahaan",
        required=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Mata Uang",
        related='company_id.currency_id',
        readonly=True
    )
    date_start = fields.Date(
        string="Tanggal Mulai",
        default=fields.Date.context_today,
        tracking=True
    )
    date_end = fields.Date(
        string="Target Selesai",
        tracking=True
    )
    date_closed = fields.Date(
        string="Tanggal Selesai Aktual",
        readonly=True,
        copy=False
    )
    state = fields.Selection([
        ('draft', 'Perencanaan'),
        ('in_progress', 'Sedang Berjalan'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan')
    ], string="Status Proyek", default='draft', tracking=True, copy=False)

    external_project_ref = fields.Char(
        string="Referensi Proyek PM",
        help="Tautan referensi ke nomor proyek pada modul project management atau dokumen kontrak fisik."
    )

    # Budgeting & Target Fields
    contract_amount = fields.Monetary(
        string="Nilai Kontrak (Plafon Pendapatan)",
        currency_field='currency_id',
        tracking=True,
        help="Total nilai kesepakatan kontrak dengan klien sebelum pajak."
    )
    budget_material = fields.Monetary(
        string="Anggaran Bahan & Material",
        currency_field='currency_id',
        tracking=True,
        help="Plafon alokasi belanja bahan baku dan material konstruksi."
    )
    budget_labor = fields.Monetary(
        string="Anggaran Upah & Subkon",
        currency_field='currency_id',
        tracking=True,
        help="Plafon alokasi pembayaran tenaga kerja, mandor, dan subkontraktor."
    )
    budget_overhead = fields.Monetary(
        string="Anggaran Overhead & Sewa",
        currency_field='currency_id',
        tracking=True,
        help="Plafon biaya perijinan, sewa alat berat, transportasi, dan logistik lapangan."
    )
    budget_total_cost = fields.Monetary(
        string="Total Anggaran Biaya (HPP)",
        compute='_compute_budget_totals',
        store=True,
        currency_field='currency_id'
    )
    projected_profit = fields.Monetary(
        string="Proyeksi Laba Bersih",
        compute='_compute_budget_totals',
        store=True,
        currency_field='currency_id'
    )
    projected_margin_pct = fields.Float(
        string="Proyeksi Margin Laba (%)",
        compute='_compute_budget_totals',
        store=True
    )

    # Realized Accrual Fields
    invoice_line_ids = fields.One2many(
        'account.move.line',
        'project_job_id',
        string="Rincian Baris Transaksi"
    )
    actual_revenue = fields.Monetary(
        string="Realisasi Pendapatan Ditagih",
        compute='_compute_accrual_financials',
        store=True,
        currency_field='currency_id',
        tracking=True
    )
    actual_material = fields.Monetary(
        string="Realisasi Biaya Material",
        compute='_compute_accrual_financials',
        store=True,
        currency_field='currency_id'
    )
    actual_labor = fields.Monetary(
        string="Realisasi Biaya Upah & Subkon",
        compute='_compute_accrual_financials',
        store=True,
        currency_field='currency_id'
    )
    actual_overhead = fields.Monetary(
        string="Realisasi Biaya Overhead",
        compute='_compute_accrual_financials',
        store=True,
        currency_field='currency_id'
    )
    actual_total_cost = fields.Monetary(
        string="Total Realisasi Biaya (HPP)",
        compute='_compute_accrual_financials',
        store=True,
        currency_field='currency_id'
    )
    accrual_profit = fields.Monetary(
        string="Laba Bersih Akrual",
        compute='_compute_accrual_financials',
        store=True,
        currency_field='currency_id'
    )
    accrual_margin_pct = fields.Float(
        string="Margin Laba Akrual (%)",
        compute='_compute_accrual_financials',
        store=True
    )

    # Realized Cashflow & Liquidity
    cash_received = fields.Monetary(
        string="Kas Masuk Riil dari Klien",
        compute='_compute_cash_financials',
        store=True,
        currency_field='currency_id'
    )
    cash_disbursed = fields.Monetary(
        string="Kas Keluar Riil ke Vendor",
        compute='_compute_cash_financials',
        store=True,
        currency_field='currency_id'
    )
    net_cash_flow = fields.Monetary(
        string="Arus Kas Bersih Riil",
        compute='_compute_cash_financials',
        store=True,
        currency_field='currency_id'
    )
    uncollected_ar = fields.Monetary(
        string="Piutang Klien Belum Lunas",
        compute='_compute_cash_financials',
        store=True,
        currency_field='currency_id'
    )
    unpaid_ap = fields.Monetary(
        string="Hutang Vendor Belum Lunas",
        compute='_compute_cash_financials',
        store=True,
        currency_field='currency_id'
    )

    # Variance & Budget Burn
    burn_rate_pct = fields.Float(
        string="Burn Rate Anggaran (%)",
        compute='_compute_variance_and_health',
        store=True
    )
    variance_material = fields.Monetary(
        string="Sisa Anggaran Material",
        compute='_compute_variance_and_health',
        store=True,
        currency_field='currency_id'
    )
    variance_labor = fields.Monetary(
        string="Sisa Anggaran Upah",
        compute='_compute_variance_and_health',
        store=True,
        currency_field='currency_id'
    )
    variance_overhead = fields.Monetary(
        string="Sisa Anggaran Overhead",
        compute='_compute_variance_and_health',
        store=True,
        currency_field='currency_id'
    )
    variance_total = fields.Monetary(
        string="Sisa Total Anggaran",
        compute='_compute_variance_and_health',
        store=True,
        currency_field='currency_id'
    )
    health_status = fields.Selection([
        ('healthy', 'Sehat'),
        ('warning', 'Perhatian'),
        ('critical', 'Kritis / Over Budget')
    ], string="Indikator Kesehatan Finansial", compute='_compute_variance_and_health', store=True, tracking=True)

    # Indonesian Withholding Tax Sensitivity
    tax_wht_type = fields.Selection([
        ('none', 'Tanpa Potongan PPh (0%)'),
        ('pph23_2', 'PPh Pasal 23 - Jasa Teknik / Konsultan (2.0%)'),
        ('pph_final_konstruksi_175', 'PPh Final Konstruksi - Kualifikasi Kecil (1.75%)'),
        ('pph_final_konstruksi_265', 'PPh Final Konstruksi - Menengah / Besar (2.65%)'),
        ('pph_final_konstruksi_4', 'PPh Final Konstruksi - Tanpa Sertifikat (4.0%)')
    ], string="Kategori Pajak Penghasilan (PPh)", default='none', tracking=True)
    wht_estimated_rate = fields.Float(
        string="Tarif Estimasi PPh (%)",
        compute='_compute_wht_totals',
        store=True
    )
    wht_estimated_amount = fields.Monetary(
        string="Estimasi Potongan PPh oleh Klien",
        compute='_compute_wht_totals',
        store=True,
        currency_field='currency_id'
    )
    net_cash_expected = fields.Monetary(
        string="Estimasi Kas Bersih Setelah Pajak",
        compute='_compute_wht_totals',
        store=True,
        currency_field='currency_id'
    )

    # Stat Counts
    invoice_count = fields.Integer(string="Jumlah Faktur", compute='_compute_transaction_counts')
    bill_count = fields.Integer(string="Jumlah Tagihan Vendor", compute='_compute_transaction_counts')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('Baru')) == _('Baru'):
                vals['code'] = self.env['ir.sequence'].next_by_code('account.job.costing') or _('Baru')
        return super().create(vals_list)

    @api.depends('contract_amount', 'budget_material', 'budget_labor', 'budget_overhead')
    def _compute_budget_totals(self):
        for rec in self:
            rec.budget_total_cost = round(rec.budget_material + rec.budget_labor + rec.budget_overhead, 2)
            rec.projected_profit = round(rec.contract_amount - rec.budget_total_cost, 2)
            if rec.contract_amount > 0:
                rec.projected_margin_pct = round((rec.projected_profit / rec.contract_amount) * 100.0, 2)
            else:
                rec.projected_margin_pct = 0.0

    @api.depends(
        'invoice_line_ids.price_subtotal',
        'invoice_line_ids.job_cost_type',
        'invoice_line_ids.move_id.state',
        'invoice_line_ids.move_id.move_type'
    )
    def _compute_accrual_financials(self):
        for rec in self:
            rev = 0.0
            mat = 0.0
            lab = 0.0
            ovh = 0.0

            for line in rec.invoice_line_ids:
                move = line.move_id
                if move.state != 'posted':
                    continue

                amount = line.price_subtotal

                # Customer Invoices and Credit Notes
                if move.move_type == 'out_invoice':
                    rev += amount
                elif move.move_type == 'out_refund':
                    rev -= amount

                # Vendor Bills and Refunds
                elif move.move_type == 'in_invoice':
                    if line.job_cost_type == 'material':
                        mat += amount
                    elif line.job_cost_type == 'labor':
                        lab += amount
                    elif line.job_cost_type == 'overhead':
                        ovh += amount
                    else:
                        mat += amount
                elif move.move_type == 'in_refund':
                    if line.job_cost_type == 'material':
                        mat -= amount
                    elif line.job_cost_type == 'labor':
                        lab -= amount
                    elif line.job_cost_type == 'overhead':
                        ovh -= amount
                    else:
                        mat -= amount

            rec.actual_revenue = round(rev, 2)
            rec.actual_material = round(mat, 2)
            rec.actual_labor = round(lab, 2)
            rec.actual_overhead = round(ovh, 2)
            rec.actual_total_cost = round(mat + lab + ovh, 2)
            rec.accrual_profit = round(rec.actual_revenue - rec.actual_total_cost, 2)
            if rec.actual_revenue > 0:
                rec.accrual_margin_pct = round((rec.accrual_profit / rec.actual_revenue) * 100.0, 2)
            else:
                rec.accrual_margin_pct = 0.0

    @api.depends(
        'invoice_line_ids.move_id.amount_total',
        'invoice_line_ids.move_id.amount_residual',
        'invoice_line_ids.move_id.state',
        'invoice_line_ids.move_id.move_type'
    )
    def _compute_cash_financials(self):
        for rec in self:
            moves = rec.invoice_line_ids.mapped('move_id').filtered(lambda m: m.state == 'posted')
            cash_in = 0.0
            cash_out = 0.0
            ar = 0.0
            ap = 0.0

            for move in moves:
                paid = move.amount_total - move.amount_residual
                if move.move_type in ('out_invoice', 'out_refund'):
                    sign = 1.0 if move.move_type == 'out_invoice' else -1.0
                    cash_in += (paid * sign)
                    ar += (move.amount_residual * sign)
                elif move.move_type in ('in_invoice', 'in_refund'):
                    sign = 1.0 if move.move_type == 'in_invoice' else -1.0
                    cash_out += (paid * sign)
                    ap += (move.amount_residual * sign)

            rec.cash_received = round(cash_in, 2)
            rec.cash_disbursed = round(cash_out, 2)
            rec.net_cash_flow = round(cash_in - cash_out, 2)
            rec.uncollected_ar = round(max(ar, 0.0), 2)
            rec.unpaid_ap = round(max(ap, 0.0), 2)

    @api.depends(
        'budget_total_cost',
        'actual_total_cost',
        'budget_material',
        'actual_material',
        'budget_labor',
        'actual_labor',
        'budget_overhead',
        'actual_overhead',
        'net_cash_flow',
        'unpaid_ap',
        'cash_received'
    )
    def _compute_variance_and_health(self):
        for rec in self:
            rec.variance_material = round(rec.budget_material - rec.actual_material, 2)
            rec.variance_labor = round(rec.budget_labor - rec.actual_labor, 2)
            rec.variance_overhead = round(rec.budget_overhead - rec.actual_overhead, 2)
            rec.variance_total = round(rec.budget_total_cost - rec.actual_total_cost, 2)

            if rec.budget_total_cost > 0:
                rec.burn_rate_pct = round((rec.actual_total_cost / rec.budget_total_cost) * 100.0, 2)
            else:
                rec.burn_rate_pct = 0.0

            # Traffic-Light Rules
            if (rec.budget_total_cost > 0 and rec.actual_total_cost > rec.budget_total_cost) or rec.net_cash_flow < 0:
                rec.health_status = 'critical'
            elif rec.burn_rate_pct >= 85.0 or (rec.unpaid_ap > rec.cash_received and rec.unpaid_ap > 0):
                rec.health_status = 'warning'
            else:
                rec.health_status = 'healthy'

    @api.depends('tax_wht_type', 'actual_revenue', 'actual_total_cost')
    def _compute_wht_totals(self):
        rates = {
            'none': 0.0,
            'pph23_2': 2.0,
            'pph_final_konstruksi_175': 1.75,
            'pph_final_konstruksi_265': 2.65,
            'pph_final_konstruksi_4': 4.0,
        }
        for rec in self:
            rate = rates.get(rec.tax_wht_type, 0.0)
            rec.wht_estimated_rate = rate
            wht_amount = round(rec.actual_revenue * (rate / 100.0), 2)
            rec.wht_estimated_amount = wht_amount
            rec.net_cash_expected = round(rec.actual_revenue - wht_amount - rec.actual_total_cost, 2)

    def _compute_transaction_counts(self):
        for rec in self:
            moves = rec.invoice_line_ids.mapped('move_id')
            rec.invoice_count = len(moves.filtered(lambda m: m.move_type in ('out_invoice', 'out_refund')))
            rec.bill_count = len(moves.filtered(lambda m: m.move_type in ('in_invoice', 'in_refund')))

    # State Transitions & Actions
    def action_start_project(self):
        self.write({'state': 'in_progress'})

    def action_complete_project(self):
        self.ensure_one()
        # Smart Closure Warning Guard
        if self.uncollected_ar > 0 or self.unpaid_ap > 0:
            return {
                'name': _('Audit Penutupan Proyek: Konfirmasi Saldo Tertunda'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.job.close.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_project_job_id': self.id,
                    'default_warning_message': _(
                        "Perhatian: Proyek '%(name)s' masih memiliki saldo transaksi yang belum lunas:\n"
                        "• Sisa Piutang Klien: %(ar)s\n"
                        "• Sisa Hutang Vendor: %(ap)s\n\n"
                        "Menutup proyek dalam kondisi ini akan mengarsipkan lembar biaya. "
                        "Apakah Anda yakin ingin menyelesaikan proyek ini?"
                    ) % {
                        'name': self.name,
                        'ar': f"{self.currency_id.symbol} {self.uncollected_ar:,.2f}",
                        'ap': f"{self.currency_id.symbol} {self.unpaid_ap:,.2f}"
                    }
                }
            }
        self.write({
            'state': 'completed',
            'date_closed': fields.Date.context_today(self)
        })

    def action_force_complete(self, reason=""):
        self.write({
            'state': 'completed',
            'date_closed': fields.Date.context_today(self)
        })
        if reason:
            self.message_post(body=_(f"Proyek diselesaikan dengan catatan audit: {reason}"))

    def action_reset_draft(self):
        self.write({'state': 'draft', 'date_closed': False})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_view_invoices(self):
        self.ensure_one()
        moves = self.invoice_line_ids.mapped('move_id').filtered(lambda m: m.move_type in ('out_invoice', 'out_refund'))
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['domain'] = [('id', 'in', moves.ids)]
        action['context'] = {'default_move_type': 'out_invoice', 'default_project_job_id': self.id}
        return action

    def action_view_bills(self):
        self.ensure_one()
        moves = self.invoice_line_ids.mapped('move_id').filtered(lambda m: m.move_type in ('in_invoice', 'in_refund'))
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_in_invoice_type")
        action['domain'] = [('id', 'in', moves.ids)]
        action['context'] = {'default_move_type': 'in_invoice', 'default_project_job_id': self.id}
        return action

    def action_export_excel(self):
        """Buat berkas spreadsheet Excel dan picu pengunduhan langsung."""
        self.ensure_one()
        wizard = self.env['account.job.excel.export.wizard'].create({
            'project_job_id': self.id
        })
        return wizard.action_generate_excel()
