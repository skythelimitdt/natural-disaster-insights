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
            self.main_frame, text="Filter Data", variable=self.selected_option, value="filter"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Buttons
        ttk.Button(self.main_frame, text="Go", command=self.go).grid(
            row=2, column=0, pady=10
        )
        ttk.Button(self.main_frame, text="Exit", command=self.exit).grid(
            row=2, column=1, pady=10
        )

    def go(self):
        selected_option = self.selected_option.get()

        if selected_option == "filter":
            self.controller.switch_to_filter()
        else:
            messagebox.showerror("Error", "Please select an action")

    def exit(self):
        # Closes the program when the 'Exit' button is pressed
        self.controller.master.quit()