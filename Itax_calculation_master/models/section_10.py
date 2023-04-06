from odoo import models, fields, _, api


class TaxSection10(models.Model):
    _name = 'tax.section10'

    name = fields.Char("Name")
    limit_amount = fields.Float("Max Amount")
    is_required = fields.Boolean("Mandatory")
