from odoo import models
import xlsxwriter
from odoo import api, models, fields


class IncomeTaxXLS(models.AbstractModel):
    _name = 'report.hrms_inherited.report_it_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        sheet = workbook.add_worksheet('Income tax')
        format_2 = workbook.add_format({'bold': True, 'align': 'center', 'text_wrap': True})
        format_1 = workbook.add_format({'align': 'center', 'text_wrap': True})


        row = 0
        col = 0
        sheet.write(row, col, 'ID No', format_2)
        sheet.write(row, col + 1, 'Name', format_2)
        sheet.write(row, col + 2, 'PAN', format_2)
        sheet.write(row, col + 3, 'Basic Salary', format_2)
        sheet.write(row, col + 4, 'HRA ', format_2)
        sheet.write(row, col + 5, 'Standard Deduction', format_2)
        sheet.write(row, col + 6, 'LTA', format_2)
        sheet.write(row, col + 7, 'Special Allowance', format_2)
        sheet.write(row, col + 8, 'Total Gross Salary', format_2)
        sheet.write(row, col + 9, 'House Rent Allowance under section 10(13A)', format_2)
        sheet.write(row, col + 10, 'Total amount of exemption claimed under section 10', format_2)
        sheet.write(row, col + 11, 'Total amount of salary received from current employer', format_2)
        sheet.write(row, col + 12, 'Standard deduction under section 16(ia)', format_2)
        sheet.write(row, col + 13, 'Tax on employment under section 16(iii)', format_2)
        sheet.write(row, col + 14, 'Total amount of deductions under section 16', format_2)
        sheet.write(row, col + 15, 'Income chargeable under the head "Salaries"', format_2)
        sheet.write(row, col + 16, 'Income (or admissible loss) from house property reported by employee offered for TDS', format_2)
        # sheet.write(row, col + 17, 'Less: Deduction under Chapter VI A', format_2)
        sheet.write(row, col + 17, 'Deduction Under Section 80C', format_2)
        sheet.write(row, col + 18, 'Aggregate of deductible amount under Chapter VI-A', format_2)
        sheet.write(row, col + 19, 'Total taxable income', format_2)
        sheet.write(row, col + 20, 'Total Tax Payable', format_2)
        sheet.write(row, col + 21, 'Rebate under section 87A, if applicable', format_2)
        sheet.write(row, col + 22, 'Surcharge, wherever applicable', format_2)
        sheet.write(row, col + 23, 'Health and education cess', format_2)
        sheet.write(row, col + 24, 'Tax payable', format_2)
        sheet.write(row, col + 25, 'Less: Relief under section 89', format_2)
        sheet.write(row, col + 26, 'Net tax payable', format_2)


        # sheet.write(row, 28, 'Total', format_2)
        sheet.set_column(0, 28, 15)
        sheet.set_row(0, 65)
        # print(data, "data=====================================")
        # tax_obj = self.env['it.returns'].search([data])
        tax_data = data.get('data')
        for tax_val in tax_data:
            tax_obj = self.env['it.returns'].search([('id', '=', tax_val)])
            print(tax_obj)
            for tax in tax_obj:
                col = 0

                row += 1
                sheet.write(row, col, tax.employee_code, format_1)
                sheet.write(row, col + 1, tax.employee_id.name, format_1)
                sheet.write(row, col + 2, tax.pan_no, format_1)

                inc = []
                ded = []
                basic1 = []
                hra1 = []
                standard_deduction1 = []
                lta1 = []
                spl_alw1 = []
                tot_gross_sal1 = []
                house_rent1 = []
                section_101 = []
                tot_cur_emp1 = []
                standard_deduction_161 = []
                tax_sec_161 = []
                tol_amt_sec_161 = []
                inc_cha_head1 = []
                aggregate_under_ch_61 = []
                tot_tax_inc1 = []
                tot_tax_pay1 = []
                rebate_under_871 = []
                surcharge1 = []
                health1 = []
                tax_payable1 = []
                less_sec_891 = []
                net_tax_pay1 = []

                basic = hra = standard_deduction = lta = 0
                spl_alw = tot_gross_sal = house_rent = section_10 = 0
                tot_cur_emp = standard_deduction_16 = tax_sec_16 = 0
                tol_amt_sec_16 = inc_cha_head = aggregate_under_ch_6 = tot_tax_inc = 0
                tot_tax_pay = rebate_under_87 = surcharge = health = tax_payable = 0
                inc_for_tds = ded_under_80 = less_sec_89 = net_tax_pay = 0

                for line in tax.computed_line_ids:
                    if line.name == 'Basic Salary':
                        basic = line.amount_total
                    if line.name == 'HRA':
                        hra = line.amount_total
                    if line.name == 'Standard Deduction':
                        standard_deduction = line.amount_total
                    if line.name == 'LTA':
                        lta = line.amount_total
                    if line.name == 'Special Allowance':
                        spl_alw = line.amount_total
                    if line.name == 'Total Gross Salary':
                        tot_gross_sal = line.amount_total
                    if line.name == 'House Rent Allowance under section 10(13A)':
                        house_rent = line.amount_total
                    if line.name == 'Total amount of exemption claimed under section 10':
                        section_10 = line.amount_total
                    if line.name == 'Total amount of salary received from current employer':
                        tot_cur_emp = line.amount_total
                    if line.name == 'Standard deduction under section 16(ia)':
                        standard_deduction_16 = line.amount_total
                    if line.name == 'Tax on employment under section 16(iii)':
                        tax_sec_16 = line.amount_total
                    if line.name == 'Total amount of deductions under section 16':
                        tol_amt_sec_16 = line.amount_total
                    if line.name == 'Income chargeable under the head "Salaries"':
                        inc_cha_head = line.amount_total
                    if line.name == 'Income (or admissible loss) from house property reported by employee offered for TDS':
                        inc_for_tds = line.amount_total
                    # if line.name == 'Deduction under Chapter VI A':
                    #     ded_under_chap_6 = line.amount_total
                    if line.name == 'Deduction Under Section 80C':
                        ded_under_80 = line.amount_total
                    if line.name == 'Aggregate of deductible amount under Chapter VI-A':
                        aggregate_under_ch_6 = line.amount_total
                    if line.name == 'Total taxable income':
                        tot_tax_inc = line.amount_total
                    if line.name == 'Total Tax Payable':
                        tot_tax_pay = line.amount_total
                    if line.name == 'Rebate under section 87A, if applicable':
                        rebate_under_87 = line.amount_total
                    if line.name == 'Surcharge, wherever applicable':
                        surcharge = line.amount_total
                    if line.name == 'Health and education cess':
                        health = line.amount_total
                    if line.name == 'Tax payable':
                        tax_payable = line.amount_total
                    if line.name == 'Less: Relief under section 89':
                        less_sec_89 = line.amount_total
                    if line.name == 'Net tax payable':
                        net_tax_pay = line.amount_total
                    # if line.name == 'Net Tax Payable':
                    #     net_tax_pay2 = line.amount_total



                inc.append(inc_for_tds)
                ded.append(ded_under_80)
                basic1.append(basic)
                hra1.append(hra)
                standard_deduction1.append(standard_deduction)
                lta1.append(lta)
                spl_alw1.append(spl_alw)
                tot_gross_sal1.append(tot_gross_sal)
                house_rent1.append(house_rent)
                section_101.append(section_10)
                tot_cur_emp1.append(tot_cur_emp)
                standard_deduction_161.append(standard_deduction_16)
                tax_sec_161.append(tax_sec_16)
                tol_amt_sec_161.append(tol_amt_sec_16)
                inc_cha_head1.append(inc_cha_head)
                aggregate_under_ch_61.append(aggregate_under_ch_6)
                tot_tax_inc1.append(tot_tax_inc)
                tot_tax_pay1.append(tot_tax_pay)
                rebate_under_871.append(rebate_under_87)
                surcharge1.append(surcharge)
                health1.append(health)
                tax_payable1.append(tax_payable)
                less_sec_891.append(less_sec_89)
                net_tax_pay1.append(net_tax_pay)


                sheet.write(row, 3, basic)
                sheet.write(row, 4, hra)
                sheet.write(row, 5, standard_deduction)
                sheet.write(row, 6, lta)
                sheet.write(row, 7, spl_alw)
                sheet.write(row, 8, tot_gross_sal)
                sheet.write(row, 9, house_rent)
                sheet.write(row, 10, section_10)
                sheet.write(row, 11, tot_cur_emp)
                sheet.write(row, 12, standard_deduction_16)
                sheet.write(row, 13, tax_sec_16)
                sheet.write(row, 14, tol_amt_sec_16)
                sheet.write(row, 15, inc_cha_head)
                sheet.write(row, 16, inc_for_tds)
                # sheet.write(row, 17, ded_under_chap_6)
                sheet.write(row, 17, ded_under_80)
                sheet.write(row, 18, aggregate_under_ch_6)
                sheet.write(row, 19, tot_tax_inc)
                sheet.write(row, 20, tot_tax_pay)
                sheet.write(row, 21, rebate_under_87)
                sheet.write(row, 22, surcharge)
                sheet.write(row, 23, health)
                sheet.write(row, 24, tax_payable)
                sheet.write(row, 25, less_sec_89)
                sheet.write(row, 26, net_tax_pay)
                # row += 1





                # col = 2
                # for line in tax.computed_line_ids:
                #     col += 1
                #     sheet.write(row, col, line.amount, format_1)

            # col = 2
            # for lines in tax.computed_line_ids:
            #     col += 1
            #     sheet.write(0, col, lines.name, format_2)
