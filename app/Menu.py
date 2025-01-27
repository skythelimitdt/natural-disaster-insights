import tkinter as tk
from tkinter import ttk, messagebox


class Menu:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        ttk.Label(self.main_frame, text="Main Menu", font=("Arial", 20, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        # Radio buttons for selecting options
        self.selected_option = tk.StringVar(value="none")

        ttk.Radiobutton(
            self.main_frame, text="Search For Disasters by Name", variable=self.selected_option, value="search_name"
        ).grid(row=1, column=0, sticky="w", padx=15, pady=10)

        ttk.Radiobutton(
            self.main_frame, text="Search For Disasters by Year", variable=self.selected_option, value="search_year"
        ).grid(row=2, column=0, sticky="w", padx=15, pady=10)

        ttk.Radiobutton(
            self.main_frame, text="Calculate Disaster Fatalities", variable=self.selected_option, value="deadly"
        ).grid(row=3, column=0, sticky="w", padx=15, pady=10)

        ttk.Radiobutton(
            self.main_frame, text="Calculate Disaster Damages", variable=self.selected_option, value="destructive"
        ).grid(row=4, column=0, sticky="w", padx=15, pady=10)

        ttk.Radiobutton(
            self.main_frame, text="Generate Disaster Duration", variable=self.selected_option, value="length"
        ).grid(row=5, column=0, sticky="w", padx=15, pady=10)

        ttk.Radiobutton(
            self.main_frame, text="Generate Disaster Count", variable=self.selected_option, value="count"
        ).grid(row=6, column=0, sticky="w", padx=15, pady=10)

        ttk.Radiobutton(
            self.main_frame, text="Generate Random Disaster", variable=self.selected_option, value="random"
        ).grid(row=7, column=0, sticky="w", padx=15, pady=10)

        # Buttons
        ttk.Button(self.main_frame, text="Go", command=self.go).grid(
            row=8, column=0, sticky="w", padx=0, pady=10
        )
        ttk.Button(self.main_frame, text="Exit", command=self.exit).grid(
            row=8, column=1, sticky="e", padx=0, pady=10
        )

    def go(self):
        selected_option = self.selected_option.get()

        if selected_option == "search_name":
            self.controller.switch_to_search_name()
        elif selected_option == "search_year":
            self.controller.switch_to_search_year()
        elif selected_option == "count":
            self.controller.switch_to_count()
        elif selected_option == "deadly":
            self.controller.switch_to_deadly()
        elif selected_option == "destructive":
            self.controller.switch_to_destructive()
        elif selected_option == "length":
            self.controller.switch_to_length()
        elif selected_option == "random":
            self.controller.switch_to_random()
        else:
            messagebox.showerror("Error", "Please select an action")

    def exit(self):
        self.controller.master.quit()