from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    director_id = fields.Many2one("res.users", string="Authorised Signatory")
