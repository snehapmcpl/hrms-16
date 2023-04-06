from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date,datetime


class EmployeeHistoryUserError(models.Model):
    _inherit = 'rec.history'

    @api.onchange('end_date')
    def onchange_end_date(self):
        for record in self.emp_history.emp_history - self:
            if self.start_date and self.end_date:
                if self.start_date >= self.end_date:
                    raise UserError(_('End Date Must be greater Than Start Date...'))
                if record.end_date >= self.end_date >= record.start_date:
                    raise UserError(_('End Date cannot be between previous employment details..!!'))
                if self.end_date >= record.end_date and self.start_date <= record.start_date:
                    raise UserError(_("Please ensure that there are no other employment details between the entered "
                                      "dates"))

    @api.onchange('start_date')
    def onchange_start_date(self):
        # print('start_date')
        for record in self.emp_history.emp_history - self:
            if self.start_date and self.end_date:
                if self.start_date >= self.end_date:
                    raise UserError(_('End Date Must be greater Than Start Date...'))
                if record.end_date >= self.start_date >= record.start_date:
                    raise UserError(_('Start Date cannot be between previous employment details..!!'))
                if self.end_date >= record.end_date and self.start_date <= record.start_date:
                    raise UserError(_("Please ensure that there are no other employment details between the entered "
                                      "dates"))


