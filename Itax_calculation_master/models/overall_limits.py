from odoo import models, fields, _, api


class MaxOverallLimits(models.Model):
    _name = 'tax.max.limit'

    name = fields.Char("Name")
    active = fields.Boolean("Active", default=True)
    max_limit_for_section_24 = fields.Float("For Section 24")
    max_limit_for_section_10 = fields.Float("For Section 10")
    max_limit_for_section_16 = fields.Float("For Section 16")
    max_limit_for_section_17 = fields.Float("For Section 17")
    max_limit_for_section_80c = fields.Float("For Section 80 C")
    max_limit_for_section_80ccd = fields.Float("For Section 80 CCD")
    max_limit_for_other_incomes = fields.Float("For Other Income Sources")
    max_limit_for_tax_slab = fields.Float("For Tax Slab")
