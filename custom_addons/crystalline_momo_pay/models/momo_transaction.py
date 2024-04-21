from odoo import models, fields

class MomoTransaction(models.Model):
    _name = 'momo.transaction'
    _description = 'MTN Mobile Money Transaction'

    created_on = fields.Datetime('Created On', readonly=True, default=fields.Datetime.now)
    reference = fields.Char('Reference', readonly=True) # Payment reference provided by you
    momo_transaction_id = fields.Char('MTN MoMo Transaction ID', readonly=True) 
    amount = fields.Float('Amount')
    currency = fields.Char('Currency')
    phone_number = fields.Char('Phone Number')
    state = fields.Selection([
        ('draft', 'Draft'), 
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], default='draft')
    x_reference_id = fields.Char(string='X-Reference-Id')