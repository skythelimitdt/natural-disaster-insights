import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database
import InputValidation as v

class SearchYear:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create the main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Search For Disasters by Year", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Label and input fields
        ttk.Label(self.main_frame, text="Year:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.year_entry = ttk.Entry(self.main_frame)
        self.year_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Frame to display the search results
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
        ttk.Button(self.main_frame, text="Search", command=self.search_year).grid(row=4, column=1, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=2, pady=10)

    def clear_ui(self):
        # Clears the input field
        self.year_entry.delete(0, tk.END)
        self.results_list.delete(1.0, tk.END)

    def search_year(self):
        # Performs a search for disasters
        year = self.year_entry.get()

        # Validate year integer
        try:
            year_int = int(year)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year.")  # Show error if the year is not an integer
            return
        
        # Validate entered year
        if year_int < v.START_YEAR or year_int > v.END_YEAR:
            messagebox.showerror("Error", f"Year must be between {v.START_YEAR} and {v.END_YEAR}.")  # Show error for out-of-range year
            return

        try:
            # Fetch disaster data
            results = self.db.search_year(year_int)
            self.results_list.delete(1.0, tk.END) 

            # Display the results
            if results:
                for event in results:
                    event_str = "\n".join([f"{key}: {value}" for key, value in event.items()])  # Format each event as a string
                    self.results_list.insert(tk.END, f"{event_str}\n{'-'*40}\n")
            else:
                self.results_list.insert(tk.END, "No disasters found for the given year")
        except Exception as e:
            # Handle error if search fails
            messagebox.showerror("Error", f"Failed to search: {e}")

    def back_to_menu(self):
        #Handles navigation back to menu
        self.controller.switch_to_menu()