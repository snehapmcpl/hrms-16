from odoo import api, fields, models, _
from datetime import datetime


class ResFamily(models.Model):
    _inherit = 'res.family'

    @api.onchange('date_of_birth_rel')
    def onchange_date_of_birth(self):
        if self.date_of_birth_rel:
            age = datetime.today().date() - self.date_of_birth_rel
            self.age_rel = age.days // (365.25)
