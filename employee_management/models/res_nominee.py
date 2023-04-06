from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class NomineeDetails(models.Model):
    _name = 'res.nominee'

    nominee_name = fields.Char(string="Name")
    relationship_with_nominee = fields.Char(string="Relationship")
    nominee_gender = fields.Selection([('male','Male'),('female','Female'),('others','others'),],string="Gender")
    nominee_dob = fields.Date(string="DOB DD/MM/YY")
    street_nominee = fields.Char(string="Stree")
    street2_nominee = fields.Char(string="Street2")
    pincode_nominee = fields.Char(change_default=True,string="PIN Code")
    city_nominee = fields.Char(string="City")
    state_id_nominee = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id_nominee = fields.Many2one('res.country', string='Country', ondelete='restrict')
    Proportion_to_be_shared = fields.Char(string="Proportion to be shared (%)")
    emp_nominee = fields.Many2one('hr.employee')