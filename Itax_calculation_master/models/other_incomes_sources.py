from odoo import models, fields, _, api


class OtherIncomeSources(models.Model):
    _name = 'other.income.sources'

    name = fields.Char("Name")
    # amount = fields.Float("Amount")
