from odoo import models, fields, _, api
import xlsxwriter
from io import BytesIO
import base64
import datetime
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta



class YtodWizard(models.TransientModel):
    _name = 'ytod.wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    date_from = fields.Date("From")
    date_to = fields.Date("To")

    data = fields.Binary(string='File')
    name = fields.Char(string='Filename')

    def generate_report(self):
        file_data = BytesIO()
        wbk = xlsxwriter.Workbook(file_data)
        format1 = wbk.add_format({'font_size': 11, 'align': 'center'})
        format2 = wbk.add_format({'font_size': 14, 'align': 'center', 'bold': True})
        format3 = wbk.add_format({'font_size': 12, 'align': 'right', 'bold': True})
        format5 = wbk.add_format({'font_size': 11, 'align': 'left'})
        format6 = wbk.add_format({'font_size': 12, 'bold': True})
        format4 = wbk.add_format({'font_size': 12})
        format7 = wbk.add_format({'font_size': 11, 'align': 'center', 'bold': True})
        format8 = wbk.add_format({'font_size': 11, 'align': 'right', 'bold': True, 'num_format': '##0.00'})
        format9 = wbk.add_format({'font_size': 11, 'align': 'right', 'num_format': '##0.00'})
        format10 = wbk.add_format({'font_size': 11, 'num_format': 'dd/mm/yyy'})

        sheet1 = wbk.add_worksheet('YTOD earnings & Deductions statement')
        sheet1.set_column(1, 20, 12)
        sheet1.set_column(0, 0, 25)
        # sheet1 = wbk.add_worksheet('YTOD earnings & Deductions statement - Period From & Period To')
        if self.employee_id.company_id.fiscal_year_start_date:
            sheet1.merge_range(1, 0, 1, 11, "YTOD Earnings & Deductions statement - Period From " + str(self.employee_id.company_id.fiscal_year_start_date.strftime('%d-%b-%Y')) + " & Period To " + str(self.employee_id.company_id.fiscal_year_last_date.strftime('%d-%b-%Y')), format2)
        sheet1.write(2, 0, "Employee Name", format3)
        sheet1.merge_range('B3:C3', self.employee_id.name, format5)
        sheet1.write(3, 0, "Employee Id", format3)
        sheet1.merge_range('B4:C4', self.employee_id.identification_id if self.employee_id.identification_id else '', format5)
        sheet1.merge_range('E3:F3', "PAN", format3)
        sheet1.merge_range('G3:H3', self.employee_id.employee_pan_no if self.employee_id.employee_pan_no else '', format5)
        sheet1.merge_range('E4:F4', "Department", format3)
        sheet1.merge_range('G4:H4', self.employee_id.department_id.name if self.employee_id.department_id.name else '', format5)
        sheet1.merge_range('E5:F5', "Date of Joining", format3)
        sheet1.merge_range('G5:H5', self.employee_id.date_join if self.employee_id.date_join else '', format10)

        start_date, end_date = False, False
        if not self.date_from and not self.date_to:
            start_date = self.employee_id.company_id.fiscal_year_start_date
            end_date = self.employee_id.company_id.fiscal_year_last_date
        elif not self.date_to:
            start_date = self.date_from
            end_date = self.employee_id.company_id.fiscal_year_last_date
        elif self.date_from and self.date_to:
            start_date = self.date_from
            end_date = self.date_to
        else:
            raise UserError(_('Please set the from date and to date.'))
        month_list = []
        while start_date < end_date:
            month_list.append(start_date.strftime('%b-%Y'))
            start_date += relativedelta(months=1)

        sheet1.write(6, 0, "Earnings", format6)
        payslip_rule_ids = self.env['hr.salary.rule'].search([('is_taxable', '=', True)])
        i = 7
        for rules in payslip_rule_ids:
            if rules.category_id.code in ['ALW', 'BASIC']:
                sheet1.write(i, 0, rules.name, format4)
                i += 1
        j = 1
        for rec in month_list:
            sheet1.write(5, j, rec, format1)
            emp_records = self.env['employee.tds'].search([('employee_id', '=', self.employee_id.id),
                                                           ('month', '=', rec)])
            if emp_records:
                i, total = 7, 0
                for rules in payslip_rule_ids:
                    if rules.category_id.code in ['ALW', 'BASIC']:
                        for line in emp_records.line_ids:
                            if rules.name == line.salary_rule_id.name:
                                sheet1.write(i, j, line.amount, format9)
                                total += line.amount
                        i += 1
                sheet1.write(i, j, total, format8)
            j += 1
        sheet1.write(5, j, "Total", format7)
        sheet1.write(i, 0, "Total Earnings", format6)
        for li in range(7, i):
            sheet1.write_formula(li, j, "{=SUM(B"+str(li+1)+":M"+str(li+1)+")}", format8)
            print(li,j,"kdjkkkkkkkkkkkkkkkkkkkk")

        i += 2
        sheet1.write(i, 0, "Deductions", format6)
        i += 1
        for rules in payslip_rule_ids:
            # print(rules.name,"rrrrrrgggggggggggg")
            if rules.category_id.code == 'DED':
                sheet1.write(i, 0, rules.name, format4)
                print(rules.name,i,'$$$$$$$$$$$$$$$$$')
                i += 1
        # sheet1.write(22, 0, 'Income Tax', format4)
        j = 1
        i_new = i - 5
        for rec in month_list:
            emp_records = self.env['employee.tds'].search([('employee_id', '=', self.employee_id.id),
                                                           ('month', '=', rec)])
            if emp_records:
                i, total = i_new, 0
                for rules in payslip_rule_ids:
                    if rules.category_id.code == 'DED':
                        # print(rules.category_id.code, 'qqqqqqqqqqqqqqq')
                        for line in emp_records.line_ids:
                            # print(emp_records.line_ids,'yyyyyyyyyyyyyyy')
                            if rules.name == line.salary_rule_id.name:
                                sheet1.write(i, j, line.amount, format9)
                                print(line.amount,'lllllllllll')
                                print(i,j,'llllllllllqqqqqqqql')
                                total += line.amount
                                print(total,"wwwwwwwwwwwww")

                        i += 1
                sheet1.write(i, j, total, format8)
                # print('eeeeeeeeeeeeeeeeeeeeeeeeee',i,j)
            j += 1
        sheet1.write(i, 0, "Total Deductions", format6)
        for li in range(i_new, i):
            sheet1.write(li, j, "{=SUM(B"+str(li+1)+":M"+str(li+1)+")}", format8)

        wbk.close()
        out = file_data.getvalue()
        self.sudo().write({'data': base64.b64encode(out), 'name': 'YTOD earnings & Deductions statement' + '.xls'})
        return {'type': 'ir.actions.act_url',
                'url': '/YTOD_report?id=' + str(self.id) + '&db=' + str(self.env.cr.dbname) + '&uid=' + str(self.env.uid),
                'nodestroy': True,
                'target': 'current'}
