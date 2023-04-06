from odoo import models, fields, _, api


class TaxSection16(models.Model):
    _name = 'tax.section16'

    name = fields.Char("Name")
    limit_amount = fields.Float("Max Amount")
    is_required = fields.Boolean("Mandatory")
