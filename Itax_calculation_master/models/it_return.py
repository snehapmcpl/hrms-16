from odoo import models, fields, _, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class ItReturns(models.Model):
    _name = 'it.returns'
    _rec_name = 'employee_id'

    @api.model
    def list_all_months(self):
        data_list = []
        current_month = (datetime.today().strftime("%b-%Y"), datetime.today().strftime("%b"))
        last_month = (datetime.today() - relativedelta(months=1)).strftime("%b")
        data_list.append(((datetime.today() - relativedelta(months=1)).strftime("%b-%Y"), last_month))
        data_list.append(current_month)
        return data_list

    employee_id = fields.Many2one("hr.employee", string="Employee Name")
    employee_code = fields.Char("Id No", related='employee_id.identification_id')
    pan_no = fields.Char("PAN", related='employee_id.employee_pan_no')
    birthday = fields.Date("Date Of Birth", related='employee_id.birthday')
    age = fields.Integer("Age", related='employee_id.age')
    tax_resign_type = fields.Many2one('tax.slab', string="Tax Regime", compute='onchange_employee_id')
    tax_resign_type_name = fields.Char("Tax Regime Name", related='employee_id.tax_regim_type.name')
    date_from = fields.Date("From Date", default=date.today().replace(day=1))
    date_to = fields.Date("To Date",
                          default=date.today().replace(day=1) + relativedelta(months=1) - relativedelta(days=1))
    relief_under_section_89 = fields.Float("Less: Relief under section 89")

    gross_line_ids = fields.One2many('gross.lines', 'it_return_gross', string="Gross")
    other_income_ids = fields.One2many('other.income.lines', 'it_return_other_income', string="Other Income")
    section_10_line_ids = fields.One2many('tax.section10.lines', 'it_return_section10', string="Section 10")
    section_16_line_ids = fields.One2many('tax.section16.lines', 'it_return_section16', string="Section 16")
    section_24_line_ids = fields.One2many('tax.section24.lines', 'it_return_section24', string="Section 24")
    section_80c_line_ids = fields.One2many('tax.section80c.lines', 'it_return_section80c', string="Section 80C")
    chapter6_line_ids = fields.One2many('tax.chapter6.lines', 'it_return_chapter6', string="Chapter VI A")
    computed_line_ids = fields.One2many('computed.lines', 'it_returns_computed', string="Computed Lines")

    gross_total = fields.Float("Gross Total", compute="compute_gross_total")
    section_10_total = fields.Float("Section 10 Total", compute="compute_section_10_total")
    section_16_total = fields.Float("Section 16 Total", compute="compute_section_16_total")
    other_income_total = fields.Float("Other Income Total", compute="compute_other_income_total")
    section_24_total = fields.Float("Section 24 Total", compute="compute_section_24_total")
    section_80c_total = fields.Float("Section 80C Total", compute="compute_section_80c_total")
    section_80c_max_limit = fields.Float("Section 80C Max Limit", compute="compute_section_80c_max_limit")
    chapter6_total = fields.Float("Chapter VI A Total", compute="compute_chapter6_total")

    rent_paid = fields.Float("Rent Paid")
    actual_hra_received = fields.Float("HRA Received")
    amount_from_basic = fields.Float("Amount From Basic")

    employee_tds_count = fields.Integer("TDS Count", compute='compute_tds_count')

    i_tax = fields.Float("Income Tax")
    surcharge = fields.Float("Surcharge")
    cess = fields.Float("Cess")
    total = fields.Float("Total", compute="compute_total_tds")

    tds_computation_month = fields.Selection(selection='list_all_months', string='TDS Month',
                                             default=datetime.today().strftime("%b-%Y"), required=1)
    state = fields.Selection([('in_progress', 'In Progress'), ('done', 'Done')], string="status", default='in_progress')

    @api.onchange('employee_id')
    def onchange_employee(self):
        for rec in self:
            it_return_obj = self.env['it.returns'].search([('employee_id', '=', rec.employee_id.id)], order='id desc',
                                                          limit=1)
            if it_return_obj:
                rec.section_24_line_ids = it_return_obj.section_24_line_ids
                rec.section_80c_line_ids = it_return_obj.section_80c_line_ids
                rec.chapter6_line_ids = it_return_obj.chapter6_line_ids
            else:
                pass

    def action_confirm(self):
        for rec in self:
            rec.state = 'done'

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for rec in self:
            try:
                employee_rec = self.env['hr.employee.tax'].search([('employee_id', '=', rec.employee_id.id)], limit=1)
            except KeyError:
                employee_rec = False
            if employee_rec:
                if rec.employee_id.tax_regim_type.name == 'Old Regime':
                    rec.update({'gross_line_ids': [(5, 0)]})
                    rec.update({'section_16_line_ids': [(5, 0)]})
                    rec.update({'section_10_line_ids': [(5, 0)]})
                    rec.update({'section_24_line_ids': [(5, 0)]})
                    rec.update({'section_80c_line_ids': [(5, 0)]})
                    rec.update({'chapter6_line_ids': [(5, 0)]})
                    rec.update({'other_income_ids': [(5, 0)]})

                    gross_id = self.env['taxable.income'].search([('salary_rule', '!=', False),
                                                                  ('is_required', '=', True)], limit=1)
                    rec.write({
                        'gross_line_ids': [(0, 0, {'it_return_gross': rec.id,
                                                   'gross_annual_income': gross_id.id,
                                                   'amount': 0.00})],
                    })

                    sec16_id = self.env['tax.section16'].search([('is_required', '=', True)])
                    sec16_list = []
                    for line in sec16_id:
                        data = {
                            'it_return_section16': rec.id,
                            'section_16': line.id,
                            'amount': line.limit_amount,
                        }
                        sec16_list.append((0, 0, data))
                    rec.write({'section_16_line_ids': sec16_list})

                    sec10_list = []
                    sec10_id = self.env['tax.section10'].search([('is_required', '=', True)])
                    for line in sec10_id:
                        data = {
                            'it_return_section10': rec.id,
                            'section_10': line.id,
                            'amount': line.limit_amount,
                        }
                        sec10_list.append((0, 0, data))
                    for line in employee_rec.section_10:
                        data = {
                            'it_return_section10': rec.id,
                            'section_10': line.section_10.id,
                            'document': line.document,
                            'amount': line.amount,
                        }
                        sec10_list.append((0, 0, data))
                    rec.write({
                        'section_10_line_ids': sec10_list,
                    })

                    sec24_list = []
                    for line in employee_rec.section_24:
                        data = {
                            'it_return_section24': rec.id,
                            'section_24': line.section_24.id,
                            'amount': line.amount * (-1),
                            'document': line.document,
                            'max_limit': line.section_24.limit_amount,
                        }
                        sec24_list.append((0, 0, data))
                    rec.write({
                        'section_24_line_ids': sec24_list,
                    })

                    sec80c_list = []
                    for line in employee_rec.section_80c:
                        data = {
                            'it_return_section80c': rec.id,
                            'section_80c': line.section_80c.id,
                            'document': line.document,
                            'amount': line.amount,
                        }
                        sec80c_list.append((0, 0, data))
                    rec.write({
                        'section_80c_line_ids': sec80c_list,
                    })

                    chp6_list = []
                    for line in employee_rec.chapter_VI_A:
                        data = {
                            'it_return_chapter6': rec.id,
                            'chapter6': line.chapter6.id,
                            'amount': line.amount,
                            'max_limit': line.chapter6.limit_amount,
                            'document': line.document,
                        }
                        chp6_list.append((0, 0, data))
                    rec.write({
                        'chapter6_line_ids': chp6_list,
                    })

                    oi_list = []
                    for line in employee_rec.other_income:
                        data = {
                            'it_return_other_income': rec.id,
                            'other_incomes': line.other_incomes.id,
                            'amount': line.amount,
                        }
                        oi_list.append((0, 0, data))
                    rec.write({
                        'other_income_ids': oi_list,
                    })
                else:
                    rec.update({'gross_line_ids': [(5, 0)]})
                    rec.update({'section_16_line_ids': [(5, 0)]})
                    rec.update({'section_10_line_ids': [(5, 0)]})
                    rec.update({'section_24_line_ids': [(5, 0)]})
                    rec.update({'section_80c_line_ids': [(5, 0)]})
                    rec.update({'chapter6_line_ids': [(5, 0)]})
                    rec.update({'other_income_ids': [(5, 0)]})
                    gross_id = self.env['taxable.income'].search([('salary_rule', '!=', False),
                                                                  ('is_required', '=', True)], limit=1)
                    rec.write({
                        'gross_line_ids': [(0, 0, {'it_return_gross': rec.id,
                                                   'gross_annual_income': gross_id.id,
                                                   'amount': 0.00})],
                    })
                    chp6_list = []
                    for line in employee_rec.chapter_VI_A:
                        data = {
                            'it_return_chapter6': rec.id,
                            'chapter6': line.chapter6.id,
                            'amount': line.amount,
                            'max_limit': line.chapter6.limit_amount,
                            'document': line.document,
                        }
                        chp6_list.append((0, 0, data))
                    rec.write({
                        'chapter6_line_ids': chp6_list,
                    })

                    oi_list = []
                    for line in employee_rec.other_income:
                        data = {
                            'it_return_other_income': rec.id,
                            'other_incomes': line.other_incomes.id,
                            'amount': line.amount,
                        }
                        oi_list.append((0, 0, data))
                    rec.write({
                        'other_income_ids': oi_list,
                    })

            else:
                rec.update({'gross_line_ids': [(5, 0)]})
                rec.update({'section_16_line_ids': [(5, 0)]})
                rec.update({'section_10_line_ids': [(5, 0)]})
                rec.update({'section_24_line_ids': [(5, 0)]})
                rec.update({'section_80c_line_ids': [(5, 0)]})
                rec.update({'chapter6_line_ids': [(5, 0)]})
                rec.update({'other_income_ids': [(5, 0)]})

            pay_slip_id = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id)], order='id desc',
                                                        limit=1)
            pf_id = self.env['tax.section80c'].search([('name', '=', 'EPF Contribution')], limit=1)
            if pay_slip_id and pf_id:
                for slip_rec in pay_slip_id.line_ids:
                    if slip_rec.code == 'EPF':
                        rec.update({
                            'section_80c_line_ids': [(0, 0, {'it_return_section80c': rec.id,
                                                             'section_80c': pf_id.id,
                                                             'amount': (slip_rec.total * 12), })],
                        })

    @api.onchange('i_tax', 'surcharge', 'cess')
    def compute_total_tds(self):
        for rec in self:
            rec.total = rec.i_tax + rec.surcharge + rec.cess

    def tds_action(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("Itax_calculation_master.action_employee_tds")
        action['domain'] = [('employee_id', '=', self.employee_id.id)]
        return action

    def compute_tds_count(self):
        for rec in self:
            rec.employee_tds_count = self.env['employee.tds'].search_count([('employee_id', '=', self.employee_id.id)])

    def compute_gross_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.gross_line_ids:
                total += lines.amount
            rec.gross_total = total

    def compute_section_10_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.section_10_line_ids:
                total += lines.amount
            rec.section_10_total = total

    def compute_section_16_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.section_16_line_ids:
                total += lines.amount
            rec.section_16_total = total

    def compute_other_income_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.other_income_ids:
                total += lines.amount
            rec.other_income_total = total

    def compute_section_24_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.section_24_line_ids:
                if lines.amount and lines.max_limit:
                    total += max(lines.max_limit, lines.amount)
                elif not lines.max_limit and lines.amount:
                    total += lines.amount
            rec.section_24_total = total

    def compute_section_80c_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.section_80c_line_ids:
                total += lines.amount
            rec.section_80c_total = total

    def compute_section_80c_max_limit(self):
        rec = self.env['tax.max.limit'].search([('active', '=', True)], limit=1)
        self.section_80c_max_limit = rec.max_limit_for_section_80c

    def compute_chapter6_total(self):
        for rec in self:
            total = 0.00
            for lines in rec.chapter6_line_ids:
                if lines.amount and lines.max_limit:
                    total += min(lines.max_limit, lines.amount)
                elif not lines.max_limit and lines.amount:
                    total += lines.amount
            rec.chapter6_total = total

    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.tax_resign_type = self.employee_id.tax_regim_type.id
        else:
            self.tax_resign_type = False

    def create_older_lines(self):
        for rec in self:
            current_date = datetime.now()
            start = self.env.company.fiscal_year_start_date
            end = self.env.company.fiscal_year_last_date
            date_list = []
            while start < end:
                date_list.append(start)
                start += relativedelta(months=1)

            pop_list = []
            for dt in range(len(date_list)):
                if date_list[dt] > current_date.date():
                    pop_list.append(dt)
            pop_list = list(reversed(pop_list))
            for pd in pop_list:
                date_list.pop(pd)
            date_list.pop(len(date_list) - 1)
            for dates in date_list:
                payslip = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id),
                                                         ('date_from', '=', dates),
                                                         ('date_to', '=',
                                                          dates + relativedelta(months=1) - relativedelta(days=1))])
                month = dates.strftime("%b-%Y")
                tds_id = self.env['employee.tds'].search([('employee_id', '=', rec.employee_id.id),
                                                          ('month', '=', month)])
                if payslip:
                    if tds_id:
                        tds_id.update({
                            'date': dates,
                            'income_tax': round(payslip.income_tax),
                            'surcharge': 0.00,
                            'cess': 0.00,
                            'total_amount': round(payslip.income_tax),
                            'payslip_id': payslip.id,
                        })
                    else:
                        tds_id = self.env['employee.tds'].create({
                            'employee_id': rec.employee_id.id,
                            'month': month,
                            'date': dates,
                            'income_tax': round(payslip.income_tax),
                            'surcharge': 0.00,
                            'cess': 0.00,
                            'total_amount': round(payslip.income_tax),
                            'payslip_id': payslip.id,
                        })

                    payslip_rule_ids = self.env['hr.salary.rule'].search([('is_taxable', '=', True)])
                    payslip_line_ids = self.env['hr.payslip.line'].search([('slip_id', '=', payslip.id),
                                                                           ('salary_rule_id', 'in',
                                                                            payslip_rule_ids.ids)])
                    tds_id.line_ids.unlink()
                    tds_data_list = []
                    for tds_data in payslip_line_ids:
                        data = {
                            'salary_rule_id': tds_data.salary_rule_id.id,
                            'amount': tds_data.total,
                        }
                        tds_data_list.append((0, 0, data))
                    tds_id.update({'line_ids': tds_data_list})

    def compute_tax_sheet(self):
        for rec in self:
            pay_slip_id = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id)], order='id desc',
                                                        limit=1)
            if pay_slip_id:
                rec.computed_line_ids.unlink()
                net_amount, gross_total, sec10_total, sec16_total, oth_in_total, sec24_total, sec192_total, sec80c_total, chp6_total, sur_tax, applied_tax, cess_tax = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                if rec.tax_resign_type.name == 'Old Regime':
                    if rec.gross_line_ids:
                        for lines in rec.gross_line_ids:
                            if lines.gross_annual_income.salary_rule:
                                lines.amount = (pay_slip_id.basic_salary + pay_slip_id.hra
                                                + pay_slip_id.standard_deduction + pay_slip_id.lta
                                                + pay_slip_id.special_allowance)
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': "Basic Salary",
                                                                  'amount': pay_slip_id.basic_salary,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.basic_salary}),
                                                          (0, 0, {'name': "HRA",
                                                                  'amount': pay_slip_id.hra,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.hra}),
                                                          (0, 0, {'name': "Standard Deduction",
                                                                  'amount': pay_slip_id.standard_deduction,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.standard_deduction}),
                                                          (0, 0, {'name': "LTA",
                                                                  'amount': pay_slip_id.lta,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.lta}),
                                                          (0, 0, {'name': "Special Allowance",
                                                                  'amount': pay_slip_id.special_allowance,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.special_allowance}),
                                                          ],
                                })
                                gross_total += (pay_slip_id.basic_salary + pay_slip_id.hra
                                                + pay_slip_id.standard_deduction + pay_slip_id.lta
                                                + pay_slip_id.special_allowance)

                                for rule_line in lines.gross_annual_income.salary_rule:
                                    for rules in pay_slip_id.line_ids:
                                        if rule_line.code == rules.code:
                                            if rules.amount != 0.00:
                                                if rules.salary_rule_id.rule_type == 'fixed':
                                                    rec.update({
                                                        'computed_line_ids': [(0, 0, {'name': rules.name,
                                                                                      'amount': rules.amount * 12,
                                                                                      'color': 'blue',
                                                                                      'amount_total': rules.total * 12})],
                                                    })
                                                    gross_total += rules.amount * 12
                                                else:
                                                    rec.update({
                                                        'computed_line_ids': [(0, 0, {'name': rules.name,
                                                                                      'amount': rules.amount,
                                                                                      'color': 'blue',
                                                                                      'amount_total': rules.total})],
                                                    })
                                                    gross_total += rules.amount

                            elif lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.gross_annual_income.name,
                                                                  'amount': lines.amount,
                                                                  'color': 'blue',
                                                                  'amount_total': lines.amount})],
                                })
                                gross_total += lines.amount
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Total Gross Salary',
                                                          'amount': gross_total,
                                                          'color': 'bold',
                                                          'amount_total': gross_total})],
                        })

                    if rec.section_10_line_ids:
                        # add a user error for the city type (if not available)
                        for lines in rec.section_10_line_ids:
                            if 'House Rent Allowance' in lines.section_10.name:
                                if rec.employee_id.rent_paid:
                                    actual_hra_received = pay_slip_id.hra
                                    amount_from_basic = (pay_slip_id.basic_salary * (
                                            rec.employee_id.city_type_conf.percent / 100))
                                    rent_paid = (rec.employee_id.rent_paid * 12) - (
                                            pay_slip_id.basic_salary * (10 / 100))

                                    if rent_paid < 0:
                                        rent_paid = 0.00
                                    rec.rent_paid = rent_paid
                                    rec.actual_hra_received = actual_hra_received
                                    rec.amount_from_basic = amount_from_basic

                                    rec.update({
                                        'computed_line_ids': [(0, 0, {'name': lines.section_10.name,
                                                                      'amount': min(actual_hra_received,
                                                                                    amount_from_basic, rent_paid),
                                                                      'color': 'brown',
                                                                      'amount_total': min(actual_hra_received,
                                                                                          amount_from_basic, rent_paid)
                                                                      })],
                                    })
                                    lines.update({
                                        'amount': min(actual_hra_received, amount_from_basic, rent_paid),
                                    })
                                    sec10_total += min(actual_hra_received, amount_from_basic, rent_paid)
                            elif lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.section_10.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'brown'
                                                                  })],
                                })
                                sec10_total += lines.amount
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Total amount of exemption claimed under section 10',
                                                          'amount': sec10_total,
                                                          'color': 'bold',
                                                          'amount_total': sec10_total})],
                        })
                    net_amount = gross_total - sec10_total
                    if net_amount:
                        rec.update({
                            'computed_line_ids': [
                                (0, 0, {'name': 'Total amount of salary received from current employer',
                                        'amount': net_amount,
                                        # 'flag': 'Total amount of salary received from current employer (1 + 2)',
                                        'color': 'bold',
                                        'amount_total': net_amount})],
                        })

                    if rec.section_16_line_ids:
                        for lines in rec.section_16_line_ids:
                            if 'Tax on employment' in lines.section_16.name:
                                for p_slip_lines in pay_slip_id.line_ids:
                                    if p_slip_lines.code == 'PT':
                                        tax_amount = p_slip_lines.amount * 12
                                        lines.update({
                                            'amount': tax_amount,
                                        })
                                        rec.update({
                                            'computed_line_ids': [(0, 0, {'name': lines.section_16.name,
                                                                          'amount': tax_amount,
                                                                          'amount_total': tax_amount,
                                                                          'color': 'blue'
                                                                          })],
                                        })
                                sec16_total += tax_amount
                            elif lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.section_16.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'blue'
                                                                  })],
                                })
                                sec16_total += lines.amount
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Total amount of deductions under section 16',
                                                          'amount': sec16_total,
                                                          'amount_total': sec16_total,
                                                          'color': 'bold'
                                                          })],
                        })
                    if net_amount and sec16_total:
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Income chargeable under the head "Salaries"',
                                                          'amount': net_amount - sec16_total,
                                                          'color': 'bold',
                                                          'amount_total': net_amount - sec16_total})],
                        })
                        net_amount = net_amount - sec16_total

                    if rec.other_income_ids:
                        for lines in rec.other_income_ids:
                            if lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.other_incomes.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'brown'
                                                                  })],
                                })
                                oth_in_total += lines.amount
                    if oth_in_total:
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Income under the head Other Sources offered for TDS',
                                                          'amount': oth_in_total,
                                                          'color': 'bold',
                                                          'amount_total': oth_in_total})],
                        })

                    if rec.section_24_line_ids:
                        for lines in rec.section_24_line_ids:
                            if lines.max_limit and lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.section_24.name,
                                                                  'amount': max(lines.max_limit, lines.amount),
                                                                  'amount_total': max(lines.max_limit, lines.amount),
                                                                  'color': 'blue'
                                                                  })],
                                })
                                sec24_total += sec24_total + max(lines.max_limit, lines.amount)
                            elif not lines.max_limit and lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.section_24.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'blue'
                                                                  })],
                                })
                                sec24_total += sec24_total + lines.amount
                    if sec24_total:
                        rec.update({
                            'computed_line_ids': [(0, 0, {
                                'name': 'Income (or admissible loss) from house property reported by employee offered for TDS',
                                'amount': sec24_total,
                                'color': 'bold',
                                'amount_total': sec24_total})],
                        })

                    if oth_in_total and sec24_total:
                        rec.update({
                            'computed_line_ids': [
                                (0, 0, {'name': 'Total amount of other income reported by the employee',
                                        'amount': oth_in_total + sec24_total,
                                        'color': 'bold',
                                        'amount_total': oth_in_total + sec24_total})],
                        })
                        sec192_total = oth_in_total + sec24_total

                    if net_amount and sec192_total:
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Gross total income',
                                                          'amount': net_amount + sec192_total,
                                                          'color': 'bold',
                                                          'amount_total': net_amount + sec192_total})],
                        })
                        net_amount = net_amount + sec192_total

                    if rec.section_80c_line_ids:
                        amount = 0
                        for lines in rec.section_80c_line_ids:
                            amount += lines.amount
                        if amount and self.section_80c_max_limit:
                            amount = min(amount, self.section_80c_max_limit)
                            rec.update({
                                'computed_line_ids': [(0, 0, {'name': "Deduction Under Section 80C",
                                                              'amount': amount,
                                                              'amount_total': amount,
                                                              'color': 'brown'
                                                              })],
                            })
                        sec80c_total = amount

                    if rec.chapter6_line_ids:
                        for lines in rec.chapter6_line_ids:
                            if lines.amount and lines.max_limit:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.chapter6.name,
                                                                  'amount': min(lines.max_limit, lines.amount),
                                                                  'amount_total': min(lines.max_limit, lines.amount),
                                                                  'color': 'blue'
                                                                  })],
                                })
                                chp6_total += min(lines.max_limit, lines.amount)
                            elif not lines.max_limit and lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.chapter6.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'blue'
                                                                  })],
                                })
                                chp6_total += lines.amount

                    if sec80c_total and chp6_total:
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Aggregate of deductible amount under Chapter VI-A',
                                                          'amount': sec80c_total + chp6_total,
                                                          'color': 'bold',
                                                          'amount_total': sec80c_total + chp6_total})],
                        })
                    if net_amount and sec80c_total:
                        net_amount = net_amount - (sec80c_total + chp6_total)
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Total taxable income',
                                                          'amount': round(net_amount, -1),
                                                          'color': 'bold',
                                                          'amount_total': round(net_amount, -1)})],
                        })

                    if net_amount:
                        for slab_lines in self.tax_resign_type.line_ids:
                            if (net_amount >= slab_lines.lower_limit) and (net_amount <= slab_lines.higher_limit):
                                amount = net_amount - slab_lines.lower_limit
                                applied_tax = amount * (slab_lines.tax_per / 100)

                        for slab_lines in self.tax_resign_type.line_ids:
                            if (net_amount > slab_lines.higher_limit):
                                applied_tax += round(slab_lines.higher_limit - slab_lines.lower_limit) * (
                                        slab_lines.tax_per / 100)
                        applied_tax = round(applied_tax)
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Total Tax Payable',
                                                          'amount': applied_tax,
                                                          'color': 'bold',
                                                          'amount_total': applied_tax})],
                        })
                        rec.i_tax = applied_tax
                        sec_87tax = 0.00
                        for sec87_lines in self.tax_resign_type.section87a_ids:
                            if (net_amount >= sec87_lines.lower_limit) and (net_amount <= sec87_lines.higher_limit):
                                if sec87_lines.tax_amount < applied_tax:
                                    sec_87tax = sec87_lines.tax_amount
                                    applied_tax = applied_tax - sec87_lines.tax_amount
                                else:
                                    sec_87tax = applied_tax
                                    applied_tax = 0.00
                            rec.update({
                                'computed_line_ids': [(0, 0, {'name': 'Rebate under section 87A, if applicable',
                                                              'amount': sec_87tax,
                                                              'color': 'bold',
                                                              'amount_total': sec_87tax})],
                            })
                        for sur_lines in self.tax_resign_type.surcharge_ids:
                            if (net_amount >= sur_lines.lower_limit) and (net_amount <= sur_lines.higher_limit):
                                sur_tax = applied_tax * (sur_lines.tax_per / 100)
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Surcharge, wherever applicable',
                                                          'amount': sur_tax,
                                                          'color': 'bold',
                                                          'amount_total': sur_tax})],
                        })
                        rec.surcharge = sur_tax
                        for cess_lines in self.tax_resign_type.cess_ids:
                            if (net_amount >= cess_lines.lower_limit) and (net_amount <= cess_lines.higher_limit):
                                cess_tax = round(applied_tax * (cess_lines.tax_per / 100))
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Health and education cess',
                                                          'amount': cess_tax,
                                                          'color': 'bold',
                                                          'amount_total': cess_tax})],
                        })
                        rec.cess = cess_tax
                        if applied_tax:
                            tax_payable = (applied_tax + sur_tax + cess_tax)
                        else:
                            tax_payable = 0.00
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Tax payable',
                                                          'amount': tax_payable,
                                                          'color': 'bold',
                                                          'amount_total': tax_payable})],
                        })
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Less: Relief under section 89',
                                                          'amount': self.relief_under_section_89,
                                                          'color': 'bold',
                                                          'amount_total': self.relief_under_section_89})],
                        })
                        tax_payable = tax_payable - self.relief_under_section_89
                        if tax_payable < 0:
                            tax_payable = 0.00
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Net tax payable',
                                                          'amount': round(tax_payable, -1),
                                                          'color': 'bold',
                                                          'amount_total': round(tax_payable, -1)})],
                        })

                    current_date = datetime.now()
                    month = self.tds_computation_month
                    start = self.env.company.fiscal_year_start_date
                    end = self.env.company.fiscal_year_last_date
                    date_list = []
                    while start < end:
                        date_list.append(start)
                        start += relativedelta(months=1)
                    tds_id = self.env['employee.tds'].search([('employee_id', '=', rec.employee_id.id),
                                                              ('month', '=', month)])
                    pop_list = []
                    for dt in range(len(date_list)):
                        if date_list[dt] < current_date.date():
                            pop_list.append(dt)
                    range_val = len(pop_list) - 1
                    for pd in range(range_val):
                        if len(date_list) == pd - 1:
                            date_list.pop(pd)
                    future_months = len(date_list) + 1
                    recovered_amounts = self.report_recovered_so_far()
                    pay_slip = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id),
                                                              ('date_from', '<=',
                                                               datetime.strptime("2-" + month, "%d-%b-%Y")),
                                                              ('date_to', '>=',
                                                               datetime.strptime("2-" + month, "%d-%b-%Y"))], limit=1)
                    if tds_id:
                        tds_id.update({
                            'date': datetime.today().replace(day=1),
                            'income_tax': round((applied_tax - recovered_amounts.get('i_tax')) / future_months),
                            'surcharge': round((sur_tax - recovered_amounts.get('surcharge')) / future_months),
                            'cess': round((cess_tax - recovered_amounts.get('cess')) / future_months),
                            'total_amount': round(
                                (applied_tax - recovered_amounts.get('i_tax')) / future_months) + round(
                                (sur_tax - recovered_amounts.get('surcharge')) / future_months) + round(
                                (cess_tax - recovered_amounts.get('cess')) / future_months),
                            'payslip_id': pay_slip.id if pay_slip else False,
                        })
                    else:
                        tds_id = self.env['employee.tds'].create({
                            'employee_id': rec.employee_id.id,
                            'month': month,
                            'date': datetime.strptime("1-" + month, "%d-%b-%Y"),
                            'income_tax': round((applied_tax - recovered_amounts.get('i_tax')) / future_months),
                            'surcharge': round((sur_tax - recovered_amounts.get('surcharge')) / future_months),
                            'cess': round((cess_tax - recovered_amounts.get('cess')) / future_months),
                            'total_amount': round(
                                (applied_tax - recovered_amounts.get('i_tax')) / future_months) + round(
                                (sur_tax - recovered_amounts.get('surcharge')) / future_months) + round(
                                (cess_tax - recovered_amounts.get('cess')) / future_months),
                            'payslip_id': pay_slip.id if pay_slip else False,
                        })

                else:
                    if rec.gross_line_ids:
                        for lines in rec.gross_line_ids:
                            if lines.gross_annual_income.salary_rule:
                                lines.amount = (pay_slip_id.basic_salary + pay_slip_id.hra
                                                + pay_slip_id.standard_deduction + pay_slip_id.lta
                                                + pay_slip_id.special_allowance)
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': "Basic Salary",
                                                                  'amount': pay_slip_id.basic_salary,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.basic_salary}),
                                                          (0, 0, {'name': "HRA",
                                                                  'amount': pay_slip_id.hra,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.hra}),
                                                          (0, 0, {'name': "Standard Deduction",
                                                                  'amount': pay_slip_id.standard_deduction,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.standard_deduction}),
                                                          (0, 0, {'name': "LTA",
                                                                  'amount': pay_slip_id.lta,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.lta}),
                                                          (0, 0, {'name': "Special Allowance",
                                                                  'amount': pay_slip_id.special_allowance,
                                                                  'color': 'blue',
                                                                  'amount_total': pay_slip_id.special_allowance}),
                                                          ],
                                })
                                gross_total += (pay_slip_id.basic_salary + pay_slip_id.hra
                                                + pay_slip_id.standard_deduction + pay_slip_id.lta
                                                + pay_slip_id.special_allowance)

                                for rule_line in lines.gross_annual_income.salary_rule:
                                    for rules in pay_slip_id.line_ids:
                                        if rule_line.code == rules.code:
                                            if rules.amount != 0.00:
                                                if rules.salary_rule_id.rule_type == 'fixed':
                                                    rec.update({
                                                        'computed_line_ids': [(0, 0, {'name': rules.name,
                                                                                      'amount': rules.amount * 12,
                                                                                      'color': 'blue',
                                                                                      'amount_total': rules.total * 12})],
                                                    })
                                                    gross_total += rules.amount * 12
                                                else:
                                                    rec.update({
                                                        'computed_line_ids': [(0, 0, {'name': rules.name,
                                                                                      'amount': rules.amount,
                                                                                      'color': 'blue',
                                                                                      'amount_total': rules.total})],
                                                    })
                                                    gross_total += rules.amount

                            elif lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.gross_annual_income.name,
                                                                  'amount': lines.amount,
                                                                  'color': 'blue',
                                                                  'amount_total': lines.amount})],
                                })
                                gross_total += lines.amount
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Total Gross Salary',
                                                          'amount': gross_total,
                                                          'color': 'bold',
                                                          'amount_total': gross_total})],
                        })

                    if rec.other_income_ids:
                        for lines in rec.other_income_ids:
                            if lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.other_incomes.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'brown'
                                                                  })],
                                })
                                oth_in_total += lines.amount
                    if oth_in_total:
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Income under the head Other Sources offered for TDS',
                                                          'amount': oth_in_total,
                                                          'color': 'bold',
                                                          'amount_total': oth_in_total})],
                        })

                    if rec.chapter6_line_ids:
                        for lines in rec.chapter6_line_ids:
                            if lines.amount and lines.max_limit:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.chapter6.name,
                                                                  'amount': min(lines.max_limit, lines.amount),
                                                                  'amount_total': min(lines.max_limit, lines.amount),
                                                                  'color': 'blue'
                                                                  })],
                                })
                                chp6_total += min(lines.max_limit, lines.amount)
                            elif not lines.max_limit and lines.amount:
                                rec.update({
                                    'computed_line_ids': [(0, 0, {'name': lines.chapter6.name,
                                                                  'amount': lines.amount,
                                                                  'amount_total': lines.amount,
                                                                  'color': 'blue'
                                                                  })],
                                })
                                chp6_total += lines.amount

                    rec.update({
                        'computed_line_ids': [(0, 0, {'name': 'Total Income',
                                                      'amount': gross_total + oth_in_total + chp6_total,
                                                      'amount_total': gross_total + oth_in_total + chp6_total,
                                                      'color': 'bold'
                                                      })],
                    })
                    net_amount = gross_total + oth_in_total + chp6_total
                    applied_tax = 0.00
                    for slab_lines in self.tax_resign_type.line_ids:
                        if (net_amount >= slab_lines.lower_limit) and (net_amount <= slab_lines.higher_limit):
                            amount = net_amount - slab_lines.lower_limit
                            applied_tax = amount * (slab_lines.tax_per / 100)

                    for slab_lines in self.tax_resign_type.line_ids:
                        if (net_amount > slab_lines.higher_limit):
                            applied_tax += round(slab_lines.higher_limit - slab_lines.lower_limit) * (
                                    slab_lines.tax_per / 100)

                    sec_87tax = 0.00
                    for sec87_lines in self.tax_resign_type.section87a_ids:
                        if (net_amount >= sec87_lines.lower_limit) and (net_amount <= sec87_lines.higher_limit):
                            if sec87_lines.tax_amount < net_amount:
                                sec_87tax = net_amount - sec87_lines.tax_amount
                            else:
                                sec_87tax = applied_tax
                                applied_tax = 0.00
                        rec.update({
                            'computed_line_ids': [(0, 0, {'name': 'Rebate under section 87A, if applicable',
                                                          'amount': sec_87tax,
                                                          'color': 'bold',
                                                          'amount_total': sec_87tax})],
                        })

                    applied_tax = round(applied_tax - sec_87tax)
                    rec.update({
                        'computed_line_ids': [(0, 0, {'name': 'Total Tax Payable',
                                                      'amount': applied_tax,
                                                      'color': 'bold',
                                                      'amount_total': applied_tax})],
                    })
                    rec.i_tax = applied_tax
                    for sur_lines in self.tax_resign_type.surcharge_ids:
                        if (net_amount >= sur_lines.lower_limit) and (net_amount <= sur_lines.higher_limit):
                            sur_tax = applied_tax * (sur_lines.tax_per / 100)
                    rec.update({
                        'computed_line_ids': [(0, 0, {'name': 'Tax Surcharge, wherever applicable',
                                                      'amount': sur_tax,
                                                      'color': 'bold',
                                                      'amount_total': sur_tax})],
                    })
                    rec.surcharge = sur_tax
                    cess_tax = 0.00
                    for cess_lines in self.tax_resign_type.cess_ids:
                        if (net_amount >= cess_lines.lower_limit) and (net_amount <= cess_lines.higher_limit):
                            cess_tax = round(applied_tax * (cess_lines.tax_per / 100))
                            rec.update({
                                'computed_line_ids': [(0, 0, {'name': 'Add; Edn Cess + Health Cess',
                                                              'amount': cess_tax,
                                                              'color': 'bold',
                                                              'amount_total': cess_tax})],
                            })
                    rec.cess = cess_tax
                    tax_payable = round(applied_tax + sur_tax + cess_tax, -1)
                    rec.update({
                        'computed_line_ids': [(0, 0, {'name': 'Net Tax Payable',
                                                      'amount': tax_payable,
                                                      'color': 'bold',
                                                      'amount_total': tax_payable})],
                    })

                    current_date = datetime.now()
                    month = self.tds_computation_month
                    start = self.env.company.fiscal_year_start_date
                    end = self.env.company.fiscal_year_last_date
                    date_list = []
                    while start < end:
                        date_list.append(start)
                        start += relativedelta(months=1)
                    tds_id = self.env['employee.tds'].search([('employee_id', '=', rec.employee_id.id),
                                                              ('month', '=', month)])
                    pop_list = []
                    for dt in range(len(date_list)):
                        if date_list[dt] < current_date.date():
                            pop_list.append(dt)
                    range_val = len(pop_list) - 1
                    for pd in range(range_val):
                        if len(date_list) == pd - 1:
                            date_list.pop(pd)
                    future_months = len(date_list) + 1
                    recovered_amounts = self.report_recovered_so_far()
                    pay_slip = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id),
                                                              ('date_from', '<=',
                                                               datetime.strptime("2-" + month, "%d-%b-%Y")),
                                                              ('date_to', '>=',
                                                               datetime.strptime("2-" + month, "%d-%b-%Y"))], limit=1)
                    if tds_id:
                        tds_id.update({
                            'date': date_list[0],
                            'payslip_id': pay_slip.id if pay_slip else False,
                            'income_tax': round((applied_tax - recovered_amounts.get('i_tax')) / future_months),
                            'surcharge': round((sur_tax - recovered_amounts.get('surcharge')) / future_months),
                            'cess': round((cess_tax - recovered_amounts.get('cess')) / future_months),
                            'total_amount': round(
                                (applied_tax - recovered_amounts.get('i_tax')) / future_months) + round(
                                (sur_tax - recovered_amounts.get('surcharge')) / future_months) + round(
                                (cess_tax - recovered_amounts.get('cess')) / future_months),
                        })
                    else:
                        tds_id = self.env['employee.tds'].create({
                            'employee_id': rec.employee_id.id,
                            'payslip_id': pay_slip.id if pay_slip else False,
                            'month': month,
                            'date': datetime.strptime("1-" + month, "%d-%b-%Y"),
                            'income_tax': round((applied_tax - recovered_amounts.get('i_tax')) / future_months),
                            'surcharge': round((sur_tax - recovered_amounts.get('surcharge')) / future_months),
                            'cess': round((cess_tax - recovered_amounts.get('cess')) / future_months),
                            'total_amount': round(
                                (applied_tax - recovered_amounts.get('i_tax')) / future_months) + round(
                                (sur_tax - recovered_amounts.get('surcharge')) / future_months) + round(
                                (cess_tax - recovered_amounts.get('cess')) / future_months),
                        })

                payslip_rule_ids = self.env['hr.salary.rule'].search([('is_taxable', '=', True)])
                payslip_line_ids = self.env['hr.payslip.line'].search([('slip_id', '=', pay_slip_id.id),
                                                                       ('salary_rule_id', 'in', payslip_rule_ids.ids)])
                tds_id.line_ids.unlink()
                tds_id.computed_line_ids.unlink()
                tds_data_list, com_data_list = [], []
                for tds_data in payslip_line_ids:
                    data = {
                        'salary_rule_id': tds_data.salary_rule_id.id,
                        'amount': tds_data.total,
                    }
                    tds_data_list.append((0, 0, data))
                tds_id.update({'line_ids': tds_data_list})
                for line_data in rec.computed_line_ids:
                    data = {
                        'name': line_data.name,
                        'amount': line_data.amount_total,
                    }
                    com_data_list.append((0, 0, data))
                tds_id.update({'computed_line_ids': com_data_list})

    def report_recovered_so_far(self):
        emp_tds_ids = self.env['employee.tds'].search([('employee_id', '=', self.employee_id.id),
                                                       ('date', '>=', self.env.company.fiscal_year_start_date),
                                                       ('date', '<', datetime.today().replace(day=1))])
        i_tax, surcharge, cess, total = 0, 0, 0, 0
        for tds in emp_tds_ids:
            i_tax += tds.income_tax
            surcharge += tds.surcharge
            cess += tds.cess
            total += tds.total_amount
        return {
            'i_tax': i_tax,
            'surcharge': surcharge,
            'cess': cess,
            'total': total,
        }

    def report_TDS_payable(self):
        return {
            'i_tax': self.i_tax,
            'surcharge': self.surcharge,
            'cess': self.cess,
            'total': self.total,
        }

    def report_recovery_for_the_month(self):
        emp_tds_id = self.env['employee.tds'].search(
            [('employee_id', '=', self.employee_id.id), ('date', '=', datetime.today().replace(day=1))], limit=1)
        if emp_tds_id:
            return {
                'i_tax': round(emp_tds_id.income_tax, 2),
                'surcharge': round(emp_tds_id.surcharge, 2),
                'cess': round(emp_tds_id.cess, 2),
                'total': round(emp_tds_id.total_amount, 2),
            }
        else:
            return {
                'i_tax': 0.00,
                'surcharge': 0.00,
                'cess': 0.00,
                'total': 0.00,
            }

    def report_month(self):
        emp_tds_id = self.env['employee.tds'].search(
            [('employee_id', '=', self.employee_id.id), ('date', '=', datetime.today().replace(day=1))], limit=1)
        if emp_tds_id:
            return emp_tds_id.month
        else:
            return False

    def report_balance_payable(self):
        tds_payable = self.report_recovered_so_far()
        line_id = self.env['computed.lines'].search([('it_returns_computed', '=', self.id),
                                                     ('name', '=', 'Total Tax Payable')])
        if line_id and tds_payable:
            return round(line_id.amount_total - tds_payable.get('total'))
        else:
            return False

    def report_get_months(self):
        start = self.env.company.fiscal_year_start_date
        end = self.env.company.fiscal_year_last_date
        date_list = []
        while start < end:
            date_list.append(start)
            start += relativedelta(months=1)

        pop_list = []
        for dt in range(len(date_list)):
            if date_list[dt] < datetime.now().date():
                pop_list.append(dt)
        for pd in pop_list:
            date_list.pop(pd)
        return len(date_list)

    def PrintRoman(self, number):
        num = [1, 4, 5, 9, 10, 40, 50, 90,
               100, 400, 500, 900, 1000]
        sym = ["I", "IV", "V", "IX", "X", "XL",
               "L", "XC", "C", "CD", "D", "CM", "M"]
        i = 12
        val = ''
        while number:
            div = number // num[i]
            number %= num[i]

            while div:
                val += sym[i]
                div -= 1
            i -= 1
        return val


class GrossLines(models.Model):
    _name = 'gross.lines'

    it_return_gross = fields.Many2one('it.returns', string="It Returns")
    gross_annual_income = fields.Many2one('taxable.income', string="Gross Annual")
    amount = fields.Float("Amount")


class OtherIncomeLines(models.Model):
    _name = 'other.income.lines'

    it_return_other_income = fields.Many2one('it.returns', string="It Returns")
    other_incomes = fields.Many2one('other.income.sources', string="Other Income Sources")
    amount = fields.Float("Amount")


class TaxSection10Lines(models.Model):
    _name = 'tax.section10.lines'

    it_return_section10 = fields.Many2one('it.returns', string="It Returns")
    section_10 = fields.Many2one('tax.section10', string="Section 10")
    amount = fields.Float("Amount")
    document = fields.Binary('Document')
    file_name = fields.Char("File Name")


class TaxSection16Lines(models.Model):
    _name = 'tax.section16.lines'

    it_return_section16 = fields.Many2one('it.returns', string="It Returns")
    section_16 = fields.Many2one('tax.section16', string="Section 16")
    amount = fields.Float("Amount")

    @api.onchange('section_16')
    def onchange_section_16(self):
        if self.section_16:
            self.amount = self.section_16.limit_amount
        else:
            self.amount = 0.00


class TaxSection24Lines(models.Model):
    _name = 'tax.section24.lines'

    it_return_section24 = fields.Many2one('it.returns', string="It Returns")
    section_24 = fields.Many2one('tax.section24', string="Section 24")
    amount = fields.Float("Amount")
    max_limit = fields.Float("Max Limit")
    document = fields.Binary('Document')
    file_name = fields.Char("File Name")

    @api.onchange('section_24')
    def onchange_section_24(self):
        if self.section_24:
            self.max_limit = self.section_24.limit_amount
        else:
            self.max_limit = 0.00


class TaxSection80cLines(models.Model):
    _name = 'tax.section80c.lines'

    it_return_section80c = fields.Many2one('it.returns', string="It Returns")
    section_80c = fields.Many2one('tax.section80c', string="Section 80 C")
    amount = fields.Float("Deductible Amount")
    document = fields.Binary('Document')
    file_name = fields.Char("File Name")


class TaxChapter6Lines(models.Model):
    _name = 'tax.chapter6.lines'

    it_return_chapter6 = fields.Many2one('it.returns', string="It Returns")
    chapter6 = fields.Many2one('tax.chapter6', string="Chapter VI A")
    amount = fields.Float("Amount")
    max_limit = fields.Float("Max Limit")
    document = fields.Binary('Document')
    file_name = fields.Char("File Name")

    @api.onchange('chapter6')
    def onchange_chapter6(self):
        if self.chapter6:
            self.max_limit = self.chapter6.limit_amount
        else:
            self.max_limit = 0.00


class ComputedLines(models.Model):
    _name = 'computed.lines'

    it_returns_computed = fields.Many2one("it.returns", string="It Returns")
    name = fields.Char("Name")
    amount = fields.Float("Amount")
    amount_total = fields.Float("Total")
    color = fields.Char("Group")
