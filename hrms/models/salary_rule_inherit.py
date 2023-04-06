from odoo import models, fields, _, api
import math

class SalaryRuleInherit(models.Model):
    _inherit = 'hr.salary.rule'

    pf_applicable = fields.Boolean(string="PF Applicable")
    esi_applicable = fields.Boolean(string="ESI Applicable")
    esi_compute = fields.Boolean(string="ESI Compute")


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip.line'

    structure_id = fields.Many2one('hr.payroll.structure', string='Structure')
    esi_com = fields.Boolean(string='ESI compute')
    esi_applicable = fields.Boolean(string="ESI Applicable")


class InheritStructid(models.Model):
    _inherit = "hr.payslip"


    # @api.depends('employee_id')
    # @api.onchange('employee_id')
    # def compute_sheet(self):
    #     res = super(InheritStructid, self).compute_sheet()
    #     esi = self.env['pf.esi.settings'].search([], limit=1)
    #     # esi_inherit = self.env['hr.payslip.line'].search([])
    #     emp_contribution = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employee Contribution')])
    #     empr_contribution = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employer Contribution')])
    #     exe_payroll = self.env['hr.payroll.structure'].search([('name', '=', 'Executive Payroll')])
    #     pf_check_box = self.env['hr.employee'].search([])
    #     print(emp_contribution, exe_payroll)
    #
    #     record = self
    #     esi_not_value = 0.0
    #     for rec in record:
    #         # for line in rec.line_ids:
    #         #     print(line, '3333333')
    #         #     line.structure_id = rec.struct_id
    #         for rule in rec.struct_id.rule_ids:
    #             for line in rec.line_ids:
    #                 line.structure_id = rec.struct_id
    #                 print(line.structure_id.id, "ggggggggggggggggg")
    #                 if rule.name == line.name:
    #                     if rule.esi_applicable == True:
    #                         line.esi_applicable = True
    #                     if rule.esi_compute == True:
    #                         line.esi_com = True
    #             line_list = []
    #             total = 0.0
    #             for line_val in rec.line_ids:
    #                 if line_val.esi_applicable == True:
    #                     line_list.append(line_val.total)
    #
    #
    #             if len(line_list) != 0:
    #                 # esi_total = 0
    #                 for i in line_list:
    #                     print("DDDDDDDDDDDd", i)
    #                     total = total + i
    #                     print(total,'hhhhhhhhhhh')
    #                     esi_emp_total = total * esi.esi_employee_contribution
    #                     esi_empr_total = total * esi.esi_employer_contribution
    #                 print(total ,"111111111111111111111111111")
    #                 print(esi_emp_total,"88888888888888888888888888")
    #                 print(esi_empr_total,"ooooooooooooooooooo")
    #
    #     # for val in record:
    #     #     for rules in rec.struct_id.rule_ids:
    #     #         for line in rec.line_ids:
    #                 for vals in pf_check_box:
    #                         if rule.esi_compute == True and line.esi_com == True:
    #                             print('in first if')
    #                             print(rec.struct_id.name)
    #                         if rec.employee_id.name == vals.name:
    #                             if vals.esi_applicable_check_box == True:
    #                                 if rec.struct_id.name == 'Executive Payroll':
    #                                     if emp_contribution and exe_payroll and empr_contribution and emp_contribution.amount_select == 'code':
    #         # emp_contribution.amount_python_compute = 'result = ' + str(89)
    #         # empr_contribution.amount_python_compute = 'result = ' + str(67)
    #                                         emp_contribution.amount_python_compute = 'result = ' + str(esi_emp_total)
    #                                         empr_contribution.amount_python_compute = 'result = ' + str(esi_empr_total)
    #                                         print(emp_contribution.amount_python_compute, "llllllllllljjjjkkkk")
    #                                         print(empr_contribution.amount_python_compute, "ddddddddddllllllllllljjjjkkkk")
    #
    #                             else:
    #                                 emp_contribution.amount_python_compute = 'result = ' + str(esi_not_value)
    #                                 empr_contribution.amount_python_compute = 'result = ' + str(esi_not_value)
    #                                 print(emp_contribution.amount_python_compute, "llllpooooooppppppppppppppp")
    #                                 print(empr_contribution.amount_python_compute, "daaaaaaaaaaaaaaaaaaaadkkkk")


        # res = super(InheritStructid, record).compute_sheet()


        # return res, emp_contribution.amount_python_compute, empr_contribution.amount_python_compute



    def esi_calculation(self):
        esi = self.env['pf.esi.settings'].search([], limit=1)
        # esi_inherit = self.env['hr.payslip.line'].search([])
        emp_contribution = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employee Contribution')])
        empr_contribution = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employer Contribution')])
        exe_payroll = self.env['hr.payroll.structure'].search([('name', '=', 'Executive Payroll')])
        pf_check_box = self.env['hr.employee'].search([])
        print(emp_contribution, exe_payroll)

        record = self
        esi_not_value = 0.0
        for rec in record:
            # for line in rec.line_ids:
            #     print(line, '3333333')
            #     line.structure_id = rec.struct_id
            for rule in rec.struct_id.rule_ids:
                for line in rec.line_ids:
                    line.structure_id = rec.struct_id
                    print(line.structure_id.id, "ggggggggggggggggg")
                    if rule.name == line.name:
                        if rule.esi_applicable == True:
                            line.esi_applicable = True
                        if rule.esi_compute == True:
                            line.esi_com = True
                line_list = []
                total = 0.0
                for line_val in rec.line_ids:
                    if line_val.esi_applicable == True:
                        line_list.append(line_val.total)

                if len(line_list) != 0:
                    # esi_total = 0
                    for i in line_list:
                        print("DDDDDDDDDDDd", i)
                        total = total + i
                        print(total, 'hhhhhhhhhhh')
                        a = total * esi.esi_employee_contribution / 100
                        esi_emp_total = math.ceil(a)
                        b = total * esi.esi_employer_contribution / 100
                        esi_empr_total = math.ceil(b)
                    print(total, "111111111111111111111111111")
                    print(esi_emp_total,a, "88888888888888888888888888")
                    print(esi_empr_total,b, "ooooooooooooooooooo")

                    # for val in record:
                    #     for rules in rec.struct_id.rule_ids:
                    #         for line in rec.line_ids:
                    for vals in pf_check_box:
                        if rule.esi_compute == True and line.esi_com == True:
                            print('in first if')
                            print(rec.struct_id.name)
                        if rec.employee_id.name == vals.name:
                            if vals.esi_applicable_check_box == True:
                                if rec.struct_id.name == 'Executive Payroll':
                                    if emp_contribution and exe_payroll and empr_contribution and emp_contribution.amount_select == 'code':
                                        # emp_contribution.amount_python_compute = 'result = ' + str(89)
                                        # empr_contribution.amount_python_compute = 'result = ' + str(67)
                                        emp_contribution.amount_python_compute = 'result = ' + str(esi_emp_total)
                                        empr_contribution.amount_python_compute = 'result = ' + str(esi_empr_total)
                                        print(emp_contribution.amount_python_compute, "llllllllllljjjjkkkk")
                                        print(empr_contribution.amount_python_compute, "ddddddddddllllllllllljjjjkkkk")

                            else:
                                emp_contribution.amount_python_compute = 'result = ' + str(esi_not_value)
                                empr_contribution.amount_python_compute = 'result = ' + str(esi_not_value)
                                print(emp_contribution.amount_python_compute, "llllpooooooppppppppppppppp")
                                print(empr_contribution.amount_python_compute, "daaaaaaaaaaaaaaaaaaaadkkkk")

        # res = super(InheritStructid, record).c

        return emp_contribution.amount_python_compute, empr_contribution.amount_python_compute

    def compute_sheet(self):
        for rec in self:
            super(InheritStructid, rec).compute_sheet()
            # rec.compute_sheet_esi()
            rec.esi_calculation()
            super(InheritStructid, rec).compute_sheet()
        return




