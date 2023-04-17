# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Interview Form',
    'version': '0.1',
    'summary': 'Recruitment form',
    'sequence': 10,
    'description': """ """,
    'category': 'Recruitmenting',
    'depends': ['recruitment_management', 'hr'],
    'data': [
        'views/emp_details.xml',
        'views/view_interview_form.xml',
        '',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
