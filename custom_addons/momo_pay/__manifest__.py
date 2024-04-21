# -*- coding: utf-8 -*-
{
    'name': "momo_pay",
    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'payment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # 'momo_pay/static/src/js/*',
            # 'momo_pay/static/src/xml/pos_custom_button.xml',
        ]
    },
    # only loaded in demonstration mode
    'dAppsemo': [
        'demo/demo.xml',
    ],
}

