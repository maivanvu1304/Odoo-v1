from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WarrantyTicketLine(models.Model):
    _name = "warranty.ticket.line"
    _description = "Warranty Ticket Line"
    _order = "sequence, id"

    ticket_id = fields.Many2one(
        "warranty.ticket",
        string="Warranty Ticket",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    description = fields.Text(string="Description")
    cost = fields.Text(string="Resolution Notes")
    technician_id = fields.Many2many(
        "res.users",
        string="Technicians",
    )

    @api.constrains("qty")
    def _check_qty_positive(self):
        for rec in self:
            if rec.qty <= 0:
                raise ValidationError("Qty phải > 0")