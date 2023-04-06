from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from num2words import num2words
from datetime import date,  datetime
from dateutil.relativedelta import relativedelta
import re


class EmployeeDetailsUserError(models.Model):
    _inherit = 'hr.employee'

    grade_emp = fields.Char(string="Band / Grade")
    country_id = fields.Many2one('res.country', 'Nationality (Country)',
                                 groups="hr.group_hr_user", tracking=True,
                                 default=lambda self: self.env.company.country_id.id)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth",
                                       groups="hr.group_hr_user", tracking=True,
                                       default=lambda self: self.env.company.country_id.id)


    # _sql_constraints = [('unique_pan_card_number', 'unique(pan_card_number,aadhar_number)', 'This PAN is already exists.'),]

    @api.onchange('date_join')
    def change_date(self):
        current = date.today()
        if self.date_join:
            if self.date_join > current:
                raise UserError("Joining Date Must be lesser Than Current Date..!!")

    @api.onchange('birthday')
    def birthday_date_validation(self):
        current = date.today()
        if self.birthday:
            age = current.year - self.birthday.year - ((current.month, current.day) < (self.birthday.month, self.birthday.day))
            if self.birthday >= current:
                raise UserError("Date Of Birth Must be lesser Than Current Date..!!")
            if age <= 18:
                raise UserError("Employee age should be greater than 18 years..!!")

    @api.onchange('valid_pass')
    def passport_date_validation(self):
        if self.valid_pass and self.date_issue_pass:
            if self.valid_pass < self.date_issue_pass:
                raise UserError("Passport Issue Date Must be lesser Than Expiry Date..!!")

    @api.onchange('valid_div')
    def driving_license_date_validation(self):
        if self.valid_div and self.date_issue_div:
            if self.valid_div < self.date_issue_div:
                raise UserError("Driving License Issue Date Must be lesser Than Expiry Date..!!")

    @api.onchange('pan_card_number')
    def pan_number_validation(self):
        if self.pan_card_number:
            result = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")
            flag = ""
            error = self.env['hr.employee'].search_count([('pan_card_number', '=', self.pan_card_number)])
            if error:
                raise UserError("This PAN is already exists....!!")

            if len(self.pan_card_number) != 10:
                flag +="The given PAN Number contains "+ str(len(self.pan_card_number))+" characters it should be 10 characters"
            elif self.pan_card_number[0:5].isupper() is False:
                flag += "The first five characters should be any upper case alphabets"
            elif self.pan_card_number[5:9].isdigit() is False:
                flag += "The next four-characters should be any number from 0 to 9s"
            elif self.pan_card_number[9:10].isupper() is False:
                flag += "The last(tenth) character should be any upper case alphabet"
            elif not result.match(self.pan_card_number):
                raise UserError("PAN number is not valid ")
            if flag != "":
                raise UserError("PAN number is not valid")

    @api.onchange('aadhar_number')
    def aadhar_number_validation(self):
        if self.aadhar_number:
            error = self.env['hr.employee'].search_count([('aadhar_number', '=', self.aadhar_number)])
            flag = ""
            if error:
                raise UserError("This AADHAR Card Number already exists...!!")

            if len(self.aadhar_number) != 12:
                flag +="The given AADHAR Number contains "+ str(len(self.aadhar_number)) +" characters it should be 12 characters."
            elif re.findall("[0-1]", self.aadhar_number[0]):
                flag +="Aadhar card number cannot start with 0 or 1"
            elif re.findall("[a-zA-Z]", self.aadhar_number):
                flag +="Aadhar number should not contain alphabets"
            if flag != "":
                raise UserError("AADHAR number is not valid ...!!")

    @api.onchange('uan_number')
    def uan_number_validation(self):
        if self.uan_number:
            error = self.env['hr.employee'].search_count([('uan_number', '=', self.uan_number)])
            if error:
                raise UserError("This  UAN Number already exists...!!")

    @api.onchange('employee_pan_no')
    def employee_pan_no_validation(self):
        if self.employee_pan_no:
            result = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")
            flag = ""
            error = self.env['hr.employee'].search_count([('employee_pan_no', '=', self.employee_pan_no)])
            if error:
                raise UserError("This PAN is already exists....!!")

            if len(self.employee_pan_no) != 10:
                flag += "The given PAN Number contains " + str(
                    len(self.employee_pan_no)) + " characters it should be 10 characters"
            elif self.employee_pan_no[0:5].isupper() is False:
                flag += "The first five characters should be any upper case alphabets"
            elif self.employee_pan_no[5:9].isdigit() is False:
                flag += "The next four-characters should be any number from 0 to 9s"
            elif self.employee_pan_no[9:10].isupper() is False:
                flag += "The last(tenth) character should be any upper case alphabet"
            elif not result.match(self.employee_pan_no):
                raise UserError("PAN number is not valid ")
            if flag != "":
                raise UserError("PAN number is not valid")
