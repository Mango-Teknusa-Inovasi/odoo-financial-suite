# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FnbRecipe(models.Model):
    _name = 'fnb.recipe'
    _description = 'F&B Recipe Costing Card'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Menu / Recipe Name', required=True, tracking=True)
    code = fields.Char(string='Recipe Code / SKU', copy=False)
    active = fields.Boolean(default=True)
    category_id = fields.Many2one('fnb.recipe.category', string='Category', required=True, tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True
    )
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    product_id = fields.Many2one(
        'product.product',
        string='Linked POS/Sales Product',
        help='Link this recipe card to a sellable Odoo catalog product'
    )
    portion_yield = fields.Float(
        string='Portion Yield',
        default=1.0,
        required=True,
        help='Number of sellable servings or portions produced per recipe batch'
    )
    overhead_percent = fields.Float(
        string='Kitchen Overhead Buffer (%)',
        default=5.0,
        help='Allocation buffer for energy, gas, water, and culinary prep labor'
    )

    # Line relationships
    line_ids = fields.One2many('fnb.recipe.line', 'recipe_id', string='Raw Material Ingredients', copy=True)
    packaging_line_ids = fields.One2many('fnb.recipe.packaging.line', 'recipe_id', string='Packaging & Disposables', copy=True)

    # Computed Costing & Margin KPIs
    cost_ingredients = fields.Monetary(
        string='Ingredients Cost',
        currency_field='currency_id',
        compute='_compute_cost_and_margins',
        store=True,
        tracking=True
    )
    cost_packaging = fields.Monetary(
        string='Packaging Cost',
        currency_field='currency_id',
        compute='_compute_cost_and_margins',
        store=True
    )
    cost_overhead = fields.Monetary(
        string='Overhead Cost',
        currency_field='currency_id',
        compute='_compute_cost_and_margins',
        store=True
    )
    cost_total_batch = fields.Monetary(
        string='Total Batch Cost',
        currency_field='currency_id',
        compute='_compute_cost_and_margins',
        store=True
    )
    cost_per_portion = fields.Monetary(
        string='HPP / Portion Cost',
        currency_field='currency_id',
        compute='_compute_cost_and_margins',
        store=True,
        tracking=True
    )
    selling_price = fields.Monetary(
        string='Target Selling Price',
        currency_field='currency_id',
        default=0.0,
        tracking=True
    )
    gross_profit = fields.Monetary(
        string='Gross Profit',
        currency_field='currency_id',
        compute='_compute_cost_and_margins',
        store=True
    )
    gross_margin_percent = fields.Float(
        string='Gross Margin (%)',
        compute='_compute_cost_and_margins',
        store=True,
        tracking=True
    )
    food_cost_percent = fields.Float(
        string='Food Cost (%)',
        compute='_compute_cost_and_margins',
        store=True
    )
    margin_status = fields.Selection([
        ('optimal', 'Optimal (Margin >= 65%)'),
        ('moderate', 'Moderate (50% - 64%)'),
        ('warning', 'Low / Underpriced (< 50%)'),
    ], string='Margin Health Status', compute='_compute_cost_and_margins', store=True)

    ingredient_count = fields.Integer(string='Ingredient Count', compute='_compute_ingredient_count')
    notes = fields.Html(string='Chef Preparation Guide / Standard Operating Procedure (SOP)')

    @api.constrains('portion_yield')
    def _check_portion_yield(self):
        for record in self:
            if record.portion_yield <= 0:
                raise ValidationError(_("Portion yield must be greater than zero."))

    @api.depends('line_ids.effective_cost', 'packaging_line_ids.subtotal_cost', 'overhead_percent', 'portion_yield', 'selling_price')
    def _compute_cost_and_margins(self):
        for record in self:
            c_ing = sum(record.line_ids.mapped('effective_cost'))
            c_pkg = sum(record.packaging_line_ids.mapped('subtotal_cost'))
            c_ovh = (c_ing + c_pkg) * (record.overhead_percent / 100.0)
            c_batch = c_ing + c_pkg + c_ovh
            
            yield_val = record.portion_yield if record.portion_yield > 0 else 1.0
            c_portion = c_batch / yield_val

            record.cost_ingredients = c_ing
            record.cost_packaging = c_pkg
            record.cost_overhead = c_ovh
            record.cost_total_batch = c_batch
            record.cost_per_portion = c_portion

            profit = record.selling_price - c_portion
            record.gross_profit = profit

            if record.selling_price > 0:
                m_pct = (profit / record.selling_price) * 100.0
                fc_pct = (c_portion / record.selling_price) * 100.0
            else:
                m_pct = 0.0
                fc_pct = 0.0

            record.gross_margin_percent = m_pct
            record.food_cost_percent = fc_pct

            if m_pct >= 65.0:
                record.margin_status = 'optimal'
            elif m_pct >= 50.0:
                record.margin_status = 'moderate'
            else:
                record.margin_status = 'warning'

    @api.depends('line_ids')
    def _compute_ingredient_count(self):
        for record in self:
            record.ingredient_count = len(record.line_ids)

    def action_sync_to_product(self):
        """Update linked catalog product's standard_price (cost) and list_price (selling price)."""
        self.ensure_one()
        if not self.product_id:
            raise ValidationError(_("Please link a Sales/POS Product before syncing."))
        self.product_id.standard_price = self.cost_per_portion
        if self.selling_price > 0:
            self.product_id.list_price = self.selling_price
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Product Synchronized'),
                'message': _('Product %s updated: Standard Cost = %s, List Price = %s') % (
                    self.product_id.name, self.cost_per_portion, self.selling_price
                ),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_refresh_ingredient_costs(self):
        """Fetch latest standard costs from product catalog for all ingredients."""
        for line in self.line_ids:
            if line.product_id:
                line.unit_cost = line.product_id.standard_price
        for pkg in self.packaging_line_ids:
            if pkg.product_id:
                pkg.unit_cost = pkg.product_id.standard_price
        return True

    def action_open_simulator(self):
        self.ensure_one()
        return {
            'name': _('Price & Margin Simulator'),
            'type': 'ir.actions.act_window',
            'res_model': 'fnb.recipe.simulate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_recipe_id': self.id,
                'default_current_cost_per_portion': self.cost_per_portion,
                'default_current_selling_price': self.selling_price,
                'default_current_margin_percent': self.gross_margin_percent,
                'default_target_margin_percent': 65.0,
            }
        }
