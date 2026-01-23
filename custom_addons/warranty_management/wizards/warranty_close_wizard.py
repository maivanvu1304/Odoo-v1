# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WarrantyCloseWizard(models.TransientModel):
    _name = 'warranty.close.wizard'
    _description = 'Warranty Close Wizard'

    ticket_id = fields.Many2one(
        'warranty.ticket',
        string='Warranty Ticket',
        required=True,
        readonly=True
    )
    close_reason = fields.Selection([
        ('resolved', 'Resolved - Issue Fixed'),
        ('replaced', 'Product Replaced'),
        ('refunded', 'Refunded'),
        ('expired', 'Warranty Expired'),
        ('rejected', 'Claim Rejected'),
        ('other', 'Other')
    ], string='Close Reason', required=True, default='resolved')
    
    notes = fields.Text(string='Notes', required=True, help='Describe the resolution or reason for closing')
    close_date = fields.Date(string='Close Date', default=fields.Date.today, required=True)
    
    @api.model
    def default_get(self, fields_list):
        """Get default values from context"""
        res = super().default_get(fields_list)
        # Lấy ticket_id từ context
        if self.env.context.get('default_ticket_id'):
            res['ticket_id'] = self.env.context.get('default_ticket_id')
        return res
    
    def action_close_ticket(self):
        """Close the warranty ticket with reason and notes"""
        self.ensure_one()
        
        if not self.ticket_id:
            raise UserError(_('No ticket selected to close.'))
        
        # Kiểm tra trạng thái ticket
        if self.ticket_id.state == 'done':
            raise UserError(_('This ticket is already closed.'))
        
        if self.ticket_id.state == 'cancel':
            raise UserError(_('Cannot close a cancelled ticket.'))
        
        # Cập nhật ticket
        self.ticket_id.write({
            'state': 'done',
        })
        
        # Thêm ghi chú vào chatter
        close_reason_label = dict(self._fields['close_reason'].selection).get(self.close_reason)
        message = _(
            "<b>Ticket Closed</b><br/>"
            "<b>Reason:</b> %s<br/>"
            "<b>Close Date:</b> %s<br/>"
            "<b>Notes:</b><br/>%s"
        ) % (close_reason_label, self.close_date, self.notes or '')
        
        self.ticket_id.message_post(
            body=message,
            subject=_('Ticket Closed'),
            message_type='notification'
        )
        
        return {'type': 'ir.actions.act_window_close'}
