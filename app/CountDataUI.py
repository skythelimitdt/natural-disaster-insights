import tkinter as tk
from tkinter import ttk, messagebox

class CountData:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Count Disaster Events by Location", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for location selection
        ttk.Label(self.main_frame, text="Select Location:").grid(row=1, column=0, padx=10, pady=5)
        self.location_var = tk.StringVar(value="")
        self.location_dropdown = ttk.Combobox(self.main_frame, textvariable=self.location_var)
        self.location_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Load locations from database
        self.load_locations()

        # Buttons
        ttk.Button(self.main_frame, text="Clear", command=self.clear_ui).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Count", command=self.count_events).grid(row=2, column=1, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=3, column=0, columnspan=2, pady=10)

    def load_locations(self):
        try:
            locations = self.db.fetch_all_locations("disasters")  # Replace "disasters" with your table name
            self.location_dropdown['values'] = locations
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load locations: {e}")

    def count_events(self):
        location = self.location_var.get()
        if not location:
            messagebox.showerror("Error", "Please select a location")
            return

        try:
            count = self.db.count_events_by_location("disasters", location)  # Replace "disasters" with your table name
            messagebox.showinfo("Event Count", f"Number of events in {location}: {count}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch event count: {e}")

    def clear_ui(self):
        self.location_var.set("")

    def back_to_menu(self):
        self.controller.switch_to_menu()