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
        ttk.Label(self.main_frame, text="Main Menu", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20)
        )

        # Radio buttons for selecting options
        self.selected_option = tk.StringVar(value="none")
        ttk.Radiobutton(
            self.main_frame, text="Search For Disasters by Year", variable=self.selected_option, value="search"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)

        ttk.Radiobutton(
            self.main_frame, text="Generate Disaster Count by Location", variable=self.selected_option, value="count"
        ).grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # Buttons
        ttk.Button(self.main_frame, text="Go", command=self.go).grid(
            row=4, column=0, pady=10
        )
        ttk.Button(self.main_frame, text="Exit", command=self.exit).grid(
            row=4, column=1, pady=10
        )

    def go(self):
        selected_option = self.selected_option.get()

        if selected_option == "search":
            self.controller.switch_to_search()
        elif selected_option == "count":
            self.controller.switch_to_count()
        else:
            messagebox.showerror("Error", "Please select an action")

    def exit(self):
        self.controller.master.quit()