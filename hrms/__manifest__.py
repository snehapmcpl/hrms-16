{
    'name': 'hrms1',
   'version': '1.0',
   # 'emp_id': '123',
   'summary ': 'details of ABC',
   # 'email': 'abcdef@gmail.com.',
   # 'Joining date': '09/05/2022',
   'sequence': 10,
   'category': 'Productivity',
   'license':'LGPL-3',
   'depends': ['base', 'hr', 'Itax_calculation_master', 'recruitment_management', 'om_hr_payroll',],
   'data': [
      'security/ir.model.access.csv',
      # 'data/salary_rule_add.xml',
      'views/empsalarybreakup.xml',
      'views/salary_rule_inherit.xml',
      'views/pf_and_esi_settings.xml',
   ],
   'demo': [

   ],
   'qweb': [],
   'installable ': True,
   'application': True,
   'auto_install': False,

}

