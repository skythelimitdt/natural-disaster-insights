import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei


class DeadlyEvent:
    def __init__(self, master, controller):
        # Initialize the DeadlyEvent class
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create the main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Add the title label
        self.title_label = ttk.Label(
            self.main_frame, text="Calculate Disaster Fatalities", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for selecting deadliness type
        ttk.Label(self.main_frame, text="Select Deadliness Type:").grid(row=1, column=0, padx=10, pady=5)
        self.deadliness_var = tk.StringVar(value="")
        self.deadliness_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.deadliness_var,
            values=["Highest Death Toll", "Lowest Death Toll", "Average Death Toll"],
            state="readonly",
        )
        self.deadliness_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.deadliness_dropdown.bind("<<ComboboxSelected>>", self.update_deadliness_type)

        # Dropdown for selecting disaster type
        ttk.Label(self.main_frame, text="Select Event Type:").grid(row=2, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_type_var, state="readonly"
        )
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.update_subtypes)

        # Dropdown for selecting disaster subtype
        ttk.Label(self.main_frame, text="Select Disaster SubType:").grid(row=3, column=0, padx=10, pady=5)
        self.subtype_var = tk.StringVar(value="")
        self.subtype_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.subtype_var, state="readonly"
        )
        self.subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.deadly_event).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=1, pady=10)

        # Load the disaster types
        self.load_deadly_events()

    def get_event_image(self, event_type):
        # Returns image path for the given event type
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
        return event_images.get(event_type, None)

    def load_deadly_events(self):
        # Populate the dropdown
        try:
            disaster_types = self.db.fetch_all_event_types()
            self.event_type_dropdown["values"] = disaster_types
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def update_deadliness_type(self, event=None):
        # Handle deadliness type updates
        selected_type = self.deadliness_var.get()
        print(f"Selected deadliness type: {selected_type}")

    def update_subtypes(self, event=None):
        # Update the subtype dropdown
        event_type = self.event_type_var.get()
        if not event_type:
            self.subtype_dropdown["values"] = []
            return

        try:
            subtypes = self.db.fetch_subtypes_by_event_type(event_type)
            self.subtype_dropdown["values"] = subtypes
            self.subtype_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subtypes: {e}")

    def deadly_event(self):
        # Generate a report
        event_type = self.event_type_var.get()
        deadliness_type = self.deadliness_var.get()
        event_subtype = self.subtype_var.get()
        
        if not event_type or not deadliness_type or not event_subtype:
            messagebox.showerror("Error", "Please select disaster type, deadliness type, and subtype.")
            return

        # Fetch the image for the selected disaster type
        event_image_path = self.get_event_image(event_type)
        if not event_image_path:
            messagebox.showerror("Error", "No image available for the selected disaster type")
            return

        try:
            # Fetch fatalities data
            if deadliness_type == "Highest Death Toll":
                fatalities = self.db.fetch_max_fatalities_by_event_type(event_type)
                death_description = "highest death toll"
            elif deadliness_type == "Lowest Death Toll":
                fatalities = self.db.fetch_min_fatalities_by_event_type(event_type)
                death_description = "lowest death toll"
            else:
                fatalities = self.db.fetch_avg_fatalities_by_event_type(event_type)
                death_description = "average death toll"

            # Round fatalities
            fatalities = round(fatalities)

            # Create a new window
            image_window = tk.Toplevel(self.master)
            image_window.title(f"Disaster Type: {event_type}")

            # Display the image
            img = Image.open(event_image_path)
            img = img.resize((400, 275), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label_image = tk.Label(image_window, image=photo)
            label_image.image = photo
            label_image.pack(padx=10, pady=10)

            # Display the fatalities count
            label_text = tk.Label(
                image_window,
                text=f"{event_subtype}: {death_description.capitalize()} is {fatalities} fatalities.",
                font=("Arial", 12)
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch fatalities: {e}")

    def clear_ui(self):
        # Clear all input fields
        self.event_type_var.set("")
        self.subtype_var.set("")
        self.subtype_dropdown["values"] = []

    def back_to_menu(self):
        # Navigate back to the main menu
        self.controller.switch_to_menu()