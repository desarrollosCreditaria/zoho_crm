# -*- coding: utf-8 -*-
# from odoo import http


# class Zoho(http.Controller):
#     @http.route('/zoho/zoho/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zoho/zoho/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('zoho.listing', {
#             'root': '/zoho/zoho',
#             'objects': http.request.env['zoho.zoho'].search([]),
#         })

#     @http.route('/zoho/zoho/objects/<model("zoho.zoho"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zoho.object', {
#             'object': obj
#         })
