import frappe
from frappe.model.document import Document

class CourierGatePass(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        frappe.msgprint("Message: Courier Gate Pass created!")  # Informative message

    def set_dimensions(self):  # Use plural for consistency
        """
        This function adds rows to the 'dimensions' child table based on the
        value of the 'no_of_packages' field.
        """

        # Validate no_of_packages (optional, adapt as needed)
        if not isinstance(self.no_of_packages, int) or self.no_of_packages <= 0:
            frappe.throw(_("Number of packages must be a positive integer."))

        # Clear existing rows (optional, comment out if you want to keep existing data)
        # self.set("dimensions", [])

        # Add new rows based on the number of packages
        for i in range(self.no_of_packages):
            new_row = self.append("dimensions")  # Use append for child table rows

            # Set default values for child table fields (optional)
            # new_row.set_value("field_name", "default_value")

        # Save the document (optional if automatic saving is enabled)
        # self.save()

        frappe.msgprint(f"Message: Added {self.no_of_packages} rows to 'dimensions'!")  # Informative message
