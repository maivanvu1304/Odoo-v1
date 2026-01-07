from odoo import models, fields

class HelloWorld(models.Model):
    _name = "hello.world"
    _description = "Hello World Record"

    name = fields.Char(string="Name", required=True)
    note = fields.Text(string="Note")
    active = fields.Boolean(default=True)
