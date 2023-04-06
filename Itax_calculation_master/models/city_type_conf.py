from odoo import models, fields, _, api


class CityTypeConf(models.Model):
    _name = 'city.type.conf'

    name = fields.Char("Name")
    percent = fields.Float("Percent")
