# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class crystalline_momo_pay(models.Model):
#     _name = 'crystalline_momo_pay.crystalline_momo_pay'
#     _description = 'crystalline_momo_pay.crystalline_momo_pay'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

