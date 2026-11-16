# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class L10nIdNsfpRange(models.Model):
    _name = 'l10n_id.nsfp.range'
    _description = 'DJP Nomor Seri Faktur Pajak (NSFP) Range Pool'
    _order = 'year desc, start_number asc'

    name = fields.Char(
        string='Reference / SK DJP',
        required=True,
        help='Official approval letter number from DJP (e.g. S-123/WPJ.04/KP.0103/2026)'
    )
    year = fields.Char(
        string='Tax Year',
        size=4,
        required=True,
        default=lambda self: str(fields.Date.today().year)
    )
    prefix = fields.Char(
        string='Prefix Code',
        size=8,
        default='000',
        required=True,
        help='NSFP Prefix approved by DJP (typically 000, 001, etc.)'
    )
    start_number = fields.Integer(
        string='Start Serial (8 Digits)',
        required=True,
        help='Starting 8-digit serial number from DJP e-Nofa allocation.'
    )
    end_number = fields.Integer(
        string='End Serial (8 Digits)',
        required=True,
        help='Ending 8-digit serial number from DJP e-Nofa allocation.'
    )
    current_number = fields.Integer(
        string='Next Serial to Assign',
        required=True,
        help='Current counter pointing to the next available serial number.'
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    notes = fields.Text(string='Notes')

    total_quota = fields.Integer(
        string='Total Quota',
        compute='_compute_quota',
        store=True
    )
    used_quota = fields.Integer(
        string='Used Quota',
        compute='_compute_quota',
        store=True
    )
    remaining_quota = fields.Integer(
        string='Remaining Quota',
        compute='_compute_quota',
        store=True
    )

    @api.depends('start_number', 'end_number', 'current_number')
    def _compute_quota(self):
        for record in self:
            if record.end_number >= record.start_number:
                record.total_quota = record.end_number - record.start_number + 1
            else:
                record.total_quota = 0

            if record.current_number >= record.start_number:
                record.used_quota = record.current_number - record.start_number
            else:
                record.used_quota = 0

            record.remaining_quota = max(record.total_quota - record.used_quota, 0)

    @api.constrains('start_number', 'end_number', 'current_number')
    def _check_numbers(self):
        for record in self:
            if record.end_number < record.start_number:
                raise ValidationError(_("End serial number cannot be less than start serial number."))
            if record.current_number < record.start_number:
                raise ValidationError(_("Current serial cannot be less than start serial number."))

    def allocate_next_nsfp(self):
        self.ensure_one()
        if self.current_number > self.end_number:
            raise UserError(_(
                "NSFP Quota Depleted for range '%(range_name)s' (Year %(year)s)! "
                "Please request and register a new NSFP range from DJP e-Nofa.",
                range_name=self.name,
                year=self.year
            ))

        serial_str = f"{self.current_number:08d}"
        allocated_nsfp = f"{self.prefix}-{self.year[-2:]}.{serial_str}"
        self.current_number += 1
        return allocated_nsfp
