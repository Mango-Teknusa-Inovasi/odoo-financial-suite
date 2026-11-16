# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FnbRecipePackagingLine(models.Model):
    _name = 'fnb.recipe.packaging.line'
    _description = 'F&B Recipe Packaging & Disposables'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    recipe_id = fields.Many2one('fnb.recipe', string='Recipe', required=True, ondelete='cascade')
    product_id = fields.Many2one(
        'product.product',
        string='Packaging Item',
        required=True
    )
    name = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit')
    currency_id = fields.Many2one('res.currency', related='recipe_id.currency_id', readonly=True)
    unit_cost = fields.Monetary(
        string='Unit Cost',
        currency_field='currency_id',
        required=True,
        default=0.0
    )
    subtotal_cost = fields.Monetary(
        string='Subtotal Cost',
        currency_field='currency_id',
        compute='_compute_subtotal_cost',
        store=True
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.display_name
            self.uom_id = self.product_id.uom_id
            self.unit_cost = self.product_id.standard_price

    @api.depends('quantity', 'unit_cost')
    def _compute_subtotal_cost(self):
        for record in self:
            record.subtotal_cost = record.quantity * record.unit_cost
