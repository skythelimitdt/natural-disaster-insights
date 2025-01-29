import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei

class DestructiveEvent:
    def __init__(self, master, controller):
        # Initialize the DestructiveEvent class
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create the main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create title label
        self.title_label = ttk.Label(
            self.main_frame, text="Calculate Disaster Damages", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for selecting destructiveness type
        ttk.Label(self.main_frame, text="Select Destructiveness Type:").grid(row=1, column=0, padx=10, pady=5)
        self.destructiveness_var = tk.StringVar(value="")
        self.destructiveness_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.destructiveness_var,
            values=["Most Destructive", "Least Destructive", "Average Destructive"],
            state="readonly",
        )
        self.destructiveness_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.destructiveness_dropdown.bind("<<ComboboxSelected>>", self.update_destructiveness_type)

        # Dropdown for selecting disaster type
        ttk.Label(self.main_frame, text="Select Event Type:").grid(row=2, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_type_var)
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Dropdown for selecting disaster subtype
        ttk.Label(self.main_frame, text="Select Disaster Subtype:").grid(row=3, column=0, padx=10, pady=5)
        self.event_subtype_var = tk.StringVar(value="")
        self.event_subtype_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_subtype_var)
        self.event_subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Load disaster types
        self.load_event_types()
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_event_subtypes)

        # Add buttons
        ttk.Button(self.main_frame, text="Generate", command=self.destructive_event).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=1, pady=10)

    def get_event_image(self, event_type, event_subtype=None):
        """Returns image path for the given event type and subtype"""
        event_images = {
            "Flood": ei.flood_image(),
            "Wildfire": ei.fire_image(),
            "Earthquake": ei.earthquake_image(),
            "Volcanic activity": ei.volcano_image(),
            "Storm": ei.storm_image(event_subtype),
            "Drought": ei.drought_image(),
            "Extreme temperature": ei.extreme_temp_image(event_subtype),
            "Epidemic": ei.epidemic_image(),
            "Mass movement (wet)": ei.mass_movement_image(event_subtype),
        }
        return event_images.get(event_type)