# Copyright (c) 2026, ahmed.atef and contributors
# For license information, please see license.txt

import frappe


def execute(
	filters: dict | None = None,
) -> tuple[list[dict], list[dict], str | None, dict | None]:
	filters = filters or {}
	columns = get_column()
	data = get_data_qb(filters)
	chart = get_chart(data)
	return columns, data, None, chart


def get_column() -> list[dict]:
	return [
		{"label": "Order Date", "fieldname": "order_date", "fieldtype": "Date", "width": 120},
		{
			"label": "Number of Orders",
			"fieldname": "order_count",
			"fieldtype": "Int",
			"width": 140,
		},
		{
			"label": "Total Sales",
			"fieldname": "total_sales",
			"fieldtype": "Currency",
			"width": 140,
		},
	]


def get_data_sql(filters: dict) -> list[dict]:
	conditions = "WHERE docstatus = 1"

	if filters.get("from_date"):
		conditions += " AND order_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND order_date <= %(to_date)s"

	return frappe.db.sql(
		f"""
        SELECT
            order_date,
            COUNT(name) AS order_count,
            SUM(total)  AS total_sales
        FROM
            `tabSales Order s`
        {conditions}
        GROUP BY
            order_date
        ORDER BY
            order_date ASC
        """,
		filters,
		as_dict=True,
	)


def get_data_qb(filters: dict) -> list[dict]:
	from frappe.query_builder.functions import Count, Sum

	SO = frappe.qb.DocType("Sales Order s")

	query = (
		frappe.qb.from_(SO)
		.select(
			SO.order_date,
			Count(SO.name).as_("order_count"),
			Sum(SO.total).as_("total_sales"),
		)
		.where(SO.docstatus == 1)
		.groupby(SO.order_date)
		.orderby(SO.order_date)
	)

	if filters.get("from_date"):
		query = query.where(SO.order_date >= filters.get("from_date"))
	if filters.get("to_date"):
		query = query.where(SO.order_date <= filters.get("to_date"))

	return query.run(as_dict=True)


def get_chart(data: list[dict]) -> dict | None:
	if not data:
		return None

	return {
		"data": {
			"labels": [str(row.order_date) for row in data],
			"datasets": [{"name": "Total Sales", "values": [row.total_sales for row in data]}],
		},
		"type": "pie",
		"fieldtype": "Currency",
	}
