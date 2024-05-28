# Copyright (c) 2024, Mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Address(Document):
	def validate(self):
		self.set_full_address()
		frappe.msgprint('Message')
		
	
	def set_full_address(self):
		self.full_address = "abcd"
		frappe.msgprint('Message')
		
