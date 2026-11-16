# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FnbRecipeSimulateWizard(models.TransientModel):
    _name = 'fnb.recipe.simulate.wizard'
    _description = 'F&B Menu Pricing & Margin Simulator'

    recipe_id = fields.Many2one('fnb.recipe', string='Recipe', required=True)
    currency_id = fields.Many2one('res.currency', related='recipe_id.currency_id')
    current_cost_per_portion = fields.Monetary(string='Base HPP / Portion', currency_field='currency_id', readonly=True)
    current_selling_price = fields.Monetary(string='Current Selling Price', currency_field='currency_id', readonly=True)
    current_margin_percent = fields.Float(string='Current Margin (%)', readonly=True)

    simulation_mode = fields.Selection([
        ('target_margin', 'Set Target Gross Margin (%) -> Compute Required Price'),
        ('target_price', 'Set Proposed Selling Price -> Compute Resulting Margin (%)'),
    ], string='Simulation Method', default='target_margin', required=True)

    target_margin_percent = fields.Float(string='Target Margin (%)', default=65.0)
    target_selling_price = fields.Monetary(string='Proposed Selling Price', currency_field='currency_id')

    simulated_selling_price = fields.Monetary(
        string='Suggested Selling Price',
        currency_field='currency_id',
        compute='_compute_simulation'
    )
    simulated_gross_profit = fields.Monetary(
        string='Projected Gross Profit',
        currency_field='currency_id',
        compute='_compute_simulation'
    )
    simulated_margin_percent = fields.Float(
        string='Projected Margin (%)',
        compute='_compute_simulation'
    )
    simulated_food_cost_percent = fields.Float(
        string='Projected Food Cost (%)',
        compute='_compute_simulation'
    )

    @api.depends('simulation_mode', 'target_margin_percent', 'target_selling_price', 'current_cost_per_portion')
    def _compute_simulation(self):
        for wizard in self:
            cost = wizard.current_cost_per_portion
            if wizard.simulation_mode == 'target_margin':
                margin = wizard.target_margin_percent
                if margin < 100.0 and cost > 0:
                    price = cost / ((100.0 - margin) / 100.0)
                else:
                    price = cost
                profit = price - cost
                food_cost = (cost / price * 100.0) if price > 0 else 0.0

                wizard.simulated_selling_price = price
                wizard.simulated_gross_profit = profit
                wizard.simulated_margin_percent = margin
                wizard.simulated_food_cost_percent = food_cost
            else:
                price = wizard.target_selling_price
                profit = price - cost
                margin = (profit / price * 100.0) if price > 0 else 0.0
                food_cost = (cost / price * 100.0) if price > 0 else 0.0

                wizard.simulated_selling_price = price
                wizard.simulated_gross_profit = profit
                wizard.simulated_margin_percent = margin
                wizard.simulated_food_cost_percent = food_cost

    def action_apply_to_recipe(self):
        self.ensure_one()
        if self.simulated_selling_price <= 0:
            raise ValidationError(_("Simulated selling price must be greater than zero."))
        self.recipe_id.selling_price = self.simulated_selling_price
        return {'type': 'ir.actions.act_window_close'}
