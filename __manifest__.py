# -*- coding: utf-8 -*-
{
    'name': 'Mirgor Test',
    'summary': "Odoo module for Mirgor Test",
    'description': """""",
    'author': 'Santiago Apel',
    'website': "",
    "support": "",
    'category': "",
    'version': '15.0.0.1.0',
    'depends': ['sale_management', "stock", "account"],
    'data': [
        'security/ir.model.access.csv',
        'reports/credit_report.xml',
        'wizards/credit_group_wizard.xml',
        'views/sale_channel_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'views/sale_credit_group_views.xml',
    ],
    'license': "OPL-1",
    'auto_install': False,
    'installable': True,
    #'images': ['static/description/logo.png'],
    'pre_init_hook': 'pre_init_check',
}
