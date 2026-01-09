from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelloWorld(models.Model):
    _name = "hello.world"
    _description = "Hello World Record"

    name = fields.Char(string="Name", required=True)
    note = fields.Text(string="Note")
    active = fields.Boolean(default=True)

    # One2many: 1 world có nhiều line
    line_ids = fields.One2many(
        "hello.world.line",
        "world_id",
        string="Lines",
    )

    # Computed field: đếm số lines
    line_count = fields.Integer(
        string="Line Count",
        compute="_compute_line_count",
        store=True,
    )

    @api.depends("line_ids")
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.line_ids)

    # Constraint ví dụ: Name tối thiểu 3 ký tự
    @api.constrains("name")
    def _check_name_len(self):
        for rec in self:
            if rec.name and len(rec.name.strip()) < 3:
                raise ValidationError("Name phải có ít nhất 3 ký tự")
