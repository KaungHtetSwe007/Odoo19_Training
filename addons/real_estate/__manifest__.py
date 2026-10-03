{
    'name': "Real Estate",
    'summary': "This is the real estate",
    'description': """ Real Estate""",
    'category': 'Accounting/Accounting',
    'version': '19.0.0',
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': True,
    'author': 'Odoo KHS',
    'license': 'LGPL-3',
}
