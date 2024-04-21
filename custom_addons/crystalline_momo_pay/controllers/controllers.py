# -*- coding: utf-8 -*-
# from odoo import http


# class CrystallineMomoPay(http.Controller):
#     @http.route('/crystalline_momo_pay/crystalline_momo_pay', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crystalline_momo_pay/crystalline_momo_pay/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crystalline_momo_pay.listing', {
#             'root': '/crystalline_momo_pay/crystalline_momo_pay',
#             'objects': http.request.env['crystalline_momo_pay.crystalline_momo_pay'].search([]),
#         })

#     @http.route('/crystalline_momo_pay/crystalline_momo_pay/objects/<model("crystalline_momo_pay.crystalline_momo_pay"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crystalline_momo_pay.object', {
#             'object': obj
#         })


# from odoo import http
# from odoo.http import request

# class MomoPaymentController(http.Controller):

#     @http.route('/payment/momo/webhook', type='http', auth='public', csrf=False)
#     def momo_webhook(self, **kwargs):
#         data = request.jsonrequest
#         transaction_id = data.get('transactionId')
#         status = data.get('status')
#         if transaction_id and status:
#             transaction = request.env['momo.transaction'].sudo().search([('momo_transaction_id', '=', transaction_id)], limit=1)
#             if transaction:
#                 if status == 'SUCCESSFUL':
#                     transaction.write({'state': 'success'})
#                 elif status in ('FAILED', 'CANCELLED'):
#                     transaction.write({'state': 'failed'})
#         return 'OK'
    
#     @http.route('/payment/momo/initiate', type='json', auth='public', methods=['POST'], csrf=False)
#     def initiate_momo_payment(self, **kwargs):
#         # Extract data from the request
#         amount = kwargs.get('amount')
#         currency = kwargs.get('currency')
#         reference = kwargs.get('reference')
#         phone_number = kwargs.get('phone_number')
#         payer_message = kwargs.get('payer_message')

#         # Here, you would typically call a method to initiate the payment process
#         # For example, calling a method from your custom payment acquirer model
#         response = request.env['custom.payment.acquirer.momo'].momo_pay(amount, currency, reference, phone_number, payer_message)

#         return response

