import tkinter as tk
from tkinter import ttk, messagebox


class FilterData:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Filter Disaster Info", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Parameter 1 input
        ttk.Label(self.main_frame, text="Column:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.column_entry = ttk.Entry(self.main_frame)
        self.column_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Parameter 2 input
        ttk.Label(self.main_frame, text="Value:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.value_entry = ttk.Entry(self.main_frame)
        self.value_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Buttons
        ttk.Button(self.main_frame, text="Clear", command=self.clear_ui).grid(row=3, column=0, pady=10)
        ttk.Button(self.main_frame, text="Filter", command=self.filter_data).grid(row=3, column=1, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=3, column=2, pady=10)

    def clear_ui(self):
        self.column_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def filter_data(self):
        column = self.column_entry.get()
        value = self.value_entry.get()

        if not column or not value:
            messagebox.showerror("Error", "Please provide both column and value")
            return

        try:
            results = self.db.filter_data("disasters", column, value)  # Replace "disasters" with your table name
            messagebox.showinfo("Filtered Results", str(results))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter data: {e}")

    def back_to_menu(self):
        self.controller.switch_to_menu()