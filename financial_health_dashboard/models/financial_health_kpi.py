# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FinancialHealthKpi(models.Model):
    _name = 'financial.health.kpi'
    _description = 'Executive Financial Health & Ratio Evaluation'
    _order = 'create_date desc'

    name = fields.Char(string='Evaluation Title', required=True, default=lambda self: _('Executive Health Review - %s') % fields.Date.today().strftime('%B %Y'))
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True)
    
    period_type = fields.Selection([
        ('current_month', 'Current Month'),
        ('current_quarter', 'Current Quarter'),
        ('ytd', 'Year-to-Date (YTD)'),
        ('all_time', 'All Cumulative Transactions'),
    ], string='Evaluation Period', default='all_time', required=True)
    
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date', default=fields.Date.context_today)
    date_computed = fields.Datetime(string='Calculated At', readonly=True)

    # ---------------------------------------------------------
    # Balance Sheet Aggregates
    # ---------------------------------------------------------
    total_cash = fields.Monetary(string='Cash & Bank Balances', currency_field='currency_id', readonly=True)
    total_receivables = fields.Monetary(string='Trade Receivables (AR)', currency_field='currency_id', readonly=True)
    total_current_assets = fields.Monetary(string='Total Current Assets', currency_field='currency_id', readonly=True)
    total_fixed_assets = fields.Monetary(string='Fixed & Non-Current Assets', currency_field='currency_id', readonly=True)
    total_assets = fields.Monetary(string='Total Assets', currency_field='currency_id', readonly=True)
    
    total_current_liabilities = fields.Monetary(string='Current Liabilities (AP & Taxes)', currency_field='currency_id', readonly=True)
    total_long_term_liabilities = fields.Monetary(string='Long-Term Debt', currency_field='currency_id', readonly=True)
    total_liabilities = fields.Monetary(string='Total Liabilities', currency_field='currency_id', readonly=True)
    
    total_equity = fields.Monetary(string='Total Equity & Retained Earnings', currency_field='currency_id', readonly=True)
    working_capital = fields.Monetary(string='Net Working Capital', currency_field='currency_id', readonly=True)

    # ---------------------------------------------------------
    # Income Statement Aggregates
    # ---------------------------------------------------------
    total_revenue = fields.Monetary(string='Total Revenue (Turnover)', currency_field='currency_id', readonly=True)
    cogs = fields.Monetary(string='Cost of Goods Sold (COGS)', currency_field='currency_id', readonly=True)
    gross_profit = fields.Monetary(string='Gross Operating Profit', currency_field='currency_id', readonly=True)
    operating_expenses = fields.Monetary(string='Operating & General Expenses', currency_field='currency_id', readonly=True)
    net_profit = fields.Monetary(string='Net Profit After Tax', currency_field='currency_id', readonly=True)

    # ---------------------------------------------------------
    # Key Financial Ratios & Health Badges
    # ---------------------------------------------------------
    # 1. Liquidity
    current_ratio = fields.Float(string='Current Ratio', digits=(16, 2), readonly=True, help="Current Assets / Current Liabilities (Safe benchmark >= 1.5x - 2.0x)")
    current_ratio_status = fields.Selection([
        ('optimal', 'Optimal (>= 2.0x)'),
        ('moderate', 'Moderate (1.2x - 1.99x)'),
        ('critical', 'Critical Liquidity Risk (< 1.2x)'),
    ], string='Current Ratio Health', readonly=True)

    quick_ratio = fields.Float(string='Quick Ratio (Acid-Test)', digits=(16, 2), readonly=True, help="(Cash + Receivables) / Current Liabilities (Safe benchmark >= 1.0x)")
    quick_ratio_status = fields.Selection([
        ('optimal', 'Optimal (>= 1.0x)'),
        ('moderate', 'Moderate (0.7x - 0.99x)'),
        ('critical', 'Immediate Risk (< 0.7x)'),
    ], string='Quick Ratio Health', readonly=True)

    cash_ratio = fields.Float(string='Cash Ratio', digits=(16, 2), readonly=True, help="Cash & Bank / Current Liabilities (Safe benchmark >= 0.2x)")
    cash_ratio_status = fields.Selection([
        ('optimal', 'Optimal (>= 0.5x)'),
        ('moderate', 'Moderate (0.2x - 0.49x)'),
        ('critical', 'Cash Shortage (< 0.2x)'),
    ], string='Cash Ratio Health', readonly=True)

    # 2. Solvency
    debt_to_equity_ratio = fields.Float(string='Debt-to-Equity (DER)', digits=(16, 2), readonly=True, help="Total Liabilities / Total Equity (Safe benchmark <= 1.5x)")
    der_status = fields.Selection([
        ('optimal', 'Conservative (<= 1.0x)'),
        ('moderate', 'Moderate (1.01x - 2.0x)'),
        ('critical', 'High Solvency Leverage (> 2.0x)'),
    ], string='DER Health', readonly=True)

    debt_to_asset_ratio = fields.Float(string='Debt-to-Asset (DAR)', digits=(16, 2), readonly=True, help="Total Liabilities / Total Assets (Safe benchmark <= 0.5x)")
    dar_status = fields.Selection([
        ('optimal', 'Optimal (<= 0.4x)'),
        ('moderate', 'Moderate (0.41x - 0.6x)'),
        ('critical', 'Overleveraged (> 0.6x)'),
    ], string='DAR Health', readonly=True)

    # 3. Profitability
    gross_profit_margin = fields.Float(string='Gross Profit Margin (GPM %)', digits=(16, 1), readonly=True, help="(Revenue - COGS) / Revenue * 100%")
    gpm_status = fields.Selection([
        ('optimal', 'Strong Margin (>= 40%)'),
        ('moderate', 'Average Margin (20% - 39.9%)'),
        ('critical', 'Thin Margin (< 20%)'),
    ], string='GPM Health', readonly=True)

    net_profit_margin = fields.Float(string='Net Profit Margin (NPM %)', digits=(16, 1), readonly=True, help="Net Profit / Revenue * 100%")
    npm_status = fields.Selection([
        ('optimal', 'Highly Profitable (>= 15%)'),
        ('moderate', 'Moderate Profit (5% - 14.9%)'),
        ('critical', 'Low / Negative Profit (< 5%)'),
    ], string='NPM Health', readonly=True)

    # Overall Summary
    overall_score = fields.Integer(string='Financial Health Score (0-100)', readonly=True)
    overall_status = fields.Selection([
        ('excellent', 'Excellent (Solid Liquidity & Margins)'),
        ('good', 'Good (Healthy Operations)'),
        ('fair', 'Fair (Moderate Caution Advised)'),
        ('critical', 'Attention Required (Liquidity or Solvency Risk)'),
    ], string='Executive Health Status', readonly=True)
    
    executive_summary = fields.Html(string='Executive Advisory Analysis', readonly=True)

    @api.onchange('period_type')
    def _onchange_period_type(self):
        today = date.today()
        if self.period_type == 'current_month':
            self.date_from = today.replace(day=1)
            self.date_to = today
        elif self.period_type == 'current_quarter':
            quarter_start_month = ((today.month - 1) // 3) * 3 + 1
            self.date_from = today.replace(month=quarter_start_month, day=1)
            self.date_to = today
        elif self.period_type == 'ytd':
            self.date_from = today.replace(month=1, day=1)
            self.date_to = today
        elif self.period_type == 'all_time':
            self.date_from = False
            self.date_to = today

    def action_compute_ratios(self):
        """Aggregate ledger balances from account.move.line and calculate all executive ratios."""
        for rec in self:
            domain = [
                ('company_id', '=', rec.company_id.id),
                ('move_id.state', '=', 'posted'),
            ]
            if rec.date_from:
                domain.append(('date', '>=', rec.date_from))
            if rec.date_to:
                domain.append(('date', '<=', rec.date_to))

            lines = self.env['account.move.line'].search(domain)

            # 1. Assets
            cash = sum(lines.filtered(lambda l: l.account_id.account_type in ('asset_cash',)).mapped('balance'))
            receivables = sum(lines.filtered(lambda l: l.account_id.account_type in ('asset_receivable',)).mapped('balance'))
            current_assets = sum(lines.filtered(lambda l: l.account_id.account_type in ('asset_cash', 'asset_receivable', 'asset_current', 'asset_prepayments')).mapped('balance'))
            fixed_assets = sum(lines.filtered(lambda l: l.account_id.account_type in ('asset_fixed', 'asset_non_current')).mapped('balance'))
            total_assets = current_assets + fixed_assets

            # 2. Liabilities
            current_liabilities = -sum(lines.filtered(lambda l: l.account_id.account_type in ('liability_payable', 'liability_current')).mapped('balance'))
            long_term_liabilities = -sum(lines.filtered(lambda l: l.account_id.account_type in ('liability_non_current',)).mapped('balance'))
            total_liabilities = current_liabilities + long_term_liabilities

            # 3. Revenue & Profitability
            revenue = -sum(lines.filtered(lambda l: l.account_id.account_type in ('income', 'income_other')).mapped('balance'))
            cogs = sum(lines.filtered(lambda l: l.account_id.account_type in ('expense_direct_cost',)).mapped('balance'))
            gross_profit = revenue - cogs
            operating_expenses = sum(lines.filtered(lambda l: l.account_id.account_type in ('expense', 'expense_depreciation')).mapped('balance'))
            net_profit = gross_profit - operating_expenses

            # 4. Equity & Working Capital
            retained_equity = -sum(lines.filtered(lambda l: l.account_id.account_type in ('equity', 'equity_unaffected')).mapped('balance'))
            total_equity = retained_equity + net_profit
            working_capital = current_assets - current_liabilities

            # 5. Calculate Ratios
            # Current Ratio
            if current_liabilities > 0:
                cr = current_assets / current_liabilities
                qr = (cash + receivables) / current_liabilities
                cash_r = cash / current_liabilities
            else:
                cr = 99.0 if current_assets > 0 else 0.0
                qr = 99.0 if (cash + receivables) > 0 else 0.0
                cash_r = 99.0 if cash > 0 else 0.0

            cr_status = 'optimal' if cr >= 2.0 else ('moderate' if cr >= 1.2 else 'critical')
            qr_status = 'optimal' if qr >= 1.0 else ('moderate' if qr >= 0.7 else 'critical')
            cash_status = 'optimal' if cash_r >= 0.5 else ('moderate' if cash_r >= 0.2 else 'critical')

            # Solvency Ratios
            if total_equity > 0:
                der = total_liabilities / total_equity
            else:
                der = 99.0 if total_liabilities > 0 else 0.0

            if total_assets > 0:
                dar = total_liabilities / total_assets
            else:
                dar = 0.0

            der_status = 'optimal' if der <= 1.0 else ('moderate' if der <= 2.0 else 'critical')
            dar_status = 'optimal' if dar <= 0.4 else ('moderate' if dar <= 0.6 else 'critical')

            # Profitability Ratios
            if revenue > 0:
                gpm = (gross_profit / revenue) * 100.0
                npm = (net_profit / revenue) * 100.0
            else:
                gpm = 0.0
                npm = 0.0

            gpm_status = 'optimal' if gpm >= 40.0 else ('moderate' if gpm >= 20.0 else 'critical')
            npm_status = 'optimal' if npm >= 15.0 else ('moderate' if npm >= 5.0 else 'critical')

            # 6. Overall Financial Health Score (Weighted 0-100)
            score = 0
            # Liquidity component (35 pts)
            if cr >= 2.0: score += 20
            elif cr >= 1.2: score += 12
            else: score += 4

            if qr >= 1.0: score += 15
            elif qr >= 0.7: score += 9
            else: score += 3

            # Solvency component (30 pts)
            if der <= 1.0: score += 20
            elif der <= 2.0: score += 12
            else: score += 4

            if dar <= 0.4: score += 10
            elif dar <= 0.6: score += 6
            else: score += 2

            # Profitability component (35 pts)
            if gpm >= 40.0: score += 18
            elif gpm >= 20.0: score += 10
            else: score += 3

            if npm >= 15.0: score += 17
            elif npm >= 5.0: score += 10
            else: score += 2

            if score >= 80:
                overall_status = 'excellent'
            elif score >= 65:
                overall_status = 'good'
            elif score >= 50:
                overall_status = 'fair'
            else:
                overall_status = 'critical'

            # 7. Generate Actionable Executive Advisory Narrative
            notes = []
            if cr >= 2.0:
                notes.append(f"<li><strong>Strong Short-Term Liquidity:</strong> Current Ratio is <strong>{cr:.2f}x</strong>, indicating ample current assets to settle short-term commitments.</li>")
            elif cr < 1.2:
                notes.append(f"<li class='text-danger'><strong>Liquidity Warning:</strong> Current Ratio is <strong>{cr:.2f}x</strong> (&lt; 1.2x). Prioritize customer collections to prevent potential cash squeeze.</li>")

            if cash_r < 0.2 and receivables > 0:
                notes.append(f"<li class='text-warning'><strong>High Uncollected Receivables:</strong> Cash balance is tight while Trade Receivables stand at <strong>Rp {receivables:,.2f}</strong>. Focus on accelerating invoice collections.</li>")

            if der <= 1.0:
                notes.append(f"<li><strong>Conservative Leverage:</strong> Debt-to-Equity is <strong>{der:.2f}x</strong>, indicating safe reliance on company equity rather than external debt.</li>")
            elif der > 2.0:
                notes.append(f"<li class='text-danger'><strong>High Debt Exposure:</strong> Total liabilities exceed equity by <strong>{der:.2f}x</strong>. Refinancing or equity injection recommended.</li>")

            if npm >= 15.0:
                notes.append(f"<li><strong>High Net Margins:</strong> Business retains <strong>{npm:.1f}%</strong> of total revenue as pure net profit.</li>")
            elif npm < 5.0:
                notes.append(f"<li class='text-danger'><strong>Thin Net Profitability:</strong> Net Profit Margin is only <strong>{npm:.1f}%</strong>. Review operating expenses and supplier pricing.</li>")

            executive_summary = f"""
            <div class="p-3 bg-light rounded">
                <h5 class="fw-bold mb-2">Executive Advisory Synthesis (Health Score: {score}/100)</h5>
                <ul class="mb-0 ps-3">
                    {''.join(notes)}
                </ul>
            </div>
            """

            rec.write({
                'date_computed': fields.Datetime.now(),
                'total_cash': cash,
                'total_receivables': receivables,
                'total_current_assets': current_assets,
                'total_fixed_assets': fixed_assets,
                'total_assets': total_assets,
                'total_current_liabilities': current_liabilities,
                'total_long_term_liabilities': long_term_liabilities,
                'total_liabilities': total_liabilities,
                'total_equity': total_equity,
                'working_capital': working_capital,
                'total_revenue': revenue,
                'cogs': cogs,
                'gross_profit': gross_profit,
                'operating_expenses': operating_expenses,
                'net_profit': net_profit,
                'current_ratio': cr,
                'current_ratio_status': cr_status,
                'quick_ratio': qr,
                'quick_ratio_status': qr_status,
                'cash_ratio': cash_r,
                'cash_ratio_status': cash_status,
                'debt_to_equity_ratio': der,
                'der_status': der_status,
                'debt_to_asset_ratio': dar,
                'dar_status': dar_status,
                'gross_profit_margin': gpm,
                'gpm_status': gpm_status,
                'net_profit_margin': npm,
                'npm_status': npm_status,
                'overall_score': score,
                'overall_status': overall_status,
                'executive_summary': executive_summary,
            })

    # Drilldown Navigation Actions
    def action_view_receivables(self):
        self.ensure_one()
        return {
            'name': _('Customer Receivables Ledger'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.line',
            'view_mode': 'list,kanban',
            'domain': [('account_id.account_type', '=', 'asset_receivable'), ('company_id', '=', self.company_id.id)],
            'context': {'search_default_posted': 1},
        }

    def action_view_payables(self):
        self.ensure_one()
        return {
            'name': _('Vendor Payables Ledger'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.line',
            'view_mode': 'list,kanban',
            'domain': [('account_id.account_type', '=', 'liability_payable'), ('company_id', '=', self.company_id.id)],
            'context': {'search_default_posted': 1},
        }

    def action_view_general_ledger(self):
        self.ensure_one()
        return {
            'name': _('Journal Entries'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('company_id', '=', self.company_id.id), ('state', '=', 'posted')],
        }
