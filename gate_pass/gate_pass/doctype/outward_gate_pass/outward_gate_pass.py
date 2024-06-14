import frappe
from frappe.model.document import Document

class OutwardGatePass(Document):
    def before_save(self):
        self.send_outward_gate_to_stock_entry()

    def send_outward_gate_to_stock_entry(self):
        gate_pass = self

        if gate_pass.ogp_type == "Inventory" and gate_pass.type == "Returnable":
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
                'posting_date': gate_pass.posting_date,  # Ensure posting_date exists
                'stock_entry_type': 'Material Transfer',
                'items': stock_entry_items
            })
            
            stock_entry.insert(ignore_permissions=True)
            stock_entry.save()
            # stock_entry.submit()
            
            frappe.msgprint(f"Stock Entry has been created: {stock_entry.name}")
        
        elif gate_pass.ogp_type == "Inventory" and gate_pass.type == "Non-Returnable":
            stock_entry_items = []
            for item in gate_pass.inventory_gate_pass:
                stock_entry_items.append({
                    'item_code': item.item,
                    'qty': item.qty,
                    's_warehouse': item.s_warehouse,
                    # 't_warehouse': item.t_warehouse
                })
                
            stock_entry = frappe.get_doc({
                'doctype': 'Stock Entry',
                'purpose': 'Material Issue',
                'posting_date': gate_pass.creation_date,  # Ensure posting_date exists
                'stock_entry_type': 'Material Issue',
                'items': stock_entry_items
            })
            
            stock_entry.insert(ignore_permissions=True)
            stock_entry.save()
            # stock_entry.submit()
            
            frappe.msgprint(f"Stock Entry has been created: {stock_entry.name}")
