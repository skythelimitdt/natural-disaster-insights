from tkinter import ttk, messagebox, StringVar
from Database import Database

class DestructiveEvent:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Calculate Disaster Damages", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for disaster type
        ttk.Label(self.main_frame, text="Select Event Type:").grid(row=1, column=0, padx=10, pady=5)
        self.event_type_var = StringVar(value="")
        self.destructive_event_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_type_var)
        self.destructive_event_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Load locations from database
        self.load_destructive_event()

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.destructive_event).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=2, column=1, columnspan=2, pady=10)

    def load_destructive_event(self):
        try:
            disaster_types = self.db.fetch_all_event_types()
            self.destructive_event_dropdown['values'] = disaster_types
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")
            
    def destructive_event(self):
        event_type = self.event_type_var.get()
        if not event_type:
            messagebox.showerror("Error", "Please select a disaster type")
            return

        try:
            damages = self.db.fetch_damage_by_event_type(event_type)
            messagebox.showinfo("Damages", f"Total damages for {event_type}: {damages}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch damages: {e}")

    def clear_ui(self):
        self.location_var.set("")

    def back_to_menu(self):
        self.controller.switch_to_menu()