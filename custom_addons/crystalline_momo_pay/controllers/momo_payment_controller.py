from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)

class MomoPaymentController(http.Controller):

    @http.route('/payment/momo/callback', type='http', auth='public', methods=['POST'], csrf=False)
    def momo_payment_callback(self, **kwargs):
        # Extract the transaction details from the request
        transaction_details = request.jsonrequest

        # Extract specific details from the transaction_details
        amount = transaction_details.get('amount')
        currency = transaction_details.get('currency')
        status = transaction_details.get('status')
        external_id = transaction_details.get('externalId')
        financial_transaction_id = transaction_details.get('financialTransactionId')
        payer_party_id = transaction_details.get('payer', {}).get('partyId')

        # Process the transaction details as needed
        # This is a simplified example; you'll need to adapt it to your specific use case
        transaction = request.env['momo.transaction'].search([('external_id', '=', external_id)], limit=1)
        if transaction:
            # Map the JSON response fields to the MomoTransaction model fields
            transaction.write({
                'amount': amount,
                'currency': currency,
                'state': 'success' if status == 'SUCCESSFUL' else 'failed',
                'momo_transaction_id': financial_transaction_id,
                'phone_number': payer_party_id,
            })

        # Respond with a 200 status code to acknowledge receipt of the callback
        return request.make_response("OK", [('Content-Type', 'text/plain')])



    @http.route('/payment/momo/initiate', type='json', auth='public', methods=['POST'], csrf=False)
    def initiate_momo_payment(self, **kwargs):
        # Correctly parse the JSON data from the request body
        data = request.httprequest.get_json()

        # Extract data from the parsed JSON
        amount = data.get('amount')
        currency = data.get('currency')
        reference = data.get('reference')
        phone_number = data.get('phone_number')
        payer_message = data.get('payer_message')

        # Validate input data
        missing_fields = []
        if not amount:
            missing_fields.append('amount')
        if not currency:
            missing_fields.append('currency')
        if not reference:
            missing_fields.append('reference')
        if not phone_number:
            missing_fields.append('phone_number')

        if missing_fields:
            return {'error': f'Missing required payment details: {", ".join(missing_fields)}'}

        # Initiate the payment through your acquirer
        _logger.info("About to search for MTN MoMo acquirer") # Add this line
        acquirer = request.env['momo.payment'].sudo().search([('provider', '=', 'momo')], limit=1)
        if not acquirer:
            return {'error': 'MTN MoMo payment acquirer not found'}

        try:
            response = acquirer.momo_pay(amount, currency, reference, phone_number, payer_message)
            # Handle the response from your acquirer (redirect, status page, etc.)
            return response  
        except UserError as e:
            return {'error': str(e)}  
        












