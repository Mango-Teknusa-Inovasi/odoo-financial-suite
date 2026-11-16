# -*- coding: utf-8 -*-
"""
Unit Tests for F&B Recipe HPP & Menu Costing Engine (fnb_hpp_calculator)
"""

import unittest

class TestFnBRecipeCosting(unittest.TestCase):
    """Test culinary recipe portion HPP, waste factor adjustments, and profit margin simulation."""

    def test_shrinkage_wastage_cost_adjustment(self):
        """Test ingredient cost inflation based on wastage/shrinkage percentage."""
        base_unit_cost = 10_000.0 # Rp 10.000 / kg
        shrinkage_pct = 0.20 # 20% trimming / evaporation loss

        # Formula: Effective Cost = Base Cost / (1 - Shrinkage%)
        effective_cost = round(base_unit_cost / (1.0 - shrinkage_pct), 2)
        self.assertEqual(effective_cost, 12_500.0)

    def test_portion_hpp_with_packaging_layer(self):
        """Test multi-ingredient portion HPP combined with packaging and disposables layer."""
        # Recipe: Iced Caramel Macchiato 16oz
        ingredients = [
            {"name": "Espresso Blend (18g)", "cost": 3_600.0},
            {"name": "Fresh Milk (150ml)", "cost": 4_500.0},
            {"name": "Caramel Syrup (20ml)", "cost": 1_800.0},
            {"name": "Ice Cubes (120g)", "cost": 300.0},
        ]
        packaging = [
            {"name": "PET Cold Cup 16oz", "cost": 1_200.0},
            {"name": "Dome Lid", "cost": 400.0},
            {"name": "Paper Straw", "cost": 250.0},
            {"name": "Cup Sleeve", "cost": 350.0},
        ]

        total_ingredients_cost = sum(i["cost"] for i in ingredients) # 10,200
        total_packaging_cost = sum(p["cost"] for p in packaging) # 2,200
        total_portion_hpp = total_ingredients_cost + total_packaging_cost

        self.assertEqual(total_ingredients_cost, 10_200.0)
        self.assertEqual(total_packaging_cost, 2_200.0)
        self.assertEqual(total_portion_hpp, 12_400.0)

    def test_gross_profit_margin_and_status(self):
        """Test gross profit margin calculation and health status classification."""
        hpp = 12_400.0
        retail_price = 38_000.0

        gross_profit = retail_price - hpp
        margin_pct = round((gross_profit / retail_price) * 100, 1)

        self.assertEqual(gross_profit, 25_600.0)
        self.assertEqual(margin_pct, 67.4)

        # Status check
        def get_status(m):
            if m >= 65.0:
                return "optimal"
            elif m >= 50.0:
                return "moderate"
            return "low"

        self.assertEqual(get_status(margin_pct), "optimal") # >= 65% is optimal for F&B

    def test_price_simulator_target_margin(self):
        """Test reverse price simulator to achieve target margin."""
        hpp = 12_400.0
        target_margin_pct = 70.0 # 70%

        # Target Price = HPP / (1 - Target Margin %)
        target_price = round(hpp / (1.0 - (target_margin_pct / 100.0)), -2) # Round to nearest 100
        self.assertEqual(target_price, 41_300.0)


if __name__ == "__main__":
    unittest.main()
