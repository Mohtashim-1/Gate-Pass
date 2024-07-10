import frappe
from frappe.model.document import Document

class CourierGatePass(Document):
    def before_save(self):
        if self.docstatus == 0:
            self.set_invoice()
    
    def validate(self):
        self.send_data_to_outward_gate_pass()
        self.update_sum_in_parent()
        
    def set_invoice(self):
        self.invoice_no = self.name

        
    def send_data_to_outward_gate_pass(self):
        if self.docstatus == 1:
            outward_gate_pass_items = []    

            for item in self.courier_gate_pass_ct:
                outward_gate_pass_items.append({
                    'item': item.description_of_goods,
                    'qty': item.qty,
                    'uom': item.uom,
                })

            outward_gate_pass = frappe.get_doc({
                'doctype': 'Outward Gate Pass',
                'ogp_type': 'Non-Inventory',
                'creation_date':self.creation_date,
                'type': 'Non-Returnable',
                'out_to':self.out_to,
                'customer':self.customer,
                'supplier':self.supplier,
                'local':self.local,
                'by_hand':self.mode_of_transport,
                'document_from': 'Courier Gate Pass',
                'courier_gate_pass': self.name,
                'non_inventory': outward_gate_pass_items
            })

            outward_gate_pass.insert(ignore_permissions=True)
            outward_gate_pass.save()
            
            frappe.msgprint(f"Outward Gate Pass has been created: {outward_gate_pass.name}")
            outward_gate_pass.submit()

    def update_sum_in_parent(self):
        # Initialize sum variable
        frappe.errprint('test1')
        total_qty = 0

        # Iterate over child table items
        for item in self.dimensions:
            frappe.errprint('test')
            total_qty += item.weight  # Assuming 'qty' is the field to sum up

        # Update the parent document with the sum
        # Assuming there's a field in the parent document named 'total_qty'
        self.total_weight = total_qty

        # Optionally, print the sum or save the document if needed
        print(f"Total Quantity: {total_qty}")
        self.save()  # Uncomment if you want to save the updated document

            
