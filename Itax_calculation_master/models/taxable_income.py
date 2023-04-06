from odoo import models, fields, _, api


class TaxableIncome(models.Model):
    _name = 'taxable.income'

    name = fields.Char("Name")
    salary_rule = fields.Many2many("hr.salary.rule", string="Salary Rules")
    is_required = fields.Boolean("Mandatory")
