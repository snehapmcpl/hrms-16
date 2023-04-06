from odoo import models, fields, _, api


class TaxChapterVI(models.Model):
    _name = 'tax.chapter6'

    name = fields.Char("Name")
    limit_amount = fields.Float("Max Amount")
