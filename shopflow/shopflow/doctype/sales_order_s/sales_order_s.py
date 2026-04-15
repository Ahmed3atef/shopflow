# Copyright (c) 2026, ahmed.atef and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from shopflow.shopflow.doctype.stock_ledger_entry_s.stock_ledger_entry_s import get_stock_balance


class SalesOrders(Document):
	
	def validate(self):
		self.calculate_total()
		self.validate_stock()
  
	def on_submit(self):
		self.db_set("status", "Confirmed")
		self.create_store_ledger_entries()
		frappe.msgprint(
			f"Sales Order {self.name} has been confirmed.",
			title="Order Confirmed",
			indicator="green"
		)

	def on_cancel(self):
		self.db_set("status", "Cancelled")
		self.reverse_stock_ledger_entries()
		frappe.msgprint(
			f"Sales Order {self.name} has been cancelled.",
			title="Order Cancelled",
			indicator="red"
		)
  
	def calculate_total(self):
		total = 0
		for item in self.items:
			if not item.qty or not item.rate:
				continue
			item.amount = item.qty * item.rate
			total += item.amount
		self.total = total
  
	def validate_stock(self):
		for item in self.items:
			available = get_stock_balance(item.product)
			if item.qty > available:
				frappe.throw(
					f"Insufficient stock for {item.product}. "
                    f"Requested: {item.qty}, Available: {available}"
				)

	def create_store_ledger_entries(self):
		for item in self.items:
			sle = frappe.get_doc({
				"doctype": "Stock Ledger Entry s",
                "product": item.product,
                "qty_change": -item.qty,        # negative = stock going out
                "posting_date": self.order_date,
                "voucher_type": "Sales Order s",
                "voucher_no": self.name,
                "remarks": f"Stock deducted on order confirmation"
			})
			sle.insert(ignore_permissions=True)

	def reverse_stock_ledger_entries(self):
		for item in self.items:
			sle = frappe.get_doc({
				"doctype": "Stock Ledger Entry s",
                "product": item.product,
                "qty_change": item.qty,         # positive = stock coming back
                "posting_date": self.order_date,
                "voucher_type": "Sales Order s",
                "voucher_no": self.name,
                "remarks": f"Stock reversed on order cancellation"
			})
			sle.insert(ignore_permissions=True)
