from odoo import api, fields, models,_
from datetime import date, datetime ,timedelta
from odoo.tools.misc import format_date


class PayrollSummary(models.TransientModel):
    _name = 'payroll.summary.report.wizard'
    _description = 'Payroll Summary Report Wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    report_type = fields.Selection([('monthly pay','Monthly Payroll Summary Report'),
                                    ('bank transfer','Bank Transfer'),
                                    ('earnings deductions','Earnings & Deductions'),
                                    ('pf summary','PF Summary'),
                                    ('ptax recovery','Ptax Recovery Summary'),
                                    ('department summary','Department-wise Summary'),
                                    ('individual pay','Individual Pay Record'),
                                    ('esi summary report', 'ESI Summary Report')])
    earnings_deductions = fields.Selection([("BASIC",'Basic'),
                                 ('HRA','HRA'),
                                 ('SD','Standard Deduction'),
                                 ('LTA','LTA'),
                                 ('FCA','Food Coupon Allowance'),
                                 ('SHIFT','Shift Allowance'),
                                 ('ONSITE','Onsite Allowance'),
                                 ('SPL','Special Allowance'),
                                 ('VA','Variable Allowance'),
                                 ('EPF', 'Employee pf'),
                                 ('FCD', 'Food Coupon Deduction'),
                                 ('IT', 'Income Tax'),
                                 ('HRD', 'HR Deduction'),
                                 ('OTHER', 'Other Deduction'),
                                 ('PT', 'Professional Tax'),
                                 ],'Earnings/Deductions')
    employee_name = fields.Many2one('hr.employee',"Employee Name")
    structure_id = fields.Many2one('hr.payroll.structure', "Structure")


    def generate_payroll_summary(self):
        report = self.env['ir.actions.report']._get_report_from_name('payroll_summary.payroll_summary_report_xls')
        date_from = self.date_from
        date_to = self.date_to
        if self.report_type == 'monthly pay':
            report.name = 'Payroll Summary - %(struct)s -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
                'struct': self.structure_id.name,
            }
        elif self.report_type == 'bank transfer':
            report.name = 'Bank Transfer Summary -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        elif self.report_type == 'earnings deductions':
            report.name = 'Earnings & Deductions -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        elif self.report_type == 'pf summary':
            report.name = 'PF Summary -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        elif self.report_type == 'ptax recovery':
            report.name = 'PTax Recovery Summary -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        elif self.report_type == 'department summary':
            report.name = 'Department-wise Summary -  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        elif self.report_type == 'individual pay':
            report.name = 'Individual Pay Record - %(employee_name)s - %(date_start)s' % {
                'employee_name':self.employee_name.name,
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }
        elif self.report_type == 'esi summary report':
            report.name = 'ESI Summary Report  %(date_start)s' % {
                'date_start': format_date(self.env, date_from, date_format="MMM y"),
            }

        data = {
            'start_date': self.date_from,
             'end_date' : self.date_to,
             'report_type': self.report_type,
             'earnings_deductions': self.earnings_deductions,
             'employee_name':self.employee_name.id,
             'structure_id':self.structure_id.id
        }
        return self.env.ref('payroll_summary.payroll_summary_report_xls').report_action(self,data=data)