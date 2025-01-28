import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei

class DestructiveEvent:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Calculate Disaster Damages", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for destructiveness type
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


        # Dropdown for disaster type
        ttk.Label(self.main_frame, text="Select Event Type:").grid(row=2, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_type_var)
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Dropdown for disaster subtype
        ttk.Label(self.main_frame, text="Select Disaster Subtype:").grid(row=3, column=0, padx=10, pady=5)
        self.event_subtype_var = tk.StringVar(value="")
        self.event_subtype_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_subtype_var)
        self.event_subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Load locations and types from database
        self.load_event_types()
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_event_subtypes)

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.destructive_event).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=1, pady=10)

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

    def load_event_types(self):
        try:
            disaster_types = self.db.fetch_all_event_types()
            if disaster_types:
                self.event_type_dropdown['values'] = disaster_types
            else:
                messagebox.showwarning("No Data", "No event types found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def load_event_subtypes(self):
        try:
            event_type = self.event_type_var.get()
            if event_type:
                subtypes = self.db.fetch_subtypes_by_event_type(event_type)
                self.event_subtype_dropdown['values'] = subtypes
            else:
                self.event_subtype_dropdown['values'] = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subtypes: {e}")

    def update_destructiveness_type(self):
        """Handle updates when the deadliness type is selected."""
        selected_type = self.destructiveness_var.get()
        print(f"Selected deadliness type: {selected_type}")

    def update_subtypes(self):
        """Update the subtype dropdown based on the selected event type."""
        event_type = self.event_type_var.get()
        destructiveness_type = self.destructiveness_var.get()
        event_subtype = self.subtype_var.get()

        if not event_type or not destructiveness_type or not event_subtype:
            messagebox.showerror("Error", "Please select disaster type, deadliness type, and subtype.")
            return

        try:
            subtypes = self.db.fetch_subtypes_by_event_type(event_type)
            self.subtype_dropdown["values"] = subtypes
            self.subtype_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subtypes: {e}")

    def destructive_event(self):
        event_type = self.event_type_var.get()
        destructiveness_type = self.destructiveness_var.get()
        event_subtype = self.event_subtype_var.get()

        if not event_type:
            messagebox.showerror("Error", "Please select a disaster type")
            return

        # Get the corresponding event image
        event_image_path = self.get_event_image(event_type)
        if not event_image_path:
            messagebox.showerror("Error", "No image available for the selected disaster type")
            return

        try:
            # Fetch destructiveness based on the destructiveness type selected
            if destructiveness_type == "Most Destructive":
                fatalities = self.db.fetch_max_damages_by_event_type(event_type)
                damage_description = "most destructive"
            elif destructiveness_type == "Least Destructive":
                fatalities = self.db.fetch_min_damages_by_event_type(event_type)
                damage_description = "least destructive"
            else:
                fatalities = self.db.fetch_avg_damages_by_event_type(event_type)
                damage_description = "average destructiveness"

            # Fetch the disaster damages from the database
            damages = self.db.fetch_damage_by_event_type(event_type)

            # Create a new window to show the image and damages
            image_window = tk.Toplevel(self.master)
            image_window.title(f"Disaster Type: {event_type}")

            # Load and display the image
            img = Image.open(event_image_path)
            img = img.resize((400, 275), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label_image = tk.Label(image_window, image=photo)
            label_image.image = photo
            label_image.pack(padx=10, pady=10)

            # Display the damages and destructiveness type
            label_text = tk.Label(
                image_window,
                text=f"{event_type} ({event_subtype}): {damage_description.capitalize()} with damages totaling {damages} US dollars and {fatalities} fatalities.",
                font=("Arial", 12)
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch damages: {e}")

    def back_to_menu(self):
        self.controller.switch_to_menu()