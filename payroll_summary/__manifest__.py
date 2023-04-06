{
    'name' : 'Payroll Summary Reports',
    'version' : '15.0.0.1',
    'summary': 'Payroll Summary Reports',
    'sequence': 10,
    'description': """
    Payroll Summary Reports 
    """,
    'author':'Hema',
    'category': 'HR Payroll',
    'website': 'https://www.odoo.com/',
    'depends' : ['base','om_hr_payroll','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/payroll_summary.xml',
        'views/report_menu.xml',
        'report/report.xml',
    ],
    'installable': True,
    'application': True,
}
