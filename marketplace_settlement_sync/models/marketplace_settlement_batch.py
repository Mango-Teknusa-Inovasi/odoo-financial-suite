# -*- coding: utf-8 -*-
import io
import csv
import base64
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

try:
    import openpyxl
except ImportError:
    openpyxl = None

class MarketplaceSettlementBatch(models.Model):
    _name = 'marketplace.settlement.batch'
    _description = 'Marketplace Settlement Ingestion Batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Batch Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New Settlement Batch')
    )
    channel_id = fields.Many2one(
        'marketplace.channel',
        string='Marketplace Channel',
        required=True
    )
    company_id = fields.Many2one(
        related='channel_id.company_id',
        store=True,
        readonly=True
    )
    currency_id = fields.Many2one(
        related='company_id.currency_id',
        string='Currency',
        readonly=True
    )

    date = fields.Date(
        string='Settlement Date',
        required=True,
        default=fields.Date.context_today
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('parsed', 'Parsed & Verified'),
        ('posted', 'Journal Posted'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    file_data = fields.Binary(
        string='Settlement File (.xlsx / .csv)',
        required=True
    )
    file_name = fields.Char(string='File Name')

    line_ids = fields.One2many(
        'marketplace.settlement.line',
        'batch_id',
        string='Settlement Line Items'
    )

    move_id = fields.Many2one(
        'account.move',
        string='Generated Journal Entry',
        readonly=True,
        copy=False
    )

    # Summary Computations
    total_orders = fields.Integer(string='Total Orders', compute='_compute_totals', store=True)
    total_gross_amount = fields.Monetary(string='Gross Sales Amount', compute='_compute_totals', store=True)
    total_service_fee = fields.Monetary(string='Marketplace Service Fees', compute='_compute_totals', store=True)
    total_shipping_fee = fields.Monetary(string='Shipping Deductions', compute='_compute_totals', store=True)
    total_net_amount = fields.Monetary(string='Net Escrow Settlement', compute='_compute_totals', store=True)

    @api.depends('line_ids.gross_amount', 'line_ids.service_fee', 'line_ids.shipping_fee', 'line_ids.net_amount')
    def _compute_totals(self):
        for batch in self:
            batch.total_orders = len(batch.line_ids)
            batch.total_gross_amount = sum(batch.line_ids.mapped('gross_amount'))
            batch.total_service_fee = sum(batch.line_ids.mapped('service_fee'))
            batch.total_shipping_fee = sum(batch.line_ids.mapped('shipping_fee'))
            batch.total_net_amount = sum(batch.line_ids.mapped('net_amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New Settlement Batch')) == _('New Settlement Batch'):
                seq = self.env['ir.sequence'].next_by_code('marketplace.settlement.batch') or _('BATCH/%s') % fields.Date.today().strftime('%Y%m%d')
                vals['name'] = seq
        return super().create(vals_list)

    def action_parse_file(self):
        self.ensure_one()
        if not self.file_data:
            raise UserError(_("Please upload a settlement file before parsing."))

        # Clear existing lines
        self.line_ids.unlink()

        raw_bytes = base64.b64decode(self.file_data)
        filename = (self.file_name or '').lower()

        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            self._parse_excel(raw_bytes)
        elif filename.endswith('.csv') or filename.endswith('.txt'):
            self._parse_csv(raw_bytes)
        else:
            # Fallback attempt excel then csv
            try:
                self._parse_excel(raw_bytes)
            except Exception:
                self._parse_csv(raw_bytes)

        if not self.line_ids:
            raise UserError(_("No valid settlement order records could be extracted from the uploaded file."))

        self.state = 'parsed'

    def _parse_csv(self, raw_bytes):
        text_stream = io.StringIO(raw_bytes.decode('utf-8-sig', errors='ignore'))
        reader = csv.reader(text_stream)
        headers = None
        lines = []

        for row in reader:
            if not row or not any(row):
                continue
            if headers is None:
                headers = [str(col).strip().lower() for col in row]
                continue

            parsed_line = self._extract_columns(headers, [str(c).strip() for c in row])
            if parsed_line:
                lines.append(parsed_line)

        self._batch_create_lines(lines)

    def _parse_excel(self, raw_bytes):
        if not openpyxl:
            raise UserError(_("Python library 'openpyxl' is required to parse Excel settlement files."))

        wb = openpyxl.load_workbook(io.BytesIO(raw_bytes), data_only=True)
        sheet = wb.active
        headers = None
        lines = []

        for row in sheet.iter_rows(values_only=True):
            if not row or not any(row):
                continue
            row_vals = [c for c in row]
            if headers is None:
                headers = [str(c).strip().lower() for c in row_vals if c is not None]
                continue

            parsed_line = self._extract_columns(headers, row_vals)
            if parsed_line:
                lines.append(parsed_line)

        self._batch_create_lines(lines)

    def _extract_columns(self, headers, row):
        """
        Extracts order reference, gross, fee, shipping, and net using flexible header detection.
        Matches Indonesian marketplace statements (Shopee, Tokopedia, TikTok Shop).
        """
        def find_val(keywords, default=0.0):
            for i, h in enumerate(headers):
                if any(k in h for k in keywords) and i < len(row):
                    val = row[i]
                    if val is None or val == '':
                        continue
                    if isinstance(val, (int, float)):
                        return float(val)
                    try:
                        clean_str = str(val).replace('Rp', '').replace('.', '').replace(',', '.').strip()
                        return float(clean_str)
                    except ValueError:
                        continue
            return default

        def find_str(keywords, default=''):
            for i, h in enumerate(headers):
                if any(k in h for k in keywords) and i < len(row):
                    val = row[i]
                    if val is not None and str(val).strip():
                        return str(val).strip()
            return default

        order_ref = find_str(['order', 'pesanan', 'no', 'invoice', 'id'])
        if not order_ref:
            return None

        gross = find_val(['gross', 'harga', 'penjualan', 'omzet', 'total produk', 'subtotal'])
        service_fee = abs(find_val(['fee', 'layanan', 'komisi', 'admin', 'biaya transaksi']))
        shipping_fee = abs(find_val(['shipping', 'ongkir', 'ongkos']))
        net = find_val(['net', 'bersih', 'diterima', 'saldo', 'payout', 'penghasilan'])

        # Auto-compute net if missing or zero
        if net == 0.0 and gross > 0.0:
            net = gross - service_fee - shipping_fee

        return {
            'batch_id': self.id,
            'order_ref': order_ref,
            'order_date': self.date,
            'customer_name': find_str(['buyer', 'customer', 'pembeli', 'nama']),
            'gross_amount': gross,
            'service_fee': service_fee,
            'shipping_fee': shipping_fee,
            'net_amount': net,
        }

    def _batch_create_lines(self, lines):
        if lines:
            self.env['marketplace.settlement.line'].create(lines)

    def action_create_journal_entry(self):
        self.ensure_one()
        if self.state != 'parsed':
            raise UserError(_("Settlement must be parsed before generating accounting entries."))

        channel = self.channel_id
        if not channel.journal_id or not channel.escrow_account_id or not channel.revenue_account_id or not channel.fee_account_id:
            raise ValidationError(_("Please configure all accounting accounts on the Marketplace Channel profile."))

        move_lines = []
        # 1. Debit Net Escrow / Clearing Account
        if self.total_net_amount > 0:
            move_lines.append((0, 0, {
                'name': f"{channel.name} Settlement Payout ({self.name})",
                'account_id': channel.escrow_account_id.id,
                'debit': self.total_net_amount,
                'credit': 0.0,
            }))

        # 2. Debit Marketplace Service & Admin Fee
        if self.total_service_fee > 0:
            move_lines.append((0, 0, {
                'name': f"{channel.name} Commission & Service Fees ({self.name})",
                'account_id': channel.fee_account_id.id,
                'debit': self.total_service_fee,
                'credit': 0.0,
            }))

        # 3. Debit Shipping Fee adjustment if configured
        if self.total_shipping_fee > 0:
            ship_account = channel.shipping_account_id or channel.fee_account_id
            move_lines.append((0, 0, {
                'name': f"{channel.name} Shipping Deductions ({self.name})",
                'account_id': ship_account.id,
                'debit': self.total_shipping_fee,
                'credit': 0.0,
            }))

        # 4. Credit Gross Sales Turnover
        if self.total_gross_amount > 0:
            move_lines.append((0, 0, {
                'name': f"{channel.name} Gross Sales Turnover ({self.name})",
                'account_id': channel.revenue_account_id.id,
                'debit': 0.0,
                'credit': self.total_gross_amount,
            }))

        move = self.env['account.move'].create({
            'journal_id': channel.journal_id.id,
            'date': self.date,
            'ref': f"Settlement {channel.name} - {self.name}",
            'move_type': 'entry',
            'line_ids': move_lines,
        })
        move.action_post()

        self.write({
            'move_id': move.id,
            'state': 'posted'
        })

        return {
            'type': 'ir.actions.act_window',
            'name': _('Generated Journal Entry'),
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_cancel(self):
        for batch in self:
            if batch.move_id and batch.move_id.state == 'posted':
                batch.move_id.button_draft()
                batch.move_id.button_cancel()
            batch.state = 'cancelled'

    def action_reset_draft(self):
        for batch in self:
            batch.state = 'draft'

    def action_view_journal_entry(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entry'),
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
