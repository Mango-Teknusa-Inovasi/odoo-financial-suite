# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountBudgetCategory(models.Model):
    _name = 'account.budget.category'
    _description = 'Kategori Anggaran Keuangan'
    _order = 'budget_type desc, name asc'

    name = fields.Char(
        string="Nama Kategori Anggaran",
        required=True,
        help="Contoh: Beban Operasional, Biaya Pemasaran, Gaji & Upah, atau Pendapatan Usaha."
    )
    code = fields.Char(
        string="Kode Kategori",
        required=True,
        default="KAT/001"
    )
    budget_type = fields.Selection([
        ('expense', 'Plafon Beban / Biaya (Expense Ceiling)'),
        ('revenue', 'Target Omset / Pendapatan (Revenue Target)')
    ], string="Tipe Anggaran", default='expense', required=True)

    account_ids = fields.Many2many(
        'account.account',
        'account_budget_category_rel',
        'category_id',
        'account_id',
        string="Daftar Akun GL Terkait",
        domain="[('company_id', '=', company_id)]",
        help="Akun-akun buku besar yang transaksi realisasinya dipetakan ke dalam kategori anggaran ini."
    )
    company_id = fields.Many2one(
        'res.company',
        string="Perusahaan",
        required=True,
        default=lambda self: self.env.company
    )
    color = fields.Integer(string="Warna Tag", default=1)
    active = fields.Boolean(string="Aktif", default=True)
