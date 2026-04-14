// Copyright (c) 2026, ahmed.atef and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Order s", {
	refresh(frm) {

	},
});


frappe.ui.form.on('Sales Order Item s', {
    product: function(frm, cdt, cdn){
        let row = locals[cdt][cdn];
        if (row.product){
            frappe.db.get_value('Prodcut', row.product, ['price', 'sku'], function(value){
                frappe.model.set_value(cdt, cdn, 'rate', value.price);
                frappe.model.set_value(cdt, cdn, 'product_name', value.sku);
            });
        }
    },
    // qty: function(frm, cdt, cdn){
    //     let row = locals[cdt][cdn];
    //     frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate);
    //     frm.refresh_field('total');
    // }
});