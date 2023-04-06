from odoo import models, fields, _, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    wage = fields.Monetary('Wage', required=False, tracking=True, help="Employee's monthly gross wage.")