import tkinter as tk
from tkinter import ttk, messagebox
import input_validation as V


class FilterData:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Filter Disaster Info", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Parameter 1 input
        ttk.Label(self.main_frame, text="Parameter #1:").grid(
            row=1, column=0, padx=10, pady=5, sticky="e"
        )
        self.data1 = ttk.Entry(self.main_frame)
        self.data1.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Parameter 2 input
        ttk.Label(self.main_frame, text="Parameter #2:").grid(
            row=2, column=0, padx=10, pady=5, sticky="e"
        )
        self.data2 = ttk.Entry(self.main_frame)
        self.data2.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Buttons
        ttk.Button(self.main_frame, text="Clear", command=self.clear_ui).grid(
            row=3, column=0, pady=10
        )
        ttk.Button(self.main_frame, text="Filter", command=self.filter).grid(
            row=3, column=1, pady=10
        )
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(
            row=3, column=2, pady=10
        )

    def clear_ui(self):
        self.data1.delete(0, tk.END)
        self.data2.delete(0, tk.END)

    def filter(self):
        data1 = self.data1.get()
        data2 = self.data2.get()

        # Validate inputs
        data1_valid, data1_message = V.is_valid_data(data1)
        data2_valid, data2_message = V.is_valid_data(data2)

        if not data1_valid:
            messagebox.showerror("Error", data1_message)
            return

        if not data2_valid:
            messagebox.showerror("Error", data2_message)
            return

        messagebox.showinfo("Success", "Data filtered successfully!")

    def back_to_menu(self):
        self.controller.switch_to_menu()