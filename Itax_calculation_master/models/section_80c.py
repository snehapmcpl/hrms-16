from odoo import models, fields, _, api


class TaxSection80c(models.Model):
    _name = 'tax.section80c'

    name = fields.Char("Name")
    # amount = fields.Float("Amount")
    limit_amount = fields.Float("Max Amount")
