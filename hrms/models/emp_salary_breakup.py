from odoo import models, fields, api


class EmpSalaryBreakup(models.Model):
    _inherit = 'employee.salary.breakup'

    name = fields.Many2one("hr.applicant", string="Applicant's Name")
    # employee_name = fields.Many2one("hr.employee",string="Employee Name")
    # employee_salary = fields.Float(related='employee_name.total_ctc',string="Employee ctc salary")
    proposed_salary = fields.Float(related='name.salary_proposed', string="Proposed Salary")
    salary_structure = fields.Many2one("hr.payroll.structure", string="Salary")
    mbo1 = fields.Float()

    @api.onchange('salary_structure')
    @api.depends('salary_structure')
    def onchange_salary_structure(self):
        if self.salary_structure.name == 'Executive Payroll':
            basic1 = self.proposed_salary
            mbo1 = self.mbo1
            mbo1 = mbo1 / 100
            base = basic1 - (basic1 * mbo1)
            print(base)
            lta = 0
            var_alw = 0
            if base <= 400000.00:
                basic_cal = 180000.00
                lta = 0
            elif base > 400000.00 and base <= 700000.00:
                basic_cal = base * 0.5
                lta = 18000
            elif base >= 700000 and base <= 1200000:
                basic_cal = base * 0.45
                lta = 24000
            elif base > 1200000:
                basic_cal = base * 0.45
                lta = 42000
            if basic_cal:
                if base <= 300000:
                    hra = 0
                elif base > 300000:
                    hra = basic_cal * 0.4
            if basic_cal/12 > 15000:
                pf = 1800*12
            else:
                pf = (basic_cal * 0.12)*12

            # if basic_cal/12 > 15000:
            #     epf = (15000 * 0.12)
            # else:
            #     epf = (basic_cal/12 * 12)/100

            if base > 400000.00:
                std_ded = 50000
            else:
                std_ded = 0
            fca = self.food_coupon
            spl_alw = base - (basic_cal + hra + std_ded + lta + pf + fca)
            var_alw = basic1 * mbo1
            self.write({'basic_salary': round(basic_cal),
                        'hra': 0.00,
                        'leave_travel_allowance': 0.00,
                        'standard_deduction': 0.00,
                        'pf_employer_contribution': 0.0,
                        'special_allowance': 0.00,
                        'variable_allowance': 0.00,
                        })
            self.write({'basic_salary': round(basic_cal),
                        'hra': round(hra),
                        'standard_deduction': round(std_ded),
                        'leave_travel_allowance': round(lta),
                        'special_allowance': round(spl_alw),
                        'variable_allowance': round(var_alw),
                        'pf_employer_contribution': round(pf)})
