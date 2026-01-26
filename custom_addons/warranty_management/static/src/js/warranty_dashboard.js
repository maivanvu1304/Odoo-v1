odoo.define('warranty_management.WarrantyDashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var WarrantyDashboard = AbstractAction.extend({
        template: 'WarrantyDashboard',

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._loadDashboardData();
            });
        },

        _loadDashboardData: function () {
            var self = this;
            rpc.query({
                model: 'warranty.ticket',
                method: 'get_dashboard_data',  // Custom method trong Python model
                args: [],
            }).then(function (data) {
                self._renderDashboard(data);
            });
        },

        _renderDashboard: function (data) {
            this.$('.total_tickets').text(data.total_tickets || 0);
            this.$('.pending_tickets').text(data.pending_tickets || 0);
            this.$('.completed_tickets').text(data.completed_tickets || 0);

            // Vẽ chart nếu cần
            this._renderChart(data.chart_data);
        },

        _renderChart: function (chartData) {
            // Sử dụng Chart.js hoặc thư viện khác
            console.log('Chart data:', chartData);
        },
    });

    core.action_registry.add('warranty_dashboard', WarrantyDashboard);

    return WarrantyDashboard;
});