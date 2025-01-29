# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei

class CountEvent:
    def __init__(self, master, controller):
        # Initialize the class
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create the main frame for the view
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create and place the title label
        self.title_label = ttk.Label(
            self.main_frame, text="Generate Disaster Count", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Create and configure the dropdown for disaster type selection
        ttk.Label(self.main_frame, text="Select Disaster Type:").grid(row=1, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_type_var, state="readonly"
        )
        self.event_type_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_disaster_subtypes)

        # Create and configure the dropdown for disaster subtype selection
        ttk.Label(self.main_frame, text="Select Disaster Subtype:").grid(row=2, column=0, padx=10, pady=5)
        self.event_subtype_var = tk.StringVar(value="")
        self.event_subtype_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_subtype_var, state="readonly"
        )
        self.event_subtype_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Load disaster types
        self.load_disaster_types()

        # Add buttons for generating the count and returning to the menu
        ttk.Button(self.main_frame, text="Generate", command=self.count_events).grid(row=3, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=3, column=1, pady=10)

    # Return the image path for a given disaster type
    def get_event_image(self, event_type):
        """Returns the appropriate image path for the given event type."""
        event_images = {
            "Flood": ei.flood_image(),
            "Wildfire": ei.fire_image(),
            "Earthquake": ei.earthquake_image(),
            "Volcanic activity": ei.volcano_image(),
            "Storm": ei.storm_image(),
            "Drought": ei.drought_image(),
            "Extreme temperature": ei.extreme_temp_image(),
            "Epidemic": ei.epidemic_image(),
            "Mass movement (wet)": ei.mass_movement_image(),
        }
        return event_images.get(event_type)

    # Load disaster types from the database
    def load_disaster_types(self):
        try:
            disaster_types = self.db.fetch_all_event_types()
            self.event_type_dropdown["values"] = disaster_types
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    # Load disaster subtypes based on the selected type
    def load_disaster_subtypes(self, event):
        event_type = self.event_type_var.get()
        if not event_type:
            self.event_subtype_dropdown["values"] = []
            return

        try:
            subtypes = self.db.fetch_subtypes_by_event_type(event_type)
            self.event_subtype_dropdown["values"] = subtypes
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster subtypes: {e}")

    # Generate the count of disasters
    def count_events(self):
        event_type = self.event_type_var.get()
        event_subtype = self.event_subtype_var.get()

        if not event_type:
            messagebox.showerror("Error", "Please select a disaster type")
            return

        try:
            # Fetch disaster count from the database
            count = self.db.count_disasters_by_event_type_and_subtype(event_type, event_subtype)
            event_image_path = self.get_event_image(event_type)

            # Display the disaster count and image
            image_window = tk.Toplevel(self.master)
            image_window.title(f"Disaster Type: {event_type}")

            # Load and display the image
            if event_image_path:
                img = Image.open(event_image_path)
                img = img.resize((400, 275), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                label_image = tk.Label(image_window, image=photo)
                label_image.image = photo
                label_image.pack(padx=10, pady=10)

            # Display the disaster count
            label_text = tk.Label(
                image_window,
                text=f"{event_subtype}: Number of disasters is {count}",
                font=("Arial", 12),
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch event count: {e}")

    # Method to navigate back to the main menu
    def back_to_menu(self):
        self.controller.switch_to_menu()