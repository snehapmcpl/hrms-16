from odoo import models,fields


class Empdetails(models.Model):
    _inherit = 'hr.employee'


    height = fields.Float(string='Height')
    weight = fields.Float(string='Weight')
    eye_sight = fields.Text(string='Eye Sight')
    identification_mark = fields.Text(string="Identification Marks")
