# -*- coding: utf-8 -*-
{
    'name': "Zoho CRM",

    'summary': """
        Modulo para comunicarse con la plataforma zoho""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Creditaria",
    'website': "https://creditaria.online/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
            'direcciones','contacts_extend','base'
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/file_security.xml',

        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
