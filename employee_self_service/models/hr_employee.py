from odoo import models, fields, _, api
from odoo.tools import email_normalize


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    tds_count = fields.Integer("TDS", compute="compute_tds_count")
    allocation_used_display = fields.Float('Allocation used Display')

    def compute_tds_count(self):
        for rec in self:
            if rec.id:
                rec.tds_count = self.env['employee.tds'].search_count([('employee_id', '=', rec.id)])
            else:
                rec.tds_count = 0

    def action_tds_self_service(self):
        return {
            'name': _('TDS Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'employee.tds',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }

    def action_tax_self_service(self):
        return {
            'name': _('Tax Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'it.returns',
            'view_mode': 'list',
            'views':
                [[self.env.ref('Itax_calculation_master.it_returns_tree_new').id, 'list'],
                 [self.env.ref('Itax_calculation_master.it_returns_form_new').id, 'form']],
            # 'view_id': 'Itax_calculation_master.action_it_returns_new',
            # 'view_id': self.env.ref('Itax_calculation_master.it_returns_tree_new').id,
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }
        # return {
        #     'name': _('Tax Details'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hr.employee.tax',
        #     'view_mode': 'tree,form',
        #     'domain': [('employee_id', '=', self.id)],
        #     'context': {
        #         'employee_id': self.id,
        #     },
        # }

    def action_time_off_dashboard_self_service(self):
        return {
            'name': _('Time Off Dashboard'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave',
            'view_mode': 'calendar',
            'views':
                [[self.env.ref('hr_holidays.hr_leave_view_dashboard').id, 'calendar']],
            # 'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }

    def _create_user(self):
        """ create a new user for wizard_user.partner_id
            :returns record of res.users
        """
        return self.env['res.users'].create(dict(
            name=self.name,
            login=self.work_email,
            company_id=self.env.company.id,
        ))

    def action_create_users(self):
        for records in self:
            # self.ensure_one()
            group_user = records.env.ref('base.group_user')
            user_sudo = records.user_id.sudo()

            if not user_sudo:
                # create a user if necessary and make sure it is in the portal group
                company = records.env.company
                user_sudo = records.sudo().with_company(company.id)._create_user()
                if user_sudo:
                    user_sudo.write({'active': True, 'groups_id': [(4, group_user.id)]})
                    # prepare for the signup process
                    user_sudo.partner_id.signup_prepare()
            for rec in records:
                rec.user_id = user_sudo
                rec.work_email = user_sudo.login
