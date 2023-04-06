import datetime
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.tools.float_utils import float_round
from odoo.exceptions import UserError, ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    current_leave_id = fields.Many2one('hr.leave.type', compute='_compute_current_leave',
                                       string="Current Time Off Type",
                                       groups="hr.group_hr_user,user_access.group_self_service_employee")

    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.",
                          groups="hr.group_hr_user,user_access.group_self_service_employee",
                          copy=False)

    first_contract_date = fields.Date(compute='_compute_first_contract_date',
                                      groups="hr.group_hr_user,user_access.group_self_service_employee",
                                      store=True)
    address_home_id = fields.Many2one(
        'res.partner', 'Address',
        help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    birthday = fields.Date('Date of Birth',
                           groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    identification_id = fields.Char(string='Identification No',
                                    groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    bank_account_id = fields.Many2one(
        'res.partner.bank', 'Bank Account Number',
        domain="[('partner_id', '=', address_home_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        groups="hr.group_hr_user,user_access.group_self_service_employee",
        tracking=True,
        help='Employee bank salary account')

    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user,user_access.group_self_service_employee",
        default='single', tracking=True)

    private_email = fields.Char(related='address_home_id.email', string="Private Email",
                                groups="hr.group_hr_user,user_access.group_self_service_employee")

    phone = fields.Char(related='address_home_id.phone', related_sudo=False, readonly=False, string="Private Phone",
                        groups="hr.group_hr_user,user_access.group_self_service_employee")

    lang = fields.Selection(related='address_home_id.lang', string="Lang",
                            groups="hr.group_hr_user,user_access.group_self_service_employee",
                            readonly=False)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)

    km_home_work = fields.Integer(string="Home-Work Distance",
                                  groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="hr.group_hr_user,user_access.group_self_service_employee",
        tracking=True)

    passport_id = fields.Char(string="Passport No", groups="hr.group_hr_user,user_access.group_self_service_employee",
                              tracking=True)

    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user,user_access.group_self_service_employee",
                           tracking=True)

    place_of_birth = fields.Char('Place of Birth', groups="hr.group_hr_user,user_access.group_self_service_employee",
                                 tracking=True)

    country_of_birth = fields.Many2one('res.country', string="Country of Birth",
                                       groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)

    certificate = fields.Selection([
        ('graduate', 'Graduate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctor', 'Doctor'),
        ('other', 'Other'),
    ], 'Certificate Level', default='other', groups="hr.group_hr_user,user_access.group_self_service_employee",
        tracking=True)

    study_field = fields.Char("Field of Study", groups="hr.group_hr_user,user_access.group_self_service_employee",
                              tracking=True)

    study_school = fields.Char("School", groups="hr.group_hr_user,user_access.group_self_service_employee",
                               tracking=True)
    emergency_contact = fields.Char("Emergency Contact",
                                    groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    emergency_phone = fields.Char("Emergency Phone", groups="hr.group_hr_user,user_access.group_self_service_employee",
                                  tracking=True)

    visa_no = fields.Char('Visa No', groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    permit_no = fields.Char('Work Permit No', groups="hr.group_hr_user,user_access.group_self_service_employee",
                            tracking=True)
    visa_expire = fields.Date('Visa Expire Date', groups="hr.group_hr_user,user_access.group_self_service_employee",
                              tracking=True)
    work_permit_expiration_date = fields.Date('Work Permit Expiration Date',
                                              groups="hr.group_hr_user,user_access.group_self_service_employee",
                                              tracking=True)
    has_work_permit = fields.Binary(string="Work Permit",
                                    groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)

    spouse_complete_name = fields.Char(string="Spouse Complete Name",
                                       groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    spouse_birthdate = fields.Date(string="Spouse Birthdate",
                                   groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)

    children = fields.Integer(string='Number of Children',
                              groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrPayslip, self).create(vals_list)
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        return res

    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        return res

    def unlink(self):
        res = super(HrPayslip, self).unlink()
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        return res
