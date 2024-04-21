from odoo import models, fields

class MomoCredentials(models.Model):
    _name = 'momo.credentials'
    _description = 'MTN MoMo Credentials'

    api_user = fields.Char('API User', required=True)
    api_key = fields.Char('API Key', required=True)
    subscription_key = fields.Char('Subscription Key', required=True)
    environment = fields.Selection([('sandbox', 'Sandbox'), ('production', 'Production')], default='sandbox')
