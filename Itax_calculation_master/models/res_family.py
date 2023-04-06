from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class FamilyDetails(models.Model):
    _name = 'res.family'

    relationship_family = fields.Selection([('spouse','Spouse'),
                                            ('father','Father'),
                                            ('mother','Mother'),
                                            ('son','Son'),
                                            ('daughter','Daughter')],
                                           string="Relation")
    name_family = fields.Char(string="Name")
    date_of_birth_rel = fields.Date(string="Date Of Birth")
    age_rel = fields.Integer(string="Age")
    gender_rel = fields.Selection([('male','Male'),('female','Female'),('others','Others'),],string="Gender")
    date_of_marriage = fields.Date(string="Date Of Marriage")
    blood_group_rel = fields.Selection([('a+','A+'),('a-','A-'),('b+','B+'),('b-','B-'),('o+','O+'),('o-','O-'),
                                          ('ab+','AB+'),('ab-','AB-'),],string='Blood Group')
    Physically_disabled = fields.Selection([('yes','Yes'),('no','No'),],string="Physically Disabled")
    if_yes = fields.Binary(string="If Yes, pls attach relevant Document")
    employee_details = fields.Many2one('hr.employee',string="Employee Details")