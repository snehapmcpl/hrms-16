from odoo import models, fields, _, api
from odoo.exceptions import UserError


class EmployeeTds(models.Model):
    _name = 'employee.tds'
    _rec_name = 'employee_id'
    _order = 'month'

    employee_id = fields.Many2one("hr.employee", string="Employee Name")
    month = fields.Char("Month")
    income_tax = fields.Float("Income Tax")
    surcharge = fields.Float("Surcharge")
    cess = fields.Float("Cess")
    total_amount = fields.Float("Total")
    date = fields.Date("Date")
    payslip_id = fields.Many2one('hr.payslip', string="Payslip")
    payslip_state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft', compute='compute_payslip_state')
    line_ids = fields.One2many('employee.tds.line', 'tds_id', string="Line Ids")
    computed_line_ids = fields.One2many('employee.computed.line', 'tds_id', string="Computed Line Ids")

    def compute_payslip_state(self):
        for rec in self:
            if rec.payslip_id:
                rec.payslip_state = rec.payslip_id.state
            else:
                rec.payslip_state = 'draft'

    def update_payslip(self):
        if self.env.user.user_has_groups('user_security_groups.group_user_director'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_managers'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.env.user.user_has_groups('user_security_groups.group_user_employee'):
            raise UserError(_('You do not have access rights to run this option!'))
        if self.payslip_id:
            self.payslip_id.update({
                'income_tax': self.income_tax,
                'surcharge': self.surcharge,
                'cess': self.cess,
            })
        else:
            raise UserError(_("You don't Have any Payslip for this time period."))


class EmployeeTdsLines(models.Model):
    _name = 'employee.tds.line'

    tds_id = fields.Many2one('employee.tds', string="TDS Id")
    salary_rule_id = fields.Many2one('hr.salary.rule', string="Rules")
    amount = fields.Float(string="Amount")


class EmployeeComputedLines(models.Model):
    _name = 'employee.computed.line'

    tds_id = fields.Many2one('employee.tds', string="TDS Id")
    name = fields.Char(string="Particulars")
    amount = fields.Float(string="Amount")
