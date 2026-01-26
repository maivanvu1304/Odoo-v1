from odoo import http
from odoo.http import request

class WarrantyController(http.Controller):
    
    @http.route('/warranty/tickets', type='http', auth='user', website=True)
    def warranty_tickets_list(self, **kw):
        """Hiển thị danh sách warranty tickets"""
        tickets = request.env['warranty.ticket'].search([])
        return request.render('warranty_management.ticket_list_template', {
            'tickets': tickets
        })
    
    @http.route('/warranty/ticket/<int:ticket_id>', type='http', auth='user', website=True)
    def warranty_ticket_detail(self, ticket_id, **kw):
        """Hiển thị chi tiết một warranty ticket"""
        ticket = request.env['warranty.ticket'].browse(ticket_id)
        return request.render('warranty_management.ticket_detail_template', {
            'ticket': ticket
        })
    
    @http.route('/warranty/create', type='json', auth='user', methods=['POST'])
    def create_warranty_ticket(self, **kw):
        """API tạo warranty ticket mới"""
        ticket = request.env['warranty.ticket'].create({
            'name': kw.get('name'),
            'customer_id': kw.get('customer_id'),
            'product_id': kw.get('product_id'),
        })
        return {'success': True, 'ticket_id': ticket.id}