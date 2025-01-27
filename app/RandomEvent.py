from tkinter import ttk, messagebox
from Database import Database

class RandomEvent:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Generate Random Disaster", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Load locations from database
        self.load_random_event()

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.random_event).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=2, column=1, pady=10)

    def load_random_event(self):
        try:
            self.db.fetch_all_event_types()  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def random_event(self):
        try:
            random_disaster = self.db.fetch_random_disaster()
            if random_disaster and random_disaster[1]:
                messagebox.showinfo("Random Disaster", f"DisNo: {random_disaster[0]}, Disaster Type: {random_disaster[1]}")
            else:
                messagebox.showwarning("No disasters found", "No valid disaster type found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate random disaster: {e}")

    def clear_ui(self):
        self.location_var.set("")

    def back_to_menu(self):
        self.controller.switch_to_menu()