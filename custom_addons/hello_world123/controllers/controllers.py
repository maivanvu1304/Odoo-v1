# -*- coding: utf-8 -*-
# from odoo import http


# class HelloWorld123(http.Controller):
#     @http.route('/hello_world123/hello_world123/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hello_world123/hello_world123/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hello_world123.listing', {
#             'root': '/hello_world123/hello_world123',
#             'objects': http.request.env['hello_world123.hello_world123'].search([]),
#         })

#     @http.route('/hello_world123/hello_world123/objects/<model("hello_world123.hello_world123"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hello_world123.object', {
#             'object': obj
#         })
