// Copyright (c) 2026, ahmed.atef and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Sales Summary"] = {
	"filters": [
		{
			fieldname: 'from_date',
			label: 'From Date',
			fieldtype: 'Date',
			default: frappe.datetime.month_start(),
			reqd:1
		},
		{
			fieldname: 'to_date',
			label: 'To Date',
			fieldtype: 'Date',
			default: frappe.datetime.now_date(),
			reqd: 1
		}

	]
};
