from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date,datetime


class EmployeeHistory(models.Model):
    _name = 'rec.history'

    employee_name = fields.Char(string="Name Of The Employer")
    street_employer = fields.Char(string="Stree")
    street2_employer = fields.Char(string="Street2")
    pincode_employer = fields.Char(change_default=True,string="PIN Code")
    city_employer = fields.Char(string="City")
    state_id_employer = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id_employer = fields.Many2one('res.country', string='Country', ondelete='restrict')
    telephone_no = fields.Char(string="Telephone No")
    designation = fields.Char(string="Designation(Available on payslip)")
    salary_code = fields.Char(string="Employee/Salary Code")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    manager_name = fields.Char(string="Manager's name")
    hr_contact = fields.Char(string="HR Contact No")
    hr_email = fields.Char(string="HR office E-mail ID")
    reason = fields.Text(string="Reason For Leaving")
    first_salary = fields.Char(string="First Salary Drawn (Annual CTC)")
    last_salary = fields.Char(string="Last Salary Drawn (Annual CTC)")
    selection_position = fields.Selection([('Permanent','Permanent'),('Temporary','Temporary'),('Contractua','Contractual'),],string="Employee Position")
    con_emp = fields.Text(string="Agency Details(case of contractual employment)")
    emp_history = fields.Many2one('hr.employee')
    department_his = fields.Char(string="Department")



