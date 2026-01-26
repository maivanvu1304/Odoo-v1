odoo.define('warranty_management.WarrantyWidget', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');

    // Widget hiển thị trạng thái bảo hành với màu sắc
    var WarrantyStatusWidget = AbstractField.extend({
        className: 'o_warranty_status_widget',

        _renderReadonly: function () {
            var status = this.value || 'draft';
            var statusColors = {
                'draft': 'gray',
                'confirmed': 'blue',
                'in_progress': 'orange',
                'done': 'green',
                'cancelled': 'red'
            };

            this.$el.html(
                '<span class="badge" style="background-color: ' + statusColors[status] + '; color: white; padding: 5px 10px;">' +
                status.toUpperCase() +
                '</span>'
            );
        },
    });

    fieldRegistry.add('warranty_status_widget', WarrantyStatusWidget);

    return WarrantyStatusWidget;
});