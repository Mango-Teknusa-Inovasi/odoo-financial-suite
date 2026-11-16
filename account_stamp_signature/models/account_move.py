# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    emeterai_required = fields.Boolean(
        string='Bea Meterai Required (UU No. 10/2020)',
        compute='_compute_emeterai_required',
        store=True,
        help="Statutory requirement: Invoices with total amount >= Rp 5,000,000 require statutory stamp duty (Bea Meterai)."
    )
    emeterai_status = fields.Selection([
        ('not_required', 'Not Required (< Rp 5,000,000)'),
        ('pending', 'Pending Stamping'),
        ('stamped', 'Officially Stamped (Peruri)'),
        ('failed', 'Stamping Failed'),
    ], string='e-Meterai Status', default='not_required', tracking=True, copy=False)

    emeterai_provider_id = fields.Many2one(
        'emeterai.provider',
        string='e-Meterai Gateway Provider',
        domain="[('company_id', '=', company_id)]",
        help="Select the e-Meterai gateway connector (Mock Sandbox, PDS, Mekari Sign, or PrivyID)."
    )
    emeterai_serial_number = fields.Char(
        string='Peruri Serial Number (SN)',
        readonly=True,
        copy=False,
        help="22-digit official Peruri electronic stamp serial number."
    )
    emeterai_qr_code = fields.Char(
        string='Peruri Verification URL',
        readonly=True,
        copy=False,
        help="Public URL for digital certificate verification on the official Peruri portal."
    )
    emeterai_stamped_date = fields.Datetime(
        string='Stamped At',
        readonly=True,
        copy=False
    )
    emeterai_stamped_pdf = fields.Binary(
        string='Stamped PDF Document',
        readonly=True,
        copy=False,
        help="Archived copy of the invoice PDF carrying the embedded Peruri digital certificate."
    )

    @api.depends('amount_total', 'move_type')
    def _compute_emeterai_required(self):
        for move in self:
            if move.move_type in ('out_invoice', 'in_invoice') and move.amount_total >= 5000000.0:
                move.emeterai_required = True
                if move.emeterai_status == 'not_required':
                    move.emeterai_status = 'pending'
            else:
                move.emeterai_required = False
                if move.emeterai_status == 'pending':
                    move.emeterai_status = 'not_required'

    def action_stamp_emeterai(self):
        """Invoke e-Meterai Gateway Provider to affix official Peruri stamp."""
        self.ensure_one()
        if self.state != 'posted':
            raise UserError(_("Only confirmed / posted invoices can be affixed with an official e-Meterai."))

        provider = self.emeterai_provider_id
        if not provider:
            # Default to the first active provider for the company
            provider = self.env['emeterai.provider'].search([
                ('company_id', '=', self.company_id.id),
                ('active', '=', True)
            ], limit=1)
            if not provider:
                raise UserError(_(
                    "No active e-Meterai Gateway Provider found for company %s.\n"
                    "Please configure a provider in Accounting > Configuration > e-Meterai Providers."
                ) % self.company_id.name)
            self.emeterai_provider_id = provider

        try:
            result = provider.stamp_invoice(self)
            if result.get('success'):
                self.write({
                    'emeterai_serial_number': result.get('serial_number'),
                    'emeterai_qr_code': result.get('qr_code'),
                    'emeterai_stamped_date': result.get('stamped_date') or fields.Datetime.now(),
                    'emeterai_status': 'stamped',
                })

                # Post chatter message
                body = _(
                    "<strong>Official e-Meterai Successfully Affixed</strong><br/>"
                    "• Provider: %s (%s)<br/>"
                    "• Peruri Serial Number: <code>%s</code><br/>"
                    "• Statutory Status: <em>UU No. 10/2020 Compliant (Rp 10.000 Duty Paid)</em><br/>"
                    "• Verification: <a href='%s' target='_blank'>Verify on Peruri Gateway</a>"
                ) % (
                    provider.name,
                    dict(provider._fields['provider_type'].selection).get(provider.provider_type),
                    self.emeterai_serial_number,
                    self.emeterai_qr_code
                )
                self.message_post(body=body, message_type='notification')

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('e-Meterai Stamped Successfully'),
                        'message': _('Invoice %s is now officially stamped with Peruri SN %s.') % (self.name, self.emeterai_serial_number),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                self.emeterai_status = 'failed'
                raise UserError(result.get('error', _("Unknown e-Meterai stamping failure.")))

        except Exception as e:
            self.emeterai_status = 'failed'
            _logger.exception("Failed to stamp invoice %s with e-Meterai: %s", self.name, str(e))
            raise UserError(_("e-Meterai Stamping Error: %s") % str(e))

    def action_reset_emeterai(self):
        """Allow resetting e-meterai status for draft / test environments."""
        for move in self:
            move.write({
                'emeterai_status': 'pending' if move.emeterai_required else 'not_required',
                'emeterai_serial_number': False,
                'emeterai_qr_code': False,
                'emeterai_stamped_date': False,
            })
            move.message_post(body=_("e-Meterai stamp has been reset."), message_type='notification')
