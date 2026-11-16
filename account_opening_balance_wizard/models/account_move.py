# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_opening_balance = fields.Boolean(
        string='Opening Balance Document',
        default=False,
        readonly=True,
        copy=False,
        help='Indicates whether this journal entry, customer invoice, or vendor bill originates from the Opening Balance Wizard.'
    )
