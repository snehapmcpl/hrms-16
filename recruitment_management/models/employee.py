from odoo import api, fields, models, _
from num2words import num2words


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    recruitment_id = fields.Many2one('hr.applicant', string="Recruitment Id", compute="_get_recruitment_id")
    appointment_reference = fields.Char(string="Reference")
    appointment_date = fields.Date(string="Date")
    title = fields.Selection([('mr', 'Mr'),
                              ('ms', 'Ms'),
                              ('mrs', 'Mrs'),
                              ('dr', 'Dr')], default="mr", string="Title")

    def generate_appointment_letter(self):
        # print("&&&**&*&&&*&**&&&&", self)
        return self.env.ref('recruitment_management.report_appointment_letter_menu').report_action(self)

    def _get_recruitment_id(self):
        rec = self.env["hr.applicant"].search([('emp_id', '=', self.id)])
        if rec:
            self.recruitment_id = rec.id
        else:
            self.recruitment_id = False

    def amount_in_words(self, number):
        return num2words(number, lang='en_IN').title()

    def get_partner_first_name(self):
        if self.name:
            result = self.name.split(" ")
            return result[0]

    def get_title(self):
        if self.title == 'mr':
            return "Mr."
        if self.title == 'ms':
            return "Ms."
        if self.title == 'mrs':
            return "Mrs."
        if self.title == 'dr':
            return "Dr."
        else:
            return False
