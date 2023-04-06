from odoo import models, fields, _, api


class PFandESIsettings(models.Model):
    _name = "pf.esi.settings"
    _rec_name = "pf_esi_setting"

    pf_esi_setting = fields.Char(string='PF settings')
    pf_salary_limit = fields.Float(string="PF Salary (Monthly Limit) (Basic + DA)")
    pf_contribution = fields.Char(string="PF Contribution")
    employee_contribution = fields.Float(string="Employee Contribution (%)")
    employer_contribution = fields.Float(string="Employer Contribution (%)")
    employee_pension_scheme = fields.Float(string="Employee Pension Scheme (EPS) (%)")
    pf_admin_charges = fields.Char(string="PF Admin Charges")
    epf_admin_charges = fields.Float(string="EPF Admin Charges (%)")
    epf_min_amount_admin_charges = fields.Float(string="EPF Admin Charges(Minimum Amount)")
    edil_admin_charges = fields.Float(string="EDIL Admin Charges (%)")
    edil_min_amount_admin_charges = fields.Float(string="EDIL Admin Charges(Minimum Amount)")
    esi_salary_limit = fields.Float(string="ESI Eligibility (Monthly salary limit)")
    esi_contribution = fields.Char(string="ESI Contribution")
    esi_employee_contribution = fields.Float(string="Employee Contribution (%)")
    esi_employer_contribution = fields.Float(string="Employer Contribution (%)")
    esi_contribution_period_1st_half_year = fields.Char(string="ESI Contribution Period (1st Half Year)")
    date_from_1st_half_year = fields.Date(string="Date From (1st Half Year)")
    date_to_1st_half_year = fields.Date(string="Date To (1st Half Year)")
    esi_contribution_period_2nd_half_year = fields.Char(string="ESI Contribution Period (2nd Half Year)")
    date_from_2nd_half_year = fields.Date(string="Date From (2nd Half Year)")
    date_to_2nd_half_year = fields.Date(string="Date To (2nd Half Year)")


class EPSInherit(models.Model):
    _inherit = "hr.payslip"

    def _default_pf_contribution(self):
        pf = self.env['pf.esi.settings'].search([], limit=1)
        return pf
    # default = _default_pf_contribution
    pf_contribution = fields.Many2one('pf.esi.settings',string="PF Contribution",default=_default_pf_contribution)
    # pf_contribution = fields.Many2one('pf.esi.settings',string="PF Contribution")
    employee_pension_scheme = fields.Float(string="Employee Pension Scheme (EPS) (%)")
    pf_salary_limit = fields.Float(string="PF Salary Limit")
    employee_contribution = fields.Float(string="Employee Contribution (%)")
    employer_contribution = fields.Float(string="Employer Contribution (%)")
    pf_applicable_check_box = fields.Boolean(string="PF CHECK")
    esi_salary_limit = fields.Float(string="ESI Eligibility (Monthly salary limit)")
    esi_employee_contribution = fields.Float(string="Employee Contribution (%)")
    esi_employer_contribution = fields.Float(string="Employer Contribution (%)")

    @api.onchange('employee_id')
    @api.depends('employee_id')
    def _check_pf_contribution(self):
        pf1 = self.env['pf.esi.settings'].search([], limit=1)
        pf_check_box = self.env['hr.employee'].search([])
        for rec in self:
            for vals in pf_check_box:
                if rec.employee_id.name == vals.name:
                    if vals.pf_applicable_check_box == True:
                        rec.employee_pension_scheme = pf1.employee_pension_scheme
                        rec.pf_salary_limit = pf1.pf_salary_limit
                        rec.employee_contribution = pf1.employee_contribution
                        rec.employer_contribution = pf1.employer_contribution
                        print(rec.employer_contribution, rec.employee_contribution, 'aaaaaaaaaaaaa')

                    else:
                        # print('qqqqqqqqqqqqqqqq')
                        # pass

                        rec.employee_pension_scheme = 0.00
                        rec.pf_salary_limit = 0.00
                        rec.employee_contribution = 0.00
                        rec.employer_contribution = 0.00
                        print(rec.employer_contribution, rec.employee_contribution, 'abbbbbbbbbbbbbbbbbbbbbbbb')
                    # if vals.esi_applicable_check_box == True:
                    #     rec.esi_salary_limit = pf1.esi_salary_limit
                    #     rec.esi_employee_contribution = pf1.esi_employee_contribution
                    #     rec.esi_employer_contribution = pf1.esi_employer_contribution
                    #     print(rec.esi_employee_contribution,rec.esi_employer_contribution,'gggggggggggg')
                    #
                    # else:
                    #     rec.esi_salary_limit = 0.0
                    #     rec.esi_employee_contribution = 0.0
                    #     rec.esi_employer_contribution = 0.0



class PFESIcheckbox(models.Model):
    _inherit = "hr.employee"

    pf_applicable_check_box = fields.Boolean(string="PF Applicable")
    esi_applicable_check_box = fields.Boolean(string="ESI Applicable")


