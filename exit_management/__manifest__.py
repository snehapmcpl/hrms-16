# -*- coding: utf-8 -*-

{
    'name': 'HRMS - Exit Management',
    'version': '15.0.1.0 27-july',
    'summary': 'Handle the resignation process of the employee',
    'author': 'PMCL',
    'depends': ['base','hr', 'om_hr_payroll','mail','hr_work_entry'],
    'category': 'HR',
    'data': [
        'security/user_access.xml',
        'security/ir.model.access.csv',
        'data/hr_settlement_sequence.xml',
        'wizard/resignation_request_view.xml',
        # 'views/hr_employee.xml',
        'views/hr_leave_type.xml',
        'views/resignation_view.xml',
        'views/notice_period_view.xml',
        'views/res_company_view.xml',
        'reports/reports.xml',
        'reports/settlement_slip.xml',
        'reports/relieving_letter.xml',
        'reports/exp_letter.xml',
        'reports/handover_form.xml',

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
