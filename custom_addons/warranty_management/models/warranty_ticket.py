from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WarrantyTicket(models.Model):
    _name = "warranty.ticket"
    _description = "Warranty Ticket Record"

    name = fields.Char(string="Ticket Number", required=True)
    customer_id = fields.Many2one("res.partner", string="Customer")
    phone = fields.Char(string="Phone")
    product_id = fields.Many2one("product.product", string="Product")
    serial_no = fields.Char(string="Serial Number", _check_serial_no_len=True)
    purchase_date = fields.Date(string="Purchase Date")
    warranty_months = fields.Integer(string="Warranty Months")
    expire_date = fields.Date(string="Expire Date")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
    )
    # One2many: 1 ticket có nhiều line
    line_ids = fields.One2many(
        "warranty.ticket.line",
        "ticket_id",
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

    @api.constrains("serial_no")
    def _check_serial_no_len(self):
        for rec in self:
            if rec.serial_no and len(rec.serial_no.strip()) < 5:
                raise ValidationError("Serial Number phải có ít nhất 5 ký tự")
    @api.constrains("purchase_date")
    def _check_warranty_months_positive(self):
        for rec in self:
            if rec.purchase_date < fields.Date.today():
                raise ValidationError("Purchase Date không được trước ngày hiện tại")
    @api.constrains("warranty_months")
    def _check_warranty_months_positive(self):
        for rec in self:
            if rec.warranty_months < 0:
                raise ValidationError("Warranty Months phải >= 0")