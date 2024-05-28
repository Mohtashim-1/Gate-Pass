# Copyright (c) 2024, Mohtashim and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Address(Document):
	def before_save(self):
		self.set_full_address()
	
	def set_full_address(self):
		self.full_address = "abcd"
