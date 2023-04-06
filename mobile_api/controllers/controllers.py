# -*- coding: utf-8 -*-
# from odoo import http


# class MobileApi(http.Controller):
#     @http.route('/mobile_api/mobile_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mobile_api/mobile_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mobile_api.listing', {
#             'root': '/mobile_api/mobile_api',
#             'objects': http.request.env['mobile_api.mobile_api'].search([]),
#         })

#     @http.route('/mobile_api/mobile_api/objects/<model("mobile_api.mobile_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mobile_api.object', {
#             'object': obj
#         })
