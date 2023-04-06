from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class HrmsInherit(models.Model):
    _inherit = 'hr.employee'

    identification_id = fields.Char(string='Identification No', required='True',
                                    groups="hr.group_hr_user,user_access.group_self_service_employee", tracking=True)
    esi_number = fields.Char(string = "ESI Number")

    @api.onchange('identification_id')
    def identification_id_validation(self):
        if self.identification_id:
            error = self.env['hr.employee'].search([('identification_id', '=', self.identification_id)])
            if error:
                raise UserError("This Employee No. already exists....!!")


class HrmsNotification(models.Model):
    _inherit = "res.users"

    notification_type = fields.Selection([
        ('email', 'Handle by Emails'),
        ('inbox', 'Handle in Product')],
        'Notification', required=True, default='email',
        help="Policy on how to handle Chatter notifications:\n"
             "- Handle by Emails: notifications are sent to your email address\n"
             "- Handle in Product: notifications appear in your Product Inbox")


class ContractArch(models.Model):
    _inherit = "hr.contract.history"

    active = fields.Boolean(string="Active", default=True)


class ContractInvDup(models.Model):
    _inherit = 'hr.contract'

    @api.onchange("type_id")
    def onchange_type_id_22(self):
        for rec in self:
            if rec.type_id:
                self.contract_type_id = self.type_id
                print("..........................................................................................", self.contract_type_id)


class PayslipChange(models.Model):
    _inherit = "hr.employee"

    uan_number = fields.Char("Uan number")

    def action_offer_employee_view(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return self.env.ref('recruitment_management.report_offer_letter_menu').report_action(self.id)

        # offer = self.env['hr.applicant']
        # return offer.env.ref('recruitment_management.report_offer_letter_menu').report_action(self)

        #     {
        #         'name': 'offer',
        #         'view_type': 'form',
        #         'res_model': 'hr.applicant',
        #         'view_mode': 'form',
        #         'type': 'ir.actions.act_window'
        #     }
        # )




        # return self.env.ref('recruitment_management.report_offer_letter_menu').report_action(self)
        # html = self.env['report'].get_html(self, 'recruitment_management.report_offer_letter_menu')
        # self.write({'preview': html})
        # return True
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

