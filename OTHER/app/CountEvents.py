import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database

class CountEvents:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Count Disaster Events by Disaster Type", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for location selection
        ttk.Label(self.main_frame, text="Select Disaster Type:").grid(row=1, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_type_var)
        self.event_type_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Load locations from database
        self.load_disaster_types()

        # Buttons
        ttk.Button(self.main_frame, text="Clear", command=self.clear_ui).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Count", command=self.count_events).grid(row=2, column=1, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=3, column=0, columnspan=2, pady=10)

    def load_disaster_types(self):
        try:
            # Call fetch_all_event_types without arguments
            disaster_types = self.db.fetch_all_event_types()  
            self.event_type_dropdown['values'] = disaster_types
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def count_events(self):
        event_type = self.event_type_var.get()
        if not event_type:
            messagebox.showerror("Error", "Please select a disaster type")
            return

        try:
            count = self.db.count_disasters_by_event_type(event_type)  # Location is passed directly
            messagebox.showinfo("Event Count", f"Number of disasters of type {event_type}: {count}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch event count: {e}")

    def clear_ui(self):
        self.event_type_var.set("")

    def back_to_menu(self):
        self.controller.switch_to_menu()