import tkinter as tk
from tkinter import ttk, messagebox


class Splash:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        ttk.Label(
            self.main_frame,
            text="Welcome to the 2000s Disaster Information App",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(
            self.main_frame,
            text="Looking back we had some pretty great natural disasters...",
            font=("Arial", 10),
        ).grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # Load and display the image
        self.image = self.image = tk.PhotoImage(file=r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\app\resources\splash.png")
        self.image_label = tk.Label(self.main_frame, image=self.image)
        self.image_label.grid(row=2, column=0, columnspan=2, pady=(0, 20))

        # "Main Menu" button
        ttk.Button(
            self.main_frame, text="Learn More", command=self.menu
        ).grid(row=3, column=0, pady=10)

        # "Exit" button
        ttk.Button(
            self.main_frame, text="Exit", command=self.exit
        ).grid(row=3, column=1, pady=10)

    def menu(self):
        # Switch to the main menu
        self.controller.switch_to_menu()

    def exit(self):
        # Exit the application
        self.controller.master.quit()
