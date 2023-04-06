from odoo import api, fields, models, _


class RecruitmentReview(models.Model):
    _name = "recruitment.review"

    name = fields.Char(string="name")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    questions_temp_ref = fields.One2many('recruitment.review.line', 'review_form', string="Questions")


class RecruitmentReviewLine(models.Model):
    _name = "recruitment.review.line"

    questions_que = fields.Text(string="Questions")
    review = fields.Selection([('excellent', 'Excellent'),
                               ('good', 'Good'),
                               ('average', 'Average'),
                               ('fair', 'Fair'),
                               ('poor', 'Poor')], string="Rating")
    review_form = fields.Many2one('recruitment.review')
