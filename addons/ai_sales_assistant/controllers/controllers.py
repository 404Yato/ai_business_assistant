# -*- coding: utf-8 -*-
# from odoo import http


# class AiSalesAssistant(http.Controller):
#     @http.route('/ai_sales_assistant/ai_sales_assistant', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ai_sales_assistant/ai_sales_assistant/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ai_sales_assistant.listing', {
#             'root': '/ai_sales_assistant/ai_sales_assistant',
#             'objects': http.request.env['ai_sales_assistant.ai_sales_assistant'].search([]),
#         })

#     @http.route('/ai_sales_assistant/ai_sales_assistant/objects/<model("ai_sales_assistant.ai_sales_assistant"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ai_sales_assistant.object', {
#             'object': obj
#         })

