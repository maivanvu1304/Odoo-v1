# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WarrantyReportWizard(models.TransientModel):
    _name = 'warranty.report.wizard'
    _description = 'Warranty Report Wizard'

    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True, default=fields.Date.today)
    
    partner_id = fields.Many2one('warranty.partner', string='Customer')
    product_id = fields.Many2one('product.product', string='Product')
    
    state = fields.Selection([
        ('all', 'All'),
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status Filter', default='all')
    
    warranty_level = fields.Selection([
        ('all', 'All'),
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ], string='Warranty Level', default='all')
    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        """Validate date range"""
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise UserError(_('From Date must be before To Date.'))
    
    def action_generate_report(self):
        """Generate warranty report based on filters"""
        self.ensure_one()
        
        # Build domain for search
        domain = [
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
        ]
        
        # Add optional filters
        if self.partner_id:
            domain.append(('customer_id', '=', self.partner_id.id))
        
        if self.product_id:
            domain.append(('product_id', '=', self.product_id.id))
        
        if self.state != 'all':
            domain.append(('state', '=', self.state))
        
        if self.warranty_level != 'all':
            domain.append(('warranty_level', '=', self.warranty_level))
        
        # Search for tickets
        tickets = self.env['warranty.ticket'].search(domain, order='create_date desc')
        
        if not tickets:
            raise UserError(_('No warranty tickets found with the selected filters.'))
        
        # Generate PDF report
        return self.env.ref('warranty_management.action_report_warranty_ticket').report_action(tickets)
    
    def action_view_tickets(self):
        """Open tree view of filtered tickets"""
        self.ensure_one()
        
        # Build domain for search
        domain = [
            ('create_date', '>=', self.date_from),
            ('create_date', '<=', self.date_to),
        ]
        
        if self.partner_id:
            domain.append(('customer_id', '=', self.partner_id.id))
        
        if self.product_id:
            domain.append(('product_id', '=', self.product_id.id))
        
        if self.state != 'all':
            domain.append(('state', '=', self.state))
        
        if self.warranty_level != 'all':
            domain.append(('warranty_level', '=', self.warranty_level))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Filtered Warranty Tickets'),
            'res_model': 'warranty.ticket',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': {'create': False},
        }
