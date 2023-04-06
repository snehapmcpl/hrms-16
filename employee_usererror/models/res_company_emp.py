from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date,datetime


class EmployeeHistoryUserError(models.Model):
    _inherit = 'res.company'

    cin_emp = fields.Char(string="CIN")
    uan_emp = fields.Char(string="UAN No")
    startup_emp = fields.Char(string="Startup")
