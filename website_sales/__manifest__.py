# -*- coding: utf-8 -*-
{
    'name': "eCommerce CSTM",

    'author': "Benchmarkitsolutions",
    'website': "http://www.benchmarkitsolutions.com",


    'sequence': 59,
    'category': 'e-commerce',
    'version': '1.0',
    'depends': ['website_sale'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        # 'data/website_data.xml',
    ],
    'installable': True,
    'application': True,
}
