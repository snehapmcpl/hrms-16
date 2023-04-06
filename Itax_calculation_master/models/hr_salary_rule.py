from odoo import models, fields, _, api


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    is_taxable = fields.Boolean("Is Taxable")
    rule_type = fields.Selection([('fixed', 'Fixed'), ('variable', 'Variable')], string="Rule Type", default="variable")
