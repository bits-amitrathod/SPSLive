# -*- coding: utf-8 -*-
{
    'name': "Prioritization Engine",

    'summary': """
        Prioritization Engine""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Benchmark It Solutions",
    'website': "http://www.benchmarkitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly





    'depends': ['base','product','product_brand','sale_management','stock','web_one2many_selectable','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/saleorder_views.xml',
        'views/report_invoice.xml',
        'views/prioritization_views.xml',
        'views/web_assets.xml',
        'views/templates.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto-install': True,
    'installable': True,
}
