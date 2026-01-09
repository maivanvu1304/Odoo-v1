from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelloLine(models.Model):
    _name = "hello.world.line"
    _description = "Hello World Line"
    _order = "sequence, id"

    world_id = fields.Many2one(
        "hello.world",
        string="Hello World",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    qty = fields.Integer(default=1)

    @api.constrains("qty")
    def _check_qty_positive(self):
        for rec in self:
            if rec.qty <= 0:
                raise ValidationError("Qty phải > 0")
