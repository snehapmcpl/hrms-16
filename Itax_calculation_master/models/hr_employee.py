from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
import re


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    tax_regim_type = fields.Many2one('tax.slab', string="Tax Regime")
    employee_pan_no = fields.Char("PAN No.")
    age = fields.Integer("Age", compute="calculate_age")

    rental_line_ids = fields.One2many('employee.rental.lines', 'employee_id', string="Lines")
    city_type_conf = fields.Many2one('city.type.conf', string="City Conf")
    rent_paid = fields.Float("Rent Paid Per Month")
    total_ctc = fields.Float("Annual CTC")
    mbo = fields.Float("Variable Pay")
    relieving_date = fields.Date('Date Of Relieving')

    rental_line_counts = fields.Integer("Count", compute="compute_lines")

    # private info

    father_name = fields.Char(string="Father Name")
    mother_name = fields.Char(string="Mother Name")
    dob = fields.Date(string="Father Date Of Birth")
    date_of = fields.Date(string="Mother Date Of Birth")
    div_place = fields.Char(string="Place Of Issue")
    date_issue_div = fields.Date(string="Date Of Issue")
    valid_div = fields.Date(string="Expiry Date")
    pass_place = fields.Char(string="Place Of Issue")
    date_issue_pass = fields.Date(string="Date Of Issue")
    passport_number = fields.Char(string="Number")
    valid_pass = fields.Date(string="Expiry Date")
    driving_licence_num = fields.Char(string="Number")
    pan_card_number = fields.Char(string="PAN Card Number")
    aadhar_number = fields.Char(string="AADHAR Number")
    uan_number = fields.Char(string="UAN Number")
    age_of = fields.Integer(string="Age")
    blood_group = fields.Char(string="Blood Group")
    physically_disabled = fields.Selection([('yes','Yes'),('no','No'),],string="Physically Disabled", help="If yes,please attach relevant document")
    know_two = fields.Text(string="How do you know him/her")
    total_experience = fields.Char(string="Total Experience")
    street_emp = fields.Char()
    street2_emp = fields.Char()
    zip_emp = fields.Char(change_default=True)
    city_emp = fields.Char()
    state_id_emp = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id_emp = fields.Many2one('res.country', string='Country', ondelete='restrict')
    name_emergency = fields.Char(string="Name")
    phone_emergency = fields.Char(string="Phone")
    email_emergency = fields.Char(string="Email ID")
    son_dot_of = fields.Char()
    son_dot_of2 = fields.Char()
    street_emergency = fields.Char()
    street2_emergency = fields.Char()
    zip_emergency = fields.Char(change_default=True)
    city_emergency = fields.Char()
    state_emergency = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id_emergency = fields.Many2one('res.country', string='Country', ondelete='restrict')
    name_ref = fields.Char(string="Reference-1 Name")
    designation_ref = fields.Char(string="Designation")
    know_ref = fields.Char(string="How do you know him/her")
    phone_ref = fields.Char(string="Reference-1 Phone")
    name_ref_two = fields.Char(string="Reference-2 Name")
    designation_ref_two = fields.Char(string="Designation")
    know_ref_two = fields.Char(string="How do you know him/her")
    phone_ref_two = fields.Char(string="Reference-2 Phone")
    family_details = fields.One2many('res.family','employee_details')
    background_emp = fields.One2many('res.background','employee_background')
    nominee_details = fields.One2many('res.nominee','emp_nominee')
    emp_history = fields.One2many('rec.history','emp_history')
    street_permanent = fields.Char(string="Stree")
    street2_permanent = fields.Char(string="Street2")
    pincode_permanent = fields.Char(change_default=True, string="PIN Code")
    city_permanent = fields.Char(string="City")
    state_id_permanent = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id_permanent = fields.Many2one('res.country', string='Country', ondelete='restrict')
    total_exp = fields.Char(string="Total Experience")
    father_name_emp = fields.Char(string="Father Name")
    mother_name_emp = fields.Char(string="Mother Name")
    spouse_name_emp = fields.Char(string="Spouse Name")
    father_dob = fields.Date()
    mother_dob = fields.Date()
    spouse_dob = fields.Date()
    lan_emp = fields.One2many('res.language', 'employee_language')
    date_join = fields.Date(string="Date Of Joining", compute='_compute_date_join')
    resume_emp = fields.Binary(string="Resume")
    emp_category = fields.Selection([('confirmed', 'Confirmed'),
                                     ('in_provisional_period', 'Probation'),
                                     ('internship', 'Internship'),
                                     ('contract', 'Contract')], string="Employee Category", default="in_provisional_period")
    date_conformation = fields.Date(string="Date Confirmation", default=datetime.today())
    conformation_ref = fields.Char(string="Confirmation letter Ref")
    net_amount = fields.Float(string="Net Amount")
    phone = fields.Char(related=False, related_sudo=False, readonly=False, string="Private Phone",
                        groups="hr.group_hr_user")
    private_email = fields.Char(related=False, string="Private Email", groups="hr.group_hr_user")
    blood_group_rel = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('o+', 'O+'), ('o-', 'O-'), ('ab+', 'AB+'),
         ('ab-', 'AB-'), ], string='Blood Group')

    employee_type = fields.Selection([
        ('employee', 'Employee'),
        ('student', 'Student'),
        ('trainee', 'Trainee'),
        ('contractor', 'Contract'),
        ('freelance', 'Retainership'),
    ], string='Employee Type', default='employee', required=True,
        help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")

    self_record = fields.Boolean("Self Record")

    @api.depends('contract_ids.state', 'contract_ids.date_start')
    def _compute_date_join(self):
        for employee in self:
            contracts = employee._get_first_contracts()
            if contracts:
                employee.date_join = min(contracts.mapped('date_start'))
            else:
                employee.date_join = False

    @api.onchange('rental_line_ids')
    def compute_lines(self):
        self.rental_line_counts = len(self.rental_line_ids)

    @api.onchange('employee_pan_no')
    def is_valid(self):
        result = re.compile("[A-Z]{5}\d{4}[A-Z]{1}")
        if self.employee_pan_no:
            if result.match(self.employee_pan_no):
                pass
            else:
                raise UserError(_("Invalid PAN No...!!"))

    @api.onchange("birthday")
    def calculate_age(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            self.age = age
        else:
            self.age = False

    def create_lines(self):
        data_list, data = [], {}
        # current_month = datetime.now().month
        current_year = datetime.now().year
        for rec in range(4, 13):
            next_month = datetime(current_year, rec, 1)
            month_first_day = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0).date()
            month_last_day = self.last_day_of_month(month_first_day)
            data = (0, 0, {
                'date_from': month_first_day,
                'date_to': month_last_day,
                'rent_paid': self.rent_paid,
                'city_type_conf': self.city_type_conf.id,
            })
            data_list.append(data)

        for rec in range(3):
            next_month = datetime(current_year + 1, rec + 1, 1)
            month_first_day = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0).date()
            month_last_day = self.last_day_of_month(month_first_day)
            data = (0, 0, {
                'date_from': month_first_day,
                'date_to': month_last_day,
                'rent_paid': self.rent_paid,
                'city_type_conf': self.city_type_conf.id,
            })
            data_list.append(data)
        self.update({
            'rental_line_ids': data_list,
        })

    def update_lines(self):
        data_list = self.env['employee.rental.lines'].search([('date_from', '>', datetime.now()),
                                                              ('employee_id', '=', self.id)])
        for data in data_list:
            data.update({
                'rent_paid': self.rent_paid,
                'city_type_conf': self.city_type_conf.id,
            })

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + timedelta(days=4)
        return next_month - timedelta(days=next_month.day)


class EmployeeRentalLines(models.Model):
    _name = 'employee.rental.lines'

    date_from = fields.Date("From")
    date_to = fields.Date("To")
    rent_paid = fields.Float("Rent Amount")
    city_type_conf = fields.Many2one('city.type.conf', string="City Conf")
    employee_id = fields.Many2one('hr.employee', string="Employee")
