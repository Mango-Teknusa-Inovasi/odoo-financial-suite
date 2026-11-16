# -*- coding: utf-8 -*-
import io
import base64
from datetime import date
try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    from datetime import timedelta
    def relativedelta(days=0, months=0, **kwargs):
        return timedelta(days=days + int(months * 30.4375))
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

class AccountOpeningBalanceWizard(models.TransientModel):
    _name = 'account.opening.balance.wizard'
    _description = 'Opening Balance Setup Wizard'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string='Currency',
        readonly=True
    )
    date_cut_off = fields.Date(
        string='Cut-off Date (Tanggal Cut-off)',
        required=True,
        default=lambda self: (date.today().replace(day=1) - relativedelta(days=1)),
        help='Financial cut-off date representing the end of previous ledger accounts.'
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Opening Journal (Jurnal Pembuka)',
        required=True,
        domain="[('type', '=', 'general')]",
        default=lambda self: self.env['account.journal'].search([('type', '=', 'general')], limit=1)
    )

    # Equity Balancing Choices
    equity_choice = fields.Selection([
        ('owner_equity', '100% Modal Pemilik / Disetor (310000)'),
        ('retained_earnings', '100% Laba Ditahan (320000)'),
        ('split', 'Bagi Proporsional (Modal & Laba Ditahan)'),
    ], string='Equity Allocation (Alokasi Ekuitas)', default='owner_equity', required=True)

    equity_account_id = fields.Many2one(
        'account.account',
        string='Capital Account (Modal Disetor)',
        domain="[('account_type', '=', 'equity'), ('deprecated', '=', False)]"
    )
    retained_earnings_account_id = fields.Many2one(
        'account.account',
        string='Retained Earnings Account (Laba Ditahan)',
        domain="[('account_type', '=', 'equity'), ('deprecated', '=', False)]"
    )
    equity_split_percent = fields.Float(
        string='Capital Share (%)',
        default=50.0,
        help='Percentage of net equity allocated to Capital Account (remainder goes to Retained Earnings).'
    )

    # Operational Toggles
    update_physical_stock = fields.Boolean(
        string='Update Physical Stock in Warehouse (Update Stok Fisik)',
        default=True,
        help='Generate physical inventory stock quants alongside general ledger entry.'
    )
    warehouse_id = fields.Many2one('stock.warehouse', string='Target Warehouse (Gudang Tujuan)')
    lock_fiscal_date = fields.Boolean(
        string='Lock Opening Period (Kunci Periode Fiskal Saldo Awal)',
        default=False,
        help='Automatically set company fiscal lock date to cut-off date to prevent accidental past edits.'
    )

    # Sub-lines
    cash_line_ids = fields.One2many('account.opening.cash.line', 'wizard_id', string='Cash and Bank Lines')
    receivable_line_ids = fields.One2many('account.opening.receivable.line', 'wizard_id', string='Receivable Lines')
    payable_line_ids = fields.One2many('account.opening.payable.line', 'wizard_id', string='Payable Lines')
    stock_line_ids = fields.One2many('account.opening.stock.line', 'wizard_id', string='Stock Lines')
    asset_line_ids = fields.One2many('account.opening.asset.wizard.line', 'wizard_id', string='Fixed Asset Lines')

    # Live Balance Bar Calculations
    total_cash = fields.Monetary(string='Total Kas & Bank', currency_field='currency_id', compute='_compute_totals')
    total_receivable = fields.Monetary(string='Total Piutang Usaha', currency_field='currency_id', compute='_compute_totals')
    total_payable = fields.Monetary(string='Total Hutang Usaha', currency_field='currency_id', compute='_compute_totals')
    total_stock = fields.Monetary(string='Total Persediaan', currency_field='currency_id', compute='_compute_totals')
    total_asset_cost = fields.Monetary(string='Total Harga Perolehan Aset', currency_field='currency_id', compute='_compute_totals')
    total_asset_depreciation = fields.Monetary(string='Total Akumulasi Penyusutan', currency_field='currency_id', compute='_compute_totals')
    total_asset_nbv = fields.Monetary(string='Total Nilai Buku Aset', currency_field='currency_id', compute='_compute_totals')

    total_assets = fields.Monetary(string='Total Aktiva (Aset)', currency_field='currency_id', compute='_compute_totals')
    total_liabilities = fields.Monetary(string='Total Kewajiban (Hutang)', currency_field='currency_id', compute='_compute_totals')
    calculated_equity = fields.Monetary(string='Net Calculated Equity (Ekuitas Bersih)', currency_field='currency_id', compute='_compute_totals')
    is_balanced = fields.Boolean(string='Is Balanced', compute='_compute_totals')

    # Excel Import / Export
    excel_file = fields.Binary(string='Excel Spreadsheet (.xlsx)')
    excel_filename = fields.Char(string='Excel Filename')

    def _account_company_domain(self, company_id=None):
        cid = company_id or (self.company_id.id if self.company_id else self.env.company.id)
        if 'company_ids' in self.env['account.account']._fields:
            return [('company_ids', 'in', [cid])]
        return [('company_id', '=', cid)]

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        company = self.env.company
        acc_domain = [('company_ids', 'in', [company.id])] if 'company_ids' in self.env['account.account']._fields else [('company_id', '=', company.id)]
        # Find default equity accounts
        eq_acc = self.env['account.account'].search(acc_domain + [
            ('account_type', '=', 'equity'),
            ('code', '=like', '31%')
        ], limit=1)
        ret_acc = self.env['account.account'].search(acc_domain + [
            ('account_type', '=', 'equity'),
            ('code', '=like', '32%')
        ], limit=1)
        if eq_acc:
            res['equity_account_id'] = eq_acc.id
        if ret_acc:
            res['retained_earnings_account_id'] = ret_acc.id

        wh = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
        if wh:
            res['warehouse_id'] = wh.id
        return res

    @api.depends('cash_line_ids.amount', 'receivable_line_ids.amount', 'payable_line_ids.amount',
                 'stock_line_ids.total_value', 'asset_line_ids.original_cost',
                 'asset_line_ids.past_accumulated_depreciation')
    def _compute_totals(self):
        for wizard in self:
            cash = sum(wizard.cash_line_ids.mapped('amount'))
            receivables = sum(wizard.receivable_line_ids.mapped('amount'))
            payables = sum(wizard.payable_line_ids.mapped('amount'))
            stock = sum(wizard.stock_line_ids.mapped('total_value'))
            asset_cost = sum(wizard.asset_line_ids.mapped('original_cost'))
            asset_dep = sum(wizard.asset_line_ids.mapped('past_accumulated_depreciation'))
            asset_nbv = max(0.0, asset_cost - asset_dep)

            tot_assets = cash + receivables + stock + asset_nbv
            tot_liab = payables
            net_equity = tot_assets - tot_liab

            wizard.total_cash = cash
            wizard.total_receivable = receivables
            wizard.total_payable = payables
            wizard.total_stock = stock
            wizard.total_asset_cost = asset_cost
            wizard.total_asset_depreciation = asset_dep
            wizard.total_asset_nbv = asset_nbv
            wizard.total_assets = tot_assets
            wizard.total_liabilities = tot_liab
            wizard.calculated_equity = net_equity
            wizard.is_balanced = bool(tot_assets > 0 or tot_liab > 0)

    def action_download_excel_template(self):
        """Generate formatted Excel workbook with 5 sheets for bulk data preparation."""
        if not HAS_OPENPYXL:
            raise UserError(_("Pustaka 'openpyxl' diperlukan untuk menghasilkan file Excel."))

        wb = openpyxl.Workbook()
        # Default sheet -> Kas & Bank
        ws_cash = wb.active
        ws_cash.title = "Kas_Bank"
        ws_ar = wb.create_sheet(title="Piutang_Pelanggan")
        ws_ap = wb.create_sheet(title="Hutang_Pemasok")
        ws_stock = wb.create_sheet(title="Persediaan_Barang")
        ws_asset = wb.create_sheet(title="Aktiva_Tetap")

        # Styling headers
        header_font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
        header_fill = PatternFill(start_color='1A365D', end_color='1A365D', fill_type='solid')

        def style_headers(ws, headers):
            ws.append(headers)
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center', vertical='center')

        style_headers(ws_cash, ["Nama Jurnal (Bank/Kas)", "Kode Akun GL", "Saldo Awal (Rp)"])
        style_headers(ws_ar, ["Nama Pelanggan", "Nomor Faktur Lama", "Tanggal Faktur (YYYY-MM-DD)", "Jatuh Tempo (YYYY-MM-DD)", "Sisa Piutang (Rp)"])
        style_headers(ws_ap, ["Nama Pemasok", "Nomor Tagihan Lama", "Tanggal Tagihan (YYYY-MM-DD)", "Jatuh Tempo (YYYY-MM-DD)", "Sisa Hutang (Rp)"])
        style_headers(ws_stock, ["Kode Produk / SKU", "Nama Produk", "Kuantitas Fisik", "HPP per Unit (Rp)"])
        style_headers(ws_asset, ["Nama Aktiva Tetap", "Kategori Pajak (group_1/2/3/4/building_permanent)", "Tanggal Perolehan (YYYY-MM-DD)", "Harga Beli (Rp)", "Akumulasi Penyusutan (Rp)"])

        # Auto-adjust column widths
        for ws in [ws_cash, ws_ar, ws_ap, ws_stock, ws_asset]:
            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                ws.column_dimensions[col_letter].width = max(max_len + 4, 15)

        fp = io.BytesIO()
        wb.save(fp)
        fp.seek(0)
        data = base64.b64encode(fp.read())

        attachment = self.env['ir.attachment'].create({
            'name': 'Template_Saldo_Awal_MangoTek.xlsx',
            'type': 'binary',
            'datas': data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'res_model': self._name,
            'res_id': self.id,
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def action_import_excel(self):
        """Parse uploaded Excel workbook and populate wizard lines."""
        self.ensure_one()
        if not self.excel_file:
            raise ValidationError(_("Silakan pilih berkas spreadsheet Excel (.xlsx) terlebih dahulu."))
        if not HAS_OPENPYXL:
            raise UserError(_("Pustaka 'openpyxl' diperlukan untuk membaca berkas Excel."))

        file_data = base64.b64decode(self.excel_file)
        wb = openpyxl.load_workbook(io.BytesIO(file_data), data_only=True)

        # Clear existing lines
        self.cash_line_ids.unlink()
        self.receivable_line_ids.unlink()
        self.payable_line_ids.unlink()
        self.stock_line_ids.unlink()
        self.asset_line_ids.unlink()

        # 1. Parse Kas_Bank
        if "Kas_Bank" in wb.sheetnames:
            ws = wb["Kas_Bank"]
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]: continue
                journal_name, account_code, amount = row[0], str(row[1] or '').strip(), float(row[2] or 0.0)
                journal = self.env['account.journal'].search([('company_id', '=', self.company_id.id), ('name', 'ilike', journal_name)], limit=1)
                account = self.env['account.account'].search(self._account_company_domain() + [('code', '=', account_code)], limit=1)
                if not account and journal:
                    account = journal.default_account_id
                if journal and account and amount:
                    self.env['account.opening.cash.line'].create({
                        'wizard_id': self.id,
                        'journal_id': journal.id,
                        'account_id': account.id,
                        'amount': amount,
                    })

        # 2. Parse Piutang_Pelanggan
        if "Piutang_Pelanggan" in wb.sheetnames:
            ws = wb["Piutang_Pelanggan"]
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]: continue
                cust_name, ref, inv_date, due_date, amount = row[0], str(row[1] or ''), row[2], row[3], float(row[4] or 0.0)
                partner = self.env['res.partner'].search([('name', 'ilike', cust_name)], limit=1)
                if not partner:
                    partner = self.env['res.partner'].create({'name': cust_name, 'customer_rank': 1})
                self.env['account.opening.receivable.line'].create({
                    'wizard_id': self.id,
                    'partner_id': partner.id,
                    'invoice_ref': ref or 'INV-SALDO-AWAL',
                    'invoice_date': inv_date or self.date_cut_off,
                    'due_date': due_date or self.date_cut_off,
                    'amount': amount,
                })

        # 3. Parse Hutang_Pemasok
        if "Hutang_Pemasok" in wb.sheetnames:
            ws = wb["Hutang_Pemasok"]
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]: continue
                supp_name, ref, bill_date, due_date, amount = row[0], str(row[1] or ''), row[2], row[3], float(row[4] or 0.0)
                partner = self.env['res.partner'].search([('name', 'ilike', supp_name)], limit=1)
                if not partner:
                    partner = self.env['res.partner'].create({'name': supp_name, 'supplier_rank': 1})
                self.env['account.opening.payable.line'].create({
                    'wizard_id': self.id,
                    'partner_id': partner.id,
                    'bill_ref': ref or 'BILL-SALDO-AWAL',
                    'bill_date': bill_date or self.date_cut_off,
                    'due_date': due_date or self.date_cut_off,
                    'amount': amount,
                })

        # Recompute totals and return self form view
        self._compute_totals()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_validate_and_post(self):
        """Execute double-entry journal creation, individual invoices, and asset registers."""
        self.ensure_one()
        self._compute_totals()

        if self.total_assets <= 0 and self.total_liabilities <= 0:
            raise UserError(_("Tidak ada data saldo awal yang dimasukkan. Silakan isi minimal satu baris saldo."))

        # 1. Resolve equity account
        if self.equity_choice == 'owner_equity':
            equity_acc = self.equity_account_id
            if not equity_acc:
                raise ValidationError(_("Silakan pilih Akun Modal Pemilik / Modal Disetor."))
        elif self.equity_choice == 'retained_earnings':
            equity_acc = self.retained_earnings_account_id
            if not equity_acc:
                raise ValidationError(_("Silakan pilih Akun Laba Ditahan."))
        else:
            if not self.equity_account_id or not self.retained_earnings_account_id:
                raise ValidationError(_("Untuk mode split, kedua akun Modal Disetor dan Laba Ditahan wajib dipilih."))

        # 2. Resolve opening clearing account (Interim Account)
        clearing_account = self.env['account.account'].search(self._account_company_domain() + [
            ('code', '=like', '999%'),
            ('deprecated', '=', False)
        ], limit=1)
        if not clearing_account:
            clearing_account = self.equity_account_id

        move_lines = []

        # A. Kas & Bank lines
        for line in self.cash_line_ids:
            if line.amount > 0:
                move_lines.append((0, 0, {
                    'name': _('Saldo Awal: %s') % line.journal_id.name,
                    'account_id': line.account_id.id,
                    'debit': line.amount,
                    'credit': 0.0,
                }))

        # B. Persediaan Barang lines
        stock_account = False
        if self.stock_line_ids:
            stock_account = self.env['account.account'].search(self._account_company_domain() + [
                ('code', '=like', '114%'),
                ('deprecated', '=', False)
            ], limit=1) or clearing_account

            total_stock_val = sum(self.stock_line_ids.mapped('total_value'))
            if total_stock_val > 0:
                move_lines.append((0, 0, {
                    'name': _('Saldo Awal Persediaan Barang Dagang'),
                    'account_id': stock_account.id,
                    'debit': total_stock_val,
                    'credit': 0.0,
                }))

        # C. Aktiva Tetap lines
        for line in self.asset_line_ids:
            asset_acc = line.asset_account_id or self.env['account.account'].search(self._account_company_domain() + [
                ('code', '=like', '121%'),
                ('deprecated', '=', False)
            ], limit=1) or clearing_account

            acc_dep_acc = line.accumulated_account_id or self.env['account.account'].search(self._account_company_domain() + [
                ('code', '=like', '122%'),
                ('deprecated', '=', False)
            ], limit=1) or clearing_account

            if line.original_cost > 0:
                move_lines.append((0, 0, {
                    'name': _('Saldo Awal Perolehan Aset: %s') % line.name,
                    'account_id': asset_acc.id,
                    'debit': line.original_cost,
                    'credit': 0.0,
                }))
            if line.past_accumulated_depreciation > 0:
                move_lines.append((0, 0, {
                    'name': _('Akumulasi Penyusutan Aset: %s') % line.name,
                    'account_id': acc_dep_acc.id,
                    'debit': 0.0,
                    'credit': line.past_accumulated_depreciation,
                }))

        # D. AR Clearing offset (Debited in opening journal to counterbalance credited clearing in customer invoices)
        if self.total_receivable > 0:
            move_lines.append((0, 0, {
                'name': _('Clearing Saldo Awal Piutang Usaha'),
                'account_id': clearing_account.id,
                'debit': self.total_receivable,
                'credit': 0.0,
            }))

        # E. AP Clearing offset (Credited in opening journal to counterbalance debited clearing in vendor bills)
        if self.total_payable > 0:
            move_lines.append((0, 0, {
                'name': _('Clearing Saldo Awal Hutang Usaha'),
                'account_id': clearing_account.id,
                'debit': 0.0,
                'credit': self.total_payable,
            }))

        # F. Equity balancing line
        net_equity = self.calculated_equity
        if self.equity_choice == 'split':
            capital_share = round(net_equity * (self.equity_split_percent / 100.0), 2)
            retained_share = net_equity - capital_share
            if capital_share != 0:
                move_lines.append((0, 0, {
                    'name': _('Saldo Awal Modal Pemilik / Modal Disetor'),
                    'account_id': self.equity_account_id.id,
                    'debit': 0.0 if capital_share > 0 else abs(capital_share),
                    'credit': capital_share if capital_share > 0 else 0.0,
                }))
            if retained_share != 0:
                move_lines.append((0, 0, {
                    'name': _('Saldo Awal Laba Ditahan'),
                    'account_id': self.retained_earnings_account_id.id,
                    'debit': 0.0 if retained_share > 0 else abs(retained_share),
                    'credit': retained_share if retained_share > 0 else 0.0,
                }))
        else:
            target_acc = self.equity_account_id if self.equity_choice == 'owner_equity' else self.retained_earnings_account_id
            if net_equity != 0:
                move_lines.append((0, 0, {
                    'name': _('Saldo Awal Ekuitas Penyeimbang'),
                    'account_id': target_acc.id,
                    'debit': 0.0 if net_equity > 0 else abs(net_equity),
                    'credit': net_equity if net_equity > 0 else 0.0,
                }))

        # 3. Create Master Opening Journal Entry
        master_move = self.env['account.move'].create({
            'journal_id': self.journal_id.id,
            'date': self.date_cut_off,
            'ref': _('Setup Saldo Awal - Cut-off %s') % self.date_cut_off,
            'move_type': 'entry',
            'is_opening_balance': True,
            'line_ids': move_lines,
        })
        master_move.action_post()

        # 4. Generate Individual Posted Customer Invoices (AR)
        sale_journal = self.env['account.journal'].search([
            ('company_id', '=', self.company_id.id),
            ('type', '=', 'sale')
        ], limit=1) or self.journal_id

        for rec_line in self.receivable_line_ids:
            inv = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec_line.partner_id.id,
                'journal_id': sale_journal.id,
                'invoice_date': self.date_cut_off,
                'invoice_date_due': rec_line.due_date,
                'payment_reference': rec_line.invoice_ref,
                'ref': _('Saldo Awal Piutang: %s') % rec_line.invoice_ref,
                'is_opening_balance': True,
                'invoice_line_ids': [(0, 0, {
                    'name': _('Saldo Awal Piutang Faktur %s') % rec_line.invoice_ref,
                    'quantity': 1.0,
                    'price_unit': rec_line.amount,
                    'account_id': clearing_account.id,
                    'tax_ids': False,
                })],
            })
            inv.action_post()

        # 5. Generate Individual Posted Vendor Bills (AP)
        purchase_journal = self.env['account.journal'].search([
            ('company_id', '=', self.company_id.id),
            ('type', '=', 'purchase')
        ], limit=1) or self.journal_id

        for pay_line in self.payable_line_ids:
            bill = self.env['account.move'].create({
                'move_type': 'in_invoice',
                'partner_id': pay_line.partner_id.id,
                'journal_id': purchase_journal.id,
                'invoice_date': self.date_cut_off,
                'invoice_date_due': pay_line.due_date,
                'payment_reference': pay_line.bill_ref,
                'ref': _('Saldo Awal Hutang: %s') % pay_line.bill_ref,
                'is_opening_balance': True,
                'invoice_line_ids': [(0, 0, {
                    'name': _('Saldo Awal Hutang Tagihan %s') % pay_line.bill_ref,
                    'quantity': 1.0,
                    'price_unit': pay_line.amount,
                    'account_id': clearing_account.id,
                    'tax_ids': False,
                })],
            })
            bill.action_post()

        # 6. Generate Simple Asset Register Cards
        for asset_line in self.asset_line_ids:
            asset = self.env['account.simple.asset'].create({
                'name': asset_line.name,
                'company_id': self.company_id.id,
                'asset_group': asset_line.asset_group,
                'acquisition_date': asset_line.acquisition_date,
                'start_depreciation_date': self.date_cut_off + relativedelta(days=1),
                'original_cost': asset_line.original_cost,
                'past_accumulated_depreciation': asset_line.past_accumulated_depreciation,
                'asset_account_id': asset_line.asset_account_id.id if asset_line.asset_account_id else False,
                'accumulated_account_id': asset_line.accumulated_account_id.id if asset_line.accumulated_account_id else False,
                'expense_account_id': asset_line.expense_account_id.id if asset_line.expense_account_id else False,
            })
            asset.action_compute_board()

        # 7. Update Physical Stock Quants if option enabled
        if self.update_physical_stock and self.stock_line_ids:
            dest_location = False
            if self.warehouse_id:
                dest_location = self.warehouse_id.lot_stock_id
            elif self.stock_line_ids[0].location_id:
                dest_location = self.stock_line_ids[0].location_id
            else:
                dest_location = self.env['stock.location'].search([
                    ('company_id', 'in', (self.company_id.id, False)),
                    ('usage', '=', 'internal')
                ], limit=1)

            if dest_location:
                for s_line in self.stock_line_ids:
                    quant = self.env['stock.quant'].search([
                        ('product_id', '=', s_line.product_id.id),
                        ('location_id', '=', dest_location.id)
                    ], limit=1)
                    if quant:
                        quant.inventory_quantity = s_line.quantity
                        quant.action_apply_inventory()
                    else:
                        new_quant = self.env['stock.quant'].create({
                            'product_id': s_line.product_id.id,
                            'location_id': dest_location.id,
                            'inventory_quantity': s_line.quantity,
                        })
                        new_quant.action_apply_inventory()

        # 8. Lock Fiscal Date if option enabled
        if self.lock_fiscal_date:
            self.company_id.sudo().write({
                'fiscalyear_lock_date': self.date_cut_off,
            })

        # Return action viewing the newly posted opening balance journal entry
        return {
            'name': _('Jurnal Saldo Awal Terposting'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': master_move.id,
            'view_mode': 'form',
            'target': 'current',
        }
