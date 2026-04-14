# Copyright (c) 2026, ahmed.atef and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesOrders(Document):
	
	def validate(self):
		self.calculate_total()
		self.validate_stock()
  
  
	def calculate_total(self):
		total = 0
		for item in self.items:
			if not item.qty or not item.rate:
				continue
			item.amount = item.qty + item.rate
			total += item.amount
		self.total = total
  
	def validate_stock(self):
		for item in self.items:
			available = frappe.db.get_value("Product", item.product, "stock_qty") or 0
			if item.qty > available:
				frappe.throw(
					f"Insufficient stock for {item.product}. "
                    f"Requested: {item.qty}, Available: {available}"
				)
