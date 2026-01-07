# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hello_world123(models.Model):
#     _name = 'hello_world123.hello_world123'
#     _description = 'hello_world123.hello_world123'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
