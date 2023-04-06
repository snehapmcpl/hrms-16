from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date,datetime


class BackgroundVerification(models.Model):
    _name = 'res.background'

    certificate_level = fields.Selection([('post_graduation_1','Post Graduation one'),('post_graduation','Post Graduation'),
                                          ('graduation','Graduation'),('diploma','Diploma'),('twelfth_or_equivalent','12th or Equivalent'),
                                          ('tenth_or_equivalent','10th or Equivalent'),],string="Degree Name")
    specialization_emp = fields.Char(string="Specialization")
    highest_degree = fields.Boolean(string="Highest Degree")
    other_skill = fields.Text(string="Other Skills")
    board = fields.Char(string="Board/University")
    roll_no = fields.Char(string="Roll No/ID")
    from_month_date = fields.Date(string="From Month & Year")
    end_month_date = fields.Date(string="To Month & Year")
    employee_background = fields.Many2one('hr.employee')
    college_name_emp = fields.Char(string="College Name")
    street_background = fields.Char(string="Stree")
    street2_background = fields.Char(string="Street2")
    pincode_background = fields.Char(change_default=True, string="PIN Code")
    city_background = fields.Char(string="City")
    state_id_background = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id_background = fields.Many2one('res.country', string='Country', ondelete='restrict')

    @api.onchange('highest_degree')
    def on_change_state(self):
        # This method is using for selecting only one highest degree at one time
        # ,if we select once agine it will raise the error
        for record in self.employee_background.background_emp - self:
            if self.highest_degree == True and record.highest_degree == True:
                self.highest_degree = False
                raise UserError(_('The highest degree is selected'))