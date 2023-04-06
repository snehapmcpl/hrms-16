from odoo import models, fields, _, api


class TaxSection24(models.Model):
    _name = 'tax.section24'

    name = fields.Char(string="Name")
    limit_amount = fields.Float("Max Amount")
