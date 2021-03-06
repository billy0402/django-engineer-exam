window.onload = function () {
    (function ($) {
        const role = $('#id_role');
        const customer = $('#customer-group');
        const employee = $('#employee-group');

        updateCustomer(role.val());
        updateEmployee(role.val());

        role.on('change', function () {
            const role = this.value;
            updateCustomer(role);
            updateEmployee(role);
        })

        function updateCustomer(role) {
            if (role === 'customer') {
                customer.show();
            } else {
                customer.hide();
            }
        }

        function updateEmployee(role) {
            if (role === 'employee' || role === 'manager') {
                employee.show();
            } else {
                employee.hide();
            }
        }
    })(django.jQuery);
}
