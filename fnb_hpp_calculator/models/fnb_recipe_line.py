# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FnbRecipeLine(models.Model):
    _name = 'fnb.recipe.line'
    _description = 'F&B Recipe Ingredient Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    recipe_id = fields.Many2one('fnb.recipe', string='Recipe', required=True, ondelete='cascade')
    product_id = fields.Many2one(
        'product.product',
        string='Raw Ingredient',
        required=True,
        domain=[('type', 'in', ['consu', 'product', 'service'])]
    )
    name = fields.Char(string='Ingredient Specification')
    quantity = fields.Float(string='Portion Quantity', required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    currency_id = fields.Many2one('res.currency', related='recipe_id.currency_id', readonly=True)
    unit_cost = fields.Monetary(
        string='Unit Cost',
        currency_field='currency_id',
        compute='_compute_unit_cost',
        store=True,
        readonly=False,
        precompute=True,
        help='Unit cost of ingredient. Pre-populated automatically from product purchase cost / standard price.'
    )
    waste_percent = fields.Float(
        string='Waste / Shrinkage (%)',
        default=0.0,
        help='Percentage of raw material lost during peeling, trimming, cooking, or portioning'
    )
    effective_cost = fields.Monetary(
        string='Subtotal Cost',
        currency_field='currency_id',
        compute='_compute_effective_cost',
        store=True,
        help='Net cost adjusted for preparation waste factor'
    )

    @api.depends('product_id')
    def _compute_unit_cost(self):
        for line in self:
            if line.product_id and not line.unit_cost:
                line.unit_cost = line.product_id.standard_price
            elif not line.product_id:
                line.unit_cost = 0.0

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.display_name
            self.uom_id = self.product_id.uom_id
            self.unit_cost = self.product_id.standard_price

    @api.constrains('waste_percent')
    def _check_waste_percent(self):
        for record in self:
            if record.waste_percent < 0 or record.waste_percent >= 100:
                raise ValidationError(_("Waste / shrinkage percentage must be between 0% and 99.9%."))

    @api.depends('quantity', 'unit_cost', 'waste_percent')
    def _compute_effective_cost(self):
        for record in self:
            base_amount = record.quantity * record.unit_cost
            if record.waste_percent > 0:
                # E.g. If waste is 20%, 1kg raw only yields 0.8kg usable, effective cost factor = 1 / (1 - 0.2) = 1.25x
                divisor = (100.0 - record.waste_percent) / 100.0
                record.effective_cost = base_amount / divisor if divisor > 0 else base_amount
            else:
                record.effective_cost = base_amount
