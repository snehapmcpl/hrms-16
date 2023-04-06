from odoo import models, fields, _, api


class TaxSlab(models.Model):
    _name = 'tax.slab'
    _rec_name = 'slab_name'

    name = fields.Char(string="Name")
    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")
    line_ids = fields.One2many('tax.slab.line', 'tax_slab_id', string="Slab Lines")
    surcharge_ids = fields.One2many('tax.slab.surcharge', 'tax_slab_id', string="Surcharge")
    cess_ids = fields.One2many('tax.slab.cess', 'tax_slab_id', string="Cess")
    section87a_ids = fields.One2many('tax.slab.section87a', 'tax_slab_id', string="Section 87 A")
    age_group = fields.Selection([('less_60', 'Less Than 60 Years Old'),
                                  ('60_80', '60-80 Years'),
                                  ('more_than_80', 'Above 80 Years')], default='less_60')
    slab_name = fields.Char("Slab Name", compute="compute_slab_name")

    def compute_slab_name(self):
        for rec in self:
            if rec.age_group:
                if rec.age_group == 'more_than_80':
                    rec.slab_name = rec.name + ' ( Above 80 Years )'
                elif rec.age_group == '60_80':
                    rec.slab_name = rec.name + ' ( 60-80 Years )'
                else:
                    rec.slab_name = rec.name + ' ( Less Than 60 Years Old )'
            else:
                rec.slab_name = rec.name


class TaxSlabLine(models.Model):
    _name = 'tax.slab.line'

    tax_slab_id = fields.Many2one('tax.slab', string="Tax Slab")
    lower_limit = fields.Float("From")
    higher_limit = fields.Float("To")
    tax_per = fields.Float("Tax (%)")


class TaxSlabSurcharge(models.Model):
    _name = 'tax.slab.surcharge'

    tax_slab_id = fields.Many2one('tax.slab', string="Tax Slab")
    lower_limit = fields.Float("From")
    higher_limit = fields.Float("To")
    tax_per = fields.Float("Surcharge (%)")


class TaxSlabCess(models.Model):
    _name = 'tax.slab.cess'

    tax_slab_id = fields.Many2one('tax.slab', string="Tax Slab")
    lower_limit = fields.Float("From")
    higher_limit = fields.Float("To")
    tax_per = fields.Float("Cess (%)")


class TaxSlabSection87a(models.Model):
    _name = 'tax.slab.section87a'

    tax_slab_id = fields.Many2one('tax.slab', string="Tax Slab")
    lower_limit = fields.Float("From")
    higher_limit = fields.Float("To")
    tax_amount = fields.Float("Tax Rebate Amount")
