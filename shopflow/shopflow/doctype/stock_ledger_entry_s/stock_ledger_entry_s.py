# Copyright (c) 2026, ahmed.atef and contributors
# For license information, please see license.txt
from aiohttp.payload import Order
import frappe
from frappe.model.document import Document
from frappe.query_builder import DocType, Order
from frappe.query_builder.functions import Coalesce, Sum

class StockLedgerEntrys(Document):
    pass


def get_stock_balance(product):
    sle = DocType("Stock Ledger Entry s")

    result = (
        frappe.qb.from_(sle)
        .select(Coalesce(Sum(sle.qty_change), 0).as_("balance"))
        .where(sle.product == product)
        .run(as_dict=True)
    )



    return (result[0].get("balance") or 0) if result else 0


@frappe.whitelist()
def get_all_stock_balances():
    sle = DocType("Stock Ledger Entry s")

    query = (
        frappe.qb.from_(sle)
        .select(
            sle.product,
            Sum(sle.qty_change).as_("balance")
        )
        .groupby(sle.product)
        .orderby(sle.product, order=Order.asc)
    )

    return query.run(as_dict=True)