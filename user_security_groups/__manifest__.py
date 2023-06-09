{
    'name': 'User Security Groups',
    'summary': """New access security groups are added in this module""",
    'version': '15.0.0.1 10-june',
    'description': """New access security groups are added in this module""",
    'author': 'PMCS',
    "license": "AGPL-3",
    'sequence': 10,
    'company': 'prime minds consulting pvt ltd',
    'website': 'http://www.primeminds.com',
    'category': 'Tools',
    'depends': ['base', 'hr', 'user_access','hr_recruitment'],
    'data': [
        'security/user_security_groups.xml',
        'security/ir.model.access.csv',
        'views/view_user.xml',
        'views/views_security.xml',
        # 'data/access.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
