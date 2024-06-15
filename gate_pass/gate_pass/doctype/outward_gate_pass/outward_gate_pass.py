import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
class OutwardGatePass(Document):
    def before_save(self):
        self.send_outward_gate_to_stock_entry()
        # self.set_invoice_number()
        
    # def before_validate(self):
    #     self.invoice()
			
	# 	def invoice(self):
	# 		frappe.msgprint('testing')
	# 		self.invoice_no = self.name
	# 		frappe.errprint(self.invoice_no)
	# 		a = frappe.db.set_value('Courier Gate Pass', self.name, 'invoice_no	', self.invoice_no)
	# 		frappe.db.commit()
	# 		frappe.errprint(a)
			# frappe.db.set_value('Courier Gate Pass', self.name, 'invoice_no', "10") # issue with this line this has not set the invoice no to the docuemnt number
			# frappe.errprint("checking.........")
			# frappe.db.commit()
        

    # def set_invoice_number(self):
        # frappe.msgprint('20')
        # self.invoice_no = self.name
        # self.name = self.invoice_no
        # self.invoice_no = self.name
        # frappe.errprint(self.invoice_no)
        # frappe.msgprint(a)
        # frappe.db.set_value('Courier Gate Pass', self.name, 'invoice_no', "10") # issue with this line this has not set the invoice no to the docuemnt number
        # frappe.errprint(a)
        # frappe.db.commit()
        # frappe.errprint("hello 👌")
        # b = frappe.db.set_value('Courier Gate Pass', self.name, self.invoice_no , self.invoice_no) # issue with this line this has not set the invoice no to the docuemnt number
		# frappe.msgprint("a")
  
    def send_outward_gate_to_stock_entry(self):
        gate_pass = self

        if gate_pass.ogp_type == "Inventory" and gate_pass.type == "Returnable" and gate_pass.workflow.state == "Pending Return":
            stock_entry_items = []
            for item in gate_pass.inventory_gate_pass:
                stock_entry_items.append({
                    'item_code': item.item,
                    'qty': item.qty,
                    's_warehouse': item.s_warehouse,
                    't_warehouse': item.t_warehouse
                })
            
            stock_entry = frappe.get_doc({
                'doctype': 'Stock Entry',
                'purpose': 'Material Transfer',
                'posting_date': gate_pass.creation_date,
                'stock_entry_type': 'Material Transfer',
                'items': stock_entry_items
            })
            
            stock_entry.insert(ignore_permissions=True)
            stock_entry.save()
            # stock_entry.submit()
            
            frappe.msgprint(f"Stock Entry has been created: {stock_entry.name}")
        
        elif gate_pass.ogp_type == "Inventory" and gate_pass.type == "Non-Returnable" and gate_pass.workflow.state == "Pending Return":
            stock_entry_items = []
            for item in gate_pass.inventory_gate_pass:
                stock_entry_items.append({
                    'item_code': item.item,
                    'qty': item.qty,
                    's_warehouse': item.s_warehouse,
                    't_warehouse': item.t_warehouse
                })
                
            stock_entry = frappe.get_doc({
                'doctype': 'Stock Entry',
                'purpose': 'Material Issue',
                'posting_date': gate_pass.creation_date,
                'stock_entry_type': 'Material Issue',
                'items': stock_entry_items
            })
            
            stock_entry.insert(ignore_permissions=True)
            stock_entry.save()
            # stock_entry.submit()
            
            frappe.msgprint(f"Stock Entry has been created: {stock_entry.name}")
