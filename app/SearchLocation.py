import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database
import InputValidation as v

class SearchLocation:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Search For Disasters by Location", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Label and input field
        ttk.Label(self.main_frame, text="Location:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.location_entry = ttk.Entry(self.main_frame)
        self.location_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Frame for displaying the results
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.grid(row=3, column=0, columnspan=3, pady=20, sticky="nsew")

        # Add a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical")
        self.results_list = tk.Text(self.results_frame, wrap="word", yscrollcommand=self.scrollbar.set, height=15, width=50)
        self.scrollbar.config(command=self.results_list.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.results_list.pack(side="left", fill="both", expand=True)

        # Buttons
        ttk.Button(self.main_frame, text="Clear", command=self.clear_ui).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Search", command=self.search_location).grid(row=4, column=1, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=2, pady=10)

    def clear_ui(self):
        # Clears the input fields
        self.location_entry.delete(0, tk.END)
        self.results_list.delete(1.0, tk.END)

    def search_location(self):
        # Performs a search for disasters
        location_name = self.location_entry.get()

        # Validate input
        if not location_name:
            messagebox.showerror("Error", "Please enter a location name.")
            return

        try:
            # Clear previous search
            self.results_list.delete(1.0, tk.END)

            # Search for disasters
            results = self.db.search_location(location_name)

            if results:
                for event in results:
                    # Format each disaster event
                    event_str = "\n".join([f"{key}: {value}" for key, value in event.items()])
                    self.results_list.insert(tk.END, f"{event_str}\n{'-'*40}\n")
            else:
                # If no results found, inform the user
                self.results_list.insert(tk.END, "No disasters found for the given location.")
        except Exception as e:
            # Handle error if search fails
            messagebox.showerror("Error", f"Failed to search: {e}")

    def back_to_menu(self):
        """Handles navigation back to the main menu."""
        self.controller.switch_to_menu()