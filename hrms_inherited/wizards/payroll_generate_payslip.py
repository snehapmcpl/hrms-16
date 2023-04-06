from odoo import api, fields, models
from datetime import datetime
from dateutil import relativedelta
from odoo.tools.misc import format_date
from odoo.exceptions import ValidationError, UserError

class payslipPayrollWizard(models.TransientModel):
    _name = "payroll.payslip.wizard"
    _description = "Payroll Payslip Wizard"

    date_from = fields.Date(string='Date From', required=True,
                            default=datetime.now().strftime('%Y-%m-01'))
    date_to = fields.Date(string='Date To', required=True,
                          default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])

    batch_id = fields.Many2one('hr.payslip.run', string='Batch ID', required='True')


    # @api.onchange('date_to')
    # def end_date_day(self):
    #     if self.date_to:
    #         san = self.date_to
    #         mon = san.strftime('%m')
    #         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", mon)
    #         day = san.strftime('%d')
    #         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", day)
    #         mon1 = ['01', '03', '05', '07', '08', '10', '12', '09']
    #         if mon in mon1 and day == 30:
    #             # valid = (('mon', '=', '01', '|', 'mon', '=', '03', '|', 'mon', '=',  '05', '|', 'mon', '=', ' 07', '|', 'mon', '=', '08', '|', 'mon', '=', '10', '|', 'mon', '=', '12'), '&', 'day', '=', '31')
    #             # valid2 = (((mon == )))
    #             print("dayyyyyyyyyyyyyy",day)
    #         else:
    #             raise UserError("Day should be end date")


    @api.onchange('date_from')
    def end_date_day(self):
        if self.date_from:
            date_to: fields.date(str(self.date_from + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])


    def generate_payslip(self):
        payslip = self.env['hr.payslip']
        employee = self.env['hr.employee'].search([])
        date_from = self.date_from
        date_to = self.date_to
        batch = self.batch_id
        for emp in employee:
            exist_payslip = self.env['hr.payslip'].search([('employee_id', '=', emp.id)])
            exist_list = []
            for exist in exist_payslip:
                if str(exist.date_from) == str(date_from):
                    if str(exist.date_to) == str(date_to):
                        exist_list.append(exist)
            if not exist_list:
                rec = self.env['hr.resignation'].search([('employee_id', '=', emp.id)])
                if not rec:
                    if emp.contract_id.state == 'open':
                        vals = {'employee_id': emp.id,
                                'struct_id': emp.contract_id.struct_id.id,
                                'date_from': date_from,
                                'date_to': date_to,
                                'name': '%(payslip_name)s - %(employee_name)s - %(dates)s' % {
                                    'payslip_name': 'Salary Slip',
                                    'employee_name': emp.name,
                                    'dates': format_date(self.env, date_from, date_format="MMMM y")},
                                'payslip_run_id': batch.id,
                                }

                        new_rec = payslip.create(vals)
                        new_rec.compute_sheet()
                        new_rec.calculate_salary_details()
                elif rec:
                    emp_relieving_date = datetime.strptime(str(rec.emp_relieving_date), "%Y-%m-%d")
                    slip_date_from = datetime.strptime(str(date_from), "%Y-%m-%d")
                    if rec.state == 'done' or emp_relieving_date <= slip_date_from:
                        continue
            else:
                pass


