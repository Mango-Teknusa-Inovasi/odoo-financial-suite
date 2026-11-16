# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    stamp_enabled = fields.Boolean(
        string='Enable PDF Company Seal & Signature Overlay',
        default=True,
        help='When active, company seal and digital signature will be dynamically rendered on invoice reports.'
    )
    company_seal = fields.Binary(
        string='Official Company Seal (PNG with Transparency)',
        help='Upload a high-resolution transparent PNG image of the official company stamp.'
    )
    authorized_signature = fields.Binary(
        string='Authorized Digital Signature (PNG)',
        help='Upload a clean transparent PNG scan of the authorized signatory.'
    )
    signer_name = fields.Char(
        string='Authorized Signer Name',
        default='Direktur Utama',
        help='Name of the authorized executive printed under the signature block.'
    )
    signer_title = fields.Char(
        string='Signer Official Title / Designation',
        default='Director of Finance',
        help='Executive designation (e.g. Finance Director, Managing Director).'
    )
    stamp_signature_position = fields.Selection([
        ('bottom_right', 'Bottom Right (Standard Commercial Invoice)'),
        ('bottom_left', 'Bottom Left'),
    ], string='Seal & Signature Position', default='bottom_right', required=True)
