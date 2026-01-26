odoo.define('warranty_management.portal', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');

    publicWidget.registry.WarrantyPortal = publicWidget.Widget.extend({
        selector: '.warranty_portal_form',
        events: {
            'submit': '_onSubmitForm',
            'click .load_ticket_details': '_onLoadTicketDetails',
        },

        _onSubmitForm: function (ev) {
            ev.preventDefault();
            var formData = {
                'name': this.$('input[name="name"]').val(),
                'customer_id': this.$('select[name="customer_id"]').val(),
                'product_id': this.$('select[name="product_id"]').val(),
                'description': this.$('textarea[name="description"]').val(),
            };

            ajax.jsonRpc('/warranty/create', 'call', formData).then(function (result) {
                if (result.success) {
                    alert('Warranty ticket created!');
                    window.location.href = '/warranty/ticket/' + result.ticket_id;
                }
            });
        },

        _onLoadTicketDetails: function (ev) {
            var ticket_id = $(ev.currentTarget).data('ticket-id');
            ajax.jsonRpc('/warranty/ticket/' + ticket_id + '/json', 'call', {}).then(function (data) {
                // Display ticket details
                console.log('Ticket data:', data);
            });
        },
    });
});