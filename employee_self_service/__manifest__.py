{
    'name': 'Employee Self Services',
    'summary': """This module allows a employee to access his/her own records in employee and income tax related records""",
    'version': '15.0.0.2 10-june',
    'description': """This module allows a employee to access his/her own records in employee and income tax related records""",
    'author': 'PMCS',
    "license": "AGPL-3",
    'sequence': 10,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Accounting, Tools',
    'depends': ['base', 'hr', 'Itax_calculation_master', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'data/odoo_bot.xml',
        'views/employee_tax.xml',
        'views/hr_payslip.xml',
        'views/hr_employee.xml',
        'views/hr_holidays.xml',
    ],
    "assets": {
        "web.assets_common": [
            "employee_self_service/static/src/js/base_view.js",
        ],
        'web.assets_qweb': [
            'employee_self_service/static/src/components/*/*.xml',
            'employee_self_service/static/src/webclient/user_menu/user_menu.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
