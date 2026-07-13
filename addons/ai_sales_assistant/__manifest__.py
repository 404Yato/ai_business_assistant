# -*- coding: utf-8 -*-
{
    'name': "AI Business Assistant",

    'summary': "Integración de IA para asistir procesos comerciales en Odoo.",

    'description': """
Módulo de ejemplo que integra IA generativa con Odoo para analizar oportunidades comerciales,
generar resúmenes y asistir en la toma de decisiones.
""",

    'author': "Cristian Tapia Suárez",
    'website': "https://github.com/404Yato",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'installable': True,

    'application': True,
}

