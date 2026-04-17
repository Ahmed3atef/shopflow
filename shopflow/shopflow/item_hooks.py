import frappe


def validate(doc, method):
    if doc.custom_loyalty_points and doc.custom_loyalty_points < 0:
        frappe.throw("Loyalty Points cannot be negative.")
    
    if doc.custom_loyalty_points and doc.custom_loyalty_points > 500:
        frappe.throw("Loyalty Points cannot exceed 500.")
    
    if not doc.custom_loyalty_points and doc.valuation_rate:
        doc.custom_loyalty_points = int(doc.valuation_rate / 10)
        frappe.msgprint(
            f"Loyalty points auto-set to {doc.custom_loyalty_points} based on item price.",
            indicator="blue",
            alert=True
        )