from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date,datetime


class EmployeeBackgroundUserError(models.Model):
    _inherit = 'res.background'

    @api.onchange('end_month_date')
    def onchange_end_date(self):
        if self.from_month_date and self.end_month_date:
            if self.from_month_date >= self.end_month_date:
                raise UserError(_('From Date Must be greater Than To Date...'))

