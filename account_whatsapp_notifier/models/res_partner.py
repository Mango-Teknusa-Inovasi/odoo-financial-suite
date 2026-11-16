# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    whatsapp_number = fields.Char(
        string='WhatsApp Number',
        compute='_compute_whatsapp_number',
        store=True,
        readonly=False,
        help='Normalized international WhatsApp number (e.g. 6281234567890).'
    )

    @api.model
    def clean_whatsapp_number(self, phone):
        """
        Clean and normalize raw phone strings to standard international format without plus prefix.
        Handles Indonesian mobile numbers (08xxx -> 628xxx) and international numbers.
        """
        if not phone:
            return False
        clean = re.sub(r'\D', '', str(phone))
        if clean.startswith('08'):
            clean = '628' + clean[2:]
        elif clean.startswith('8'):
            clean = '628' + clean[1:]
        elif clean.startswith('6208'):
            clean = '628' + clean[4:]
        return clean if len(clean) >= 10 else False

    @api.depends('mobile', 'phone')
    def _compute_whatsapp_number(self):
        for partner in self:
            raw = partner.mobile or partner.phone
            partner.whatsapp_number = self.clean_whatsapp_number(raw) or raw or False
