# -*- coding: utf-8 -*-
{
    'name': "crystalline_momo_pay",
    'author': "Crystalline Wealth SMC Limited",
    'version': '0.1',
    'depends': ['point_of_sale', 'payment'],
    'application': False,
        'assets': {
        'point_of_sale._assets_pos': [
            'crystalline_momo_pay/static/src/js/*',
            'crystalline_momo_pay/static/src/js/PopUp/*',
            'crystalline_momo_pay/static/src/xml/pos_momo_payment_button.xml',
            'crystalline_momo_pay/static/src/xml/momo_pop_up.xml',
            'crystalline_momo_pay/static/src/xml/pos_product_screen_button.xml',
            'crystalline_momo_pay/static/src/xml/pos_pop_up.xml',
        ]
    },
    'data': [
        'security/ir.model.access.csv', 
        'views/momo_menu.xml',
        'views/momo_transactions_view.xml',
        'views/momo_credentials_view.xml', 
        'views/momo_payment.xml',      
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

