from odoo import models, fields, api, _


class NoticePeriodDays(models.Model):
    _name = 'notice.period.days'
    _inherit = 'mail.thread'
    _rec_name = 'employee_category'

    employee_category = fields.Selection([
         ('confirmed', 'Confirmed'),
         ('in_provisional_period', 'Probation'),
         ('trainee', 'Trainee')],
        string='Employee Category', default='probation')
    ctc_from = fields.Float('CTC From')
    ctc_to = fields.Float('CTC To')
    employee_notice_days = fields.Integer(string="Employee Notice Period (days)")
    company_notice_days = fields.Integer(string="Comapany Notice Period (days)")


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_encashable = fields.Boolean('Allow For Leave Encashment')
