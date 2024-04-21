# -*- coding: utf-8 -*-
# from odoo import http


# class MomoPay(http.Controller):
#     @http.route('/momo_pay/momo_pay', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/momo_pay/momo_pay/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('momo_pay.listing', {
#             'root': '/momo_pay/momo_pay',
#             'objects': http.request.env['momo_pay.momo_pay'].search([]),
#         })

#     @http.route('/momo_pay/momo_pay/objects/<model("momo_pay.momo_pay"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('momo_pay.object', {
#             'object': obj
#         })

