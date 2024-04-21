import json
import uuid
import requests
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)

class MomoPayment(models.Model):
    _name = 'momo.payment'
    _description = 'MTN MoMo Payment Processor'
 
    provider = fields.Selection([('momo', 'MTN MoMo')], default='momo')
    environment = fields.Selection([('sandbox', 'Sandbox'), ('production', 'Production')], default='sandbox') 
    momo_credentials_id = fields.Many2one('momo.credentials', string='MTN MoMo Credentials', required=True, ondelete="cascade")

    def _get_momo_credentials(self):
        return self.momo_credentials_id

    def _get_momo_api_headers(self):
        credentials = self._get_momo_credentials()
        headers = {
            'Ocp-Apim-Subscription-Key': credentials.subscription_key,
            'Content-Type': 'application/json'  
        }

        # Authentication: Using the API key from credentials
        if credentials.api_key:  
            headers['Authorization'] = f"Basic {credentials.api_key}"  

        return headers

    def _get_momo_token(self):
        credentials = self._get_momo_credentials()
        if self.environment == 'sandbox':
            token_endpoint = 'https://sandbox.momodeveloper.mtn.com/collection/token/' 
        else:
            token_endpoint = 'https://momodeveloper.mtn.com/token'

        auth_data = base64.b64encode(f"{credentials.api_user}:{credentials.api_key}".encode()).decode() # Example for Basic Auth
        auth_headers = { 
            'Ocp-Apim-Subscription-Key': credentials.subscription_key,
            'Content-Type': 'application/json', 
            'Authorization': f"Basic {auth_data}",
        }

        try:
            response = requests.post(token_endpoint, headers=auth_headers)
            response.raise_for_status() # Check for success
            token_data = response.json()
            token = token_data.get('access_token') 
            print(f"MTN MoMo Token: {token}") # Print the token
            return token
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Failed to obtain MTN MoMo token: {e}")
            return None



    def _get_base_url(self): 
        return 'https://sandbox.momodeveloper.mtn.com/collection/' if self.environment == 'sandbox' else 'https://momodeveloper.mtn.com'


    def momo_pay(self, amount, currency, reference, phone_number, payer_message):
        base_url = self._get_base_url()
        request_url = f"{base_url}/v1_0/requesttopay" 
        credentials = self._get_momo_credentials()
        environment = self.environment

        # Generate a new UUID for the X-Reference-Id
        x_reference_id = str(uuid.uuid4())

        headers = {
            'X-Reference-Id': x_reference_id, # Use the generated UUID here
            'X-Target-Environment': environment,
            'Ocp-Apim-Subscription-Key': credentials.subscription_key,
            'Content-Type': 'application/json',  
            'X-Callback-Url': 'http://localhost:8085/payment/momo/callback',
        }

        # Fetch token if required
        token = self._get_momo_token()  
                
        headers['Authorization'] = f"Bearer {token}" 

        payload = {
            'amount': str(amount), # Ensure correct formatting
            'currency': currency,
            'externalId': reference or str(uuid.uuid4()), # Generate reference if not provided 
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': phone_number
            },
            'payerMessage': payer_message,
            'payeeNote': payer_message
        }

        response = requests.post(request_url, headers=headers, json=payload)
        # Log the response content
        logging.debug(f"Response content: {response.content}")
        response_data = {"response": response.status_code, "ref": reference}
  
        if response.status_code == 202:
            transaction_vals = {
                'reference': reference,
                'momo_transaction_id': response_data.get('transactionId'),
                'amount': amount,
                'currency': currency,
                'phone_number': phone_number,
                'state': 'pending',
                'x_reference_id': x_reference_id,
                
            }
            self.env['momo.transaction'].create(transaction_vals)
        else:
            _logger.error(f"Payment request failed! Status code: {response.status_code}, Details: {response.text}")
            raise UserError(("Payment request failed! Details: %s") % response.text)
    
       
    def check_transaction_status(self, reference_id):
        # Find the transaction record by reference_id
        transaction = self.env['momo.transaction'].search([('reference', '=', reference_id)], limit=1)
        if not transaction:
            _logger.error(f"Transaction with reference {reference_id} not found.")
            return None

        x_reference_id = transaction.x_reference_id
        if not x_reference_id:
            _logger.error(f"X-Reference-Id not found for transaction {reference_id}.")
            return None

        # Retrieve MTN MoMo credentials and token
        credentials = self._get_momo_credentials()
        token = self._get_momo_token()
        if token is None:
            _logger.error("MTN MoMo token is not available. Cannot check transaction status.")
            return None

        # Prepare headers for the API request
        headers = {
            'Authorization': f"Bearer {token}",
            'X-Target-Environment': self.environment,
        }

        # Construct the request URL
        request_url = f"{self._get_base_url()}/v1_0/requesttopay/{x_reference_id}"

        # Make the GET request to the MTN MoMo API
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status() # Check for success
            transaction_status = response.json()
            _logger.info(f"Transaction Status for {reference_id}: {transaction_status}")
            return transaction_status
        except requests.exceptions.HTTPError as e:
            _logger.error(f"Failed to get transaction status: {e}")
            return None


