from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Splash:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        # Create the main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        ttk.Label(
            self.main_frame,
            text="Welcome to the Natural Disaster Information App",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Subtitle label
        ttk.Label(
            self.main_frame,
            text="Explore the 600+ Natural Disasters of the 21st Century. Click Below to Learn More!",
            font=("Arial", 10),
        ).grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # Try to load and resize the splash image
        try:
            # Attempt to load the image
            og_image = Image.open(r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\images\splash.png")
            resize_image = og_image.resize((550, 325), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(resize_image)
            
            # Display the resized image
            self.image_label = tk.Label(self.main_frame, image=self.image)
            self.image_label.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 10))
        except Exception as e:
            # Handle the error if the image cannot be loaded
            messagebox.showwarning("Image Error", f"Failed to load splash image: {e}")
            
            # Provide a fallback if image cant be loaded
            self.image_label = ttk.Label(self.main_frame, text="Image failed to load.")
            self.image_label.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 10))

        # Learn More button
        ttk.Button(
            self.main_frame, text="Learn More", command=self.menu
        ).grid(row=3, column=0, pady=5)

        # Exit button
        ttk.Button(
            self.main_frame, text="Exit", command=self.exit
        ).grid(row=3, column=1, pady=5)

    def menu(self):
        # Switch to the main menu
        self.controller.switch_to_menu()

    def exit(self):
        # Exit the application
        self.controller.master.quit()