# -*- coding: utf-8 -*-
{
    'name': "Rest API - HRMS Prime",

    'summary': """
        Rest API developed for MobileApp integrations""",

    'description': """
         
    """,

    'author': "Prime Minds Consulting Private Limited",
    'website': "http://www.primeminds.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
