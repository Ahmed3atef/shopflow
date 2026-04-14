# Copyright (c) 2026, ahmed.atef and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Product(Document):
	
 
	def validate(self):
		if self.price <= 0:
			frappe.throw("Price must be greater than zero.")
			return
  
	def before_save(self):
		if self.sku:
			self.sku = self.sku.upper()
   
	def after_insert(self):
		frappe.msgprint(
			f"Product {self.sku} has been added to catalog.",
			title="Product Created",
			indicator="green"
		)


@frappe.whitelist()
def get_low_stock_products(threshold=10):
    threshold = int(threshold)
    
    products = frappe.get_list(
		"Product",
		filters={"stock_qty": ["<", threshold]},
		fields=["name", "sku", "stock_qty"],
		order_by="stock_qty asc"
	)
    
    return products


@frappe.whitelist(allow_guest=True)
def get_product_catalog():
    return frappe.db.get_list(
        "Product",
        fields=["sku", "price"],
        order_by="sku asc",
        ignore_permissions=True 
    )