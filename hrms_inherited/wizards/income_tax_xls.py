from odoo import api, fields, models
import time
from datetime import datetime


class IncomeTaxWizard(models.TransientModel):
    _name = "income.tax.wizard"
    _description = "Income Tax Wizard"

    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")

    def generate_xlsx_report(self):
        it_obj = self.env['it.returns'].search(
            ['&', ('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)])

        print(it_obj, "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        it_list = []
        for it_return in it_obj:
            it_list.append(it_return.id)
        data = {
            'data': it_list
        }
        # print(":::::::::::::::")
        return self.env.ref('hrms_inherited.income_tax_xlx').report_action(self, data=data)
