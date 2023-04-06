# -*- coding:utf-8 -*-

import babel
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from pytz import timezone
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from num2words import num2words
from datetime import date, datetime, timedelta
from odoo.tools.misc import format_date


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    def action_compute_payroll(self):
        active_id = self._context.get('active_ids')
        rec = self.env['hr.payslip'].browse(active_id)
        for payslip in rec:
            payslip.compute_sheet()

    def action_confirm_payroll(self):
        active_id = self._context.get('active_ids')
        rec = self.env['hr.payslip'].browse(active_id)
        for payslip in rec:
            payslip.action_payslip_done()
