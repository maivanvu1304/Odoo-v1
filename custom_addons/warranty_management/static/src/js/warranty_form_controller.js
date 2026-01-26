odoo.define('warranty_management.WarrantyFormController', function (require) {
    'use strict';

    var FormController = require('web.FormController');
    var viewRegistry = require('web.view_registry');
    var FormView = require('web.FormView');

    var WarrantyFormController = FormController.extend({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            warranty_button_clicked: '_onWarrantyButtonClicked',
        }),

        _onWarrantyButtonClicked: function (event) {
            var self = this;
            var record_id = this.handle;

            this._rpc({
                model: 'warranty.ticket',
                method: 'custom_action',
                args: [[this.modelName === 'warranty.ticket' ?
                    parseInt(this.handle.res_id) : null]],
            }).then(function (result) {
                self.do_notify('Success', 'Action completed!');
                self.reload();
            });
        },

        // Override method save
        saveRecord: function () {
            console.log('Saving warranty ticket...');
            return this._super.apply(this, arguments).then(function () {
                console.log('Ticket saved successfully!');
            });
        },
    });

    var WarrantyFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: WarrantyFormController,
        }),
    });

    viewRegistry.add('warranty_form', WarrantyFormView);
});