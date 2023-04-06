{
    'name': 'hrmsinh',
   'version': '1.0',
   # 'emp_id': '123',
   'summary ': 'details of ABC',
   # 'email': 'abcdef@gmail.com.',
   # 'Joining date': '09/05/2022',
   'sequence': 10,
   'category': 'Productivity',
   'license':'LGPL-3',
   'depends': ['base', 'hr', 'Itax_calculation_master', 'recruitment_management','employee_self_service', ],
   'data': [
      'security/ir.model.access.csv',
      'views/hrms11.xml',
      'views/payroll.xml',
      'wizards/payroll_generate_payslip.xml',
      'wizards/income_tax_xls.xml',
      'reports/xls.xml',
   ],
   'demo': [

   ],
   'qweb': [],
   'installable ': True,
   'application': True,
   'auto_install': False,

}

