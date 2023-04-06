from odoo import api, fields, models, _
from odoo.exceptions import UserError



class Applicant(models.Model):
    _inherit = 'hr.applicant'

    # @api.model
    # def create(self, vals):
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code('hr.applicant') or _('New')
    #     result = super(Applicant, self).create(vals)
    #     return result

    reference = fields.Char("Reference", readonly=True)
    title = fields.Selection([('mr', 'Mr'),
                              ('ms', 'Ms'),
                              ('mrs', 'Mrs'),
                              ('dr', 'Dr')], default="mr", string="Title")
    no_of_rounds = fields.Integer(string="No Of Rounds", default=1)
    # evaluation = fields.Many2one('recruitment.review', "Evaluation")
    #approval_id = fields.Many2one('approval.request', "Approval")
    location = fields.Char("Location")
    probationary_period = fields.Integer("Probationary Period")
    salary_breakup_id = fields.Many2one('employee.salary.breakup', string="Salary Breakup")
    offer_letter_validity = fields.Date(string="Offer letter Valid Till")
    # interview_stage = fields.Selection([('yes', 'Yes'), ('no', 'No')], sting='Stage')
    # # interview_stage = fields.Many2one('hr.recruitment.stage', readonly=True, string='stage', copy=False, states={'draft': [('readonly', False)]})
    interview_stage = fields.Char(related='stage_id.name', string='stage')


    review_1 = fields.One2many('review.line', 'applicant_id', string='Remarks Of the Interviewer 1...')
    review_2 = fields.One2many('review.line2', 'applicant_id2', string='Remarks Of the Interviewer 2...')
    review_3 = fields.One2many('review.line3', 'applicant_id3', string='Remarks Of the Interviewer 3...')
    review_4 = fields.One2many('review.line4', 'applicant_id4', string='Remarks Of the Interviewer 4...')
    review_5 = fields.One2many('review.line5', 'applicant_id5', string='Remarks Of the Interviewer 5...')
    review_6 = fields.One2many('review.line6', 'applicant_id6', string='Remarks Of the Interviewer 6...')

    recruiter = fields.Many2one('hr.employee', "Interviewer Name")
    recruiter2 = fields.Many2one('hr.employee', "Interviewer Name")
    recruiter3 = fields.Many2one('hr.employee', "Interviewer Name")
    recruiter4 = fields.Many2one('hr.employee', "Interviewer Name")
    recruiter5 = fields.Many2one('hr.employee', "Interviewer Name")
    recruiter6 = fields.Many2one('hr.employee', "Interviewer Name")

    date = fields.Date("Date")
    date2 = fields.Date("Date")
    date3 = fields.Date("Date")
    date4 = fields.Date("Date")
    date5 = fields.Date("Date")
    date6 = fields.Date("Date")

    duration = fields.Float("Duration In HRS")
    duration2 = fields.Float("Duration In HRS")
    duration3 = fields.Float("Duration In HRS")
    duration4 = fields.Float("Duration In HRS")
    duration5 = fields.Float("Duration In HRS")
    duration6 = fields.Float("Duration In HRS")

    hire = fields.Text("Hire")
    hire2 = fields.Text("Hire")
    hire3 = fields.Text("Hire")
    hire4 = fields.Text("Hire")
    hire5 = fields.Text("Hire")
    hire6 = fields.Text("Hire")

    hold = fields.Text("Hold")
    hold2 = fields.Text("Hold")
    hold3 = fields.Text("Hold")
    hold4 = fields.Text("Hold")
    hold5 = fields.Text("Hold")
    hold6 = fields.Text("Hold")

    proceed_no_further = fields.Text("Proceed no further")
    proceed_no_further2 = fields.Text("Proceed no further")
    proceed_no_further3 = fields.Text("Proceed no further")
    proceed_no_further4 = fields.Text("Proceed no further")
    proceed_no_further5 = fields.Text("Proceed no further")
    proceed_no_further6 = fields.Text("Proceed no further")

    other = fields.Text("Other")
    other2 = fields.Text("Other")
    other3 = fields.Text("Other")
    other4 = fields.Text("Other")
    other5 = fields.Text("Other")
    other6 = fields.Text("Other")

    evaluation = fields.Many2one('recruitment.review', "Evaluation")
    evaluation2 = fields.Many2one('recruitment.review', "Evaluation")
    evaluation3 = fields.Many2one('recruitment.review', "Evaluation")
    evaluation4 = fields.Many2one('recruitment.review', "Evaluation")
    evaluation5 = fields.Many2one('recruitment.review', "Evaluation")
    evaluation6 = fields.Many2one('recruitment.review', "Evaluation")





    def get_partner_first_name(self):
        if self.partner_name:
            result = self.partner_name.split(" ")
            return result[0]

    def generate_offer_letter(self):
        template = self.env.ref('recruitment_management.report_offer_letter_menu', raise_if_not_found=False)
        if not template:
            raise ValueError(_("The mail template is missing..!!!"))
        if not self.salary_breakup_id:
            raise UserError(_("salary breakup is ont selected..!!!"
                              "Please add it to continue"))
        if not self.email_from:
            raise UserError(_("The applicant mail is missing..!!!"))

        # print("&&&**&*&&&*&**&&&&", self)
        # template.sudo().send_mail(self.id, force_send=True, email_values={
        #         'email_from': self.env.company.email,
        #         'email_to': self.email_from})
        return

    @api.constrains("evaluation")
    @api.onchange("evaluation")
    def onchange_evaluation(self):
        self.write({
            'review_1': [(5, 0, 0)]
        })
        if self.evaluation:
            line_vals = []
            for rec in self.evaluation.questions_temp_ref:
                vals = {
                    'questions_que': rec.questions_que
                }
                line_vals.append((0, 0, vals))
            self.write({
                'review_1': line_vals
            })

    @api.constrains("evaluation2")
    @api.onchange("evaluation2")
    def onchange_evaluation2(self):
        self.write({
            'review_2': [(5, 0, 0)]
        })
        if self.evaluation2:
            line_vals = []
            for rec in self.evaluation2.questions_temp_ref:
                vals = {
                    'questions_que': rec.questions_que
                }
                line_vals.append((0, 0, vals))
            self.write({
                'review_2': line_vals
            })

    @api.constrains("evaluation3")
    @api.onchange("evaluation3")
    def onchange_evaluation3(self):
        self.write({
            'review_3': [(5, 0, 0)]
        })
        if self.evaluation3:
            line_vals = []
            for rec in self.evaluation3.questions_temp_ref:
                vals = {
                    'questions_que': rec.questions_que
                }
                line_vals.append((0, 0, vals))
            self.write({
                'review_3': line_vals
            })

    @api.constrains("evaluation4")
    @api.onchange("evaluation4")
    def onchange_evaluation4(self):
        self.write({
            'review_4': [(5, 0, 0)]
        })
        if self.evaluation4:
            line_vals = []
            for rec in self.evaluation4.questions_temp_ref:
                vals = {
                    'questions_que': rec.questions_que
                }
                line_vals.append((0, 0, vals))
            self.write({
                'review_4': line_vals
            })

    @api.constrains("evaluation5")
    @api.onchange("evaluation5")
    def onchange_evaluation5(self):
        self.write({
            'review_5': [(5, 0, 0)]
        })
        if self.evaluation5:
            line_vals = []
            for rec in self.evaluation5.questions_temp_ref:
                vals = {
                    'questions_que': rec.questions_que
                }
                line_vals.append((0, 0, vals))
            self.write({
                'review_5': line_vals,
            })

    @api.constrains("evaluation6")
    @api.onchange("evaluation6")
    def onchange_evaluation6(self):
        self.write({
            'review_6': [(5, 0, 0)]
        })
        if self.evaluation6:
            line_vals = []
            for rec in self.evaluation6.questions_temp_ref:
                vals = {
                    'questions_que': rec.questions_que
                }
                line_vals.append((0, 0, vals))
            self.write({
                'review_6': line_vals
            })

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

class ReviewLine(models.Model):
    _name = "review.line"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    applicant_id = fields.Many2one('hr.applicant')


class ReviewLine2(models.Model):
    _name = "review.line2"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    applicant_id2 = fields.Many2one('hr.applicant')


class ReviewLine3(models.Model):
    _name = "review.line3"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    applicant_id3 = fields.Many2one('hr.applicant')


class ReviewLine4(models.Model):
    _name = "review.line4"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    applicant_id4 = fields.Many2one('hr.applicant')


class ReviewLine5(models.Model):
    _name = "review.line5"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    applicant_id5 = fields.Many2one('hr.applicant')


class ReviewLine6(models.Model):
    _name = "review.line6"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    applicant_id6 = fields.Many2one('hr.applicant')

