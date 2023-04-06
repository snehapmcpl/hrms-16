from odoo import api, fields, models, _
from datetime import date, datetime
from odoo.exceptions import UserError


class EmployeeDetailsFields(models.Model):
    _inherit = 'hr.employee'

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
    name_ref = fields.Char(string="Name")
    designation_ref = fields.Char(string="Designation")
    know_ref = fields.Char(string="How do you know him/her")
    phone_ref = fields.Char(string="Phone")
    name_ref_two = fields.Char(string="Name")
    designation_ref_two = fields.Char(string="Designation")
    know_ref_two = fields.Char(string="How do you know him/her")
    phone_ref_two = fields.Char(string="Phone")
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
    lan_emp = fields.One2many('res.language','employee_language')
    date_join = fields.Date(string="Date Of Joining")
    resume_emp = fields.Binary(string="Resume")
    emp_category = fields.Selection([('confirmed', 'Confirmed'),
                                     ('in_provisional_period', 'Probation'),
                                     ('internship', 'Internship'),
                                     ('contract', 'Contract')],
                                         string="Employee Category", default="in_provisional_period")
    date_conformation = fields.Date(string="Date Confirmation", default=datetime.today())
    conformation_ref = fields.Char(string="Confirmation letter Ref")
    net_amount = fields.Float(string="Net Amount")
    phone = fields.Char(related=False, related_sudo=False, readonly=False, string="Private Phone",
                        groups="hr.group_hr_user")
    private_email = fields.Char(related=False, string="Private Email", groups="hr.group_hr_user")

    employee_type = fields.Selection([
        ('employee', 'Employee'),
        ('student', 'Student'),
        ('trainee', 'Trainee'),
        ('contractor', 'Contract'),
        ('freelance', 'Retainership'),
    ], string='Employee Type', default='employee', required=True,
        help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")

    self_record = fields.Boolean("Self Record", compute="compute_self_record")

    def compute_self_record(self):
        for rec in self:
            if rec.user_id:
                if rec.user_id == rec.env.user:
                    rec.self_record = True
                else:
                    rec.self_record = False
            else:
                rec.self_record = False

    # def write(self, vals):
    #     # self.compute_self_record()
    #     if not self.self_record:
    #         raise UserError(_('You are not allowed to edit the record..!!!'))
    #     else:
    #         return super().write(vals)
