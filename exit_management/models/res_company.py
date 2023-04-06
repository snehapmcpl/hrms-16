from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    calculate_gratuity = fields.Boolean('Calculate Gratuity')