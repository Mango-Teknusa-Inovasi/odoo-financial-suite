# -*- coding: utf-8 -*-
from odoo import models, fields

class FnbRecipeCategory(models.Model):
    _name = 'fnb.recipe.category'
    _description = 'F&B Recipe Category'
    _order = 'sequence, name'

    name = fields.Char(string='Category Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    target_food_cost_percent = fields.Float(
        string='Target Food Cost (%)',
        default=30.0,
        help='Benchmark target food cost percentage (typically 28% to 35% in culinary industry)'
    )
    description = fields.Text(string='Description')
    recipe_count = fields.Integer(string='Recipe Count', compute='_compute_recipe_count')

    def _compute_recipe_count(self):
        for record in self:
            record.recipe_count = self.env['fnb.recipe'].search_count([('category_id', '=', record.id)])
