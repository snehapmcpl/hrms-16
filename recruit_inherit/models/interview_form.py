from odoo import fields,models

class Applicanter(models.Model):
    _inherit = 'hr.applicant'


    family_background1 = fields.Text(string="Family Background")
    economic_status1 = fields.Text(string="Economic Status")
    educational_attain1 = fields.Text(string="Educational Attainments")
    subject_knowledge1 = fields.Text(string="Subject Knowledge")
    work_experience1 = fields.Text(string="Work Experience")
    hobbies1 = fields.Text(string="Hobbies/Interests")
    political_antecedents1 = fields.Text(string="Political Antecedents")
    expected_remun1 = fields.Text(string="Expected Remuneration")
    join_duty1 = fields.Text(string="Time required to Join Duty")
    remarks1 = fields.Text(string="Remarks")

    family_background2 = fields.Text(string="Family Background")
    economic_status2 = fields.Text(string="Economic Status")
    educational_attain2 = fields.Text(string="Educational Attainments")
    subject_knowledge2 = fields.Text(string="Subject Knowledge")
    work_experience2 = fields.Text(string="Work Experience")
    hobbies2 = fields.Text(string="Hobbies/Interests")
    political_antecedents2 = fields.Text(string="Political Antecedents")
    expected_remun2 = fields.Text(string="Expected Remuneration")
    join_duty2 = fields.Text(string="Time required to Join Duty")
    remarks2 = fields.Text(string="Remarks")
