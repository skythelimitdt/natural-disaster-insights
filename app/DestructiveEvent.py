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

        # Dropdown for selecting the destructiveness type
        ttk.Label(self.main_frame, text="Select Destructiveness:").grid(row=1, column=0, padx=10, pady=5)
        self.destructiveness_var = tk.StringVar(value="")
        self.destructiveness_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.destructiveness_var,
            values=["Most Destructive", "Least Destructive", "Average Destructive"],
            state="readonly",
        )
        self.destructiveness_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.destructiveness_dropdown.bind("<<ComboboxSelected>>", self.update_destructiveness_type)

        # Dropdown for selecting the disaster type
        ttk.Label(self.main_frame, text="Select Disaster Type:").grid(row=2, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_type_var, state="readonly"
        )
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.update_subtypes)


        # Dropdown for selecting the disaster subtype
        ttk.Label(self.main_frame, text="Select Disaster Subtype:").grid(row=3, column=0, padx=10, pady=5)
        self.event_subtype_var = tk.StringVar(value="")
        self.event_subtype_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_subtype_var, state="readonly"
        )
        self.event_subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Load disaster types
        self.load_event_types()
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_event_subtypes)

        # Add buttons
        ttk.Button(self.main_frame, text="Generate", command=self.destructive_event).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=1, pady=10)

    def get_event_image(self, event_type, event_subtype=None):
        # Returns image path for the given event type
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

    def load_event_types(self):
        # Populate the event type dropdown
        try:
            disaster_types = self.db.fetch_all_event_types()
            if disaster_types:
                self.event_type_dropdown['values'] = disaster_types
            else:
                messagebox.showwarning("No Data", "No event types found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def load_event_subtypes(self, event=None):
        self.event_subtype_var.set("")
        self.event_subtype_dropdown["values"] = []
        try:
            event_type = self.event_type_var.get()
            if event_type:
                subtypes = self.db.fetch_subtypes_by_event_type(event_type)
                self.event_subtype_dropdown['values'] = subtypes if subtypes else ["No subtypes available"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subtypes: {e}")

    def update_destructiveness_type(self, event=None):
        # Handle update destructiveness type
        selected_type = self.destructiveness_var.get()
        print(f"Selected destructiveness type: {selected_type}")

    def destructive_event(self):
        # Generate and display damages
        event_type = self.event_type_var.get()
        destructiveness_type = self.destructiveness_var.get()
        event_subtype = self.event_subtype_var.get()

        # Validate selections
        if not event_type:
            messagebox.showerror("Error", "Please select a disaster type")
            return
        
        if not event_subtype:
            messagebox.showerror("Error", "Please select a disaster subtype")
            return

        # Get image for the selected event type
        event_image_path = self.get_event_image(event_type, event_subtype)
        if not event_image_path:
            messagebox.showerror("Error", "No image available for the selected disaster type")
            return

        try:
            # Fetch damages information
            if destructiveness_type == "Most Destructive":
                damages = self.db.fetch_max_damages_by_event_type(event_type)
                damage_description = "highest damages"
            elif destructiveness_type == "Least Destructive":
                damages = self.db.fetch_min_damages_by_event_type(event_type)
                damage_description = "lowest damages"
            else:
                damages = self.db.fetch_avg_damages_by_event_type(event_type)
                damage_description = "average damages"

            # Format the damages
            formatted_damages = "${:,.2f}".format(damages)

            # Create a new window
            image_window = tk.Toplevel(self.master)
            image_window.title(f"Disaster Type: {event_type}")

            # Display the image
            try:
                img = Image.open(event_image_path)
                img = img.resize((400, 275), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label_image = tk.Label(image_window, image=photo)
                label_image.image = photo
                label_image.pack(padx=10, pady=10)
            except Exception as e:
                messagebox.showwarning("Image Error", f"Failed to load image: {e}")
                # Create a blank image as fallback
                fallback_image = Image.new("RGB", (400, 275), (200, 200, 200))
                fallback_photo = ImageTk.PhotoImage(fallback_image)

                label_fallback = tk.Label(image_window, image=fallback_photo, text="Image Not Available", font=("Arial", 12))
                label_fallback.image = fallback_photo
                label_fallback.pack(padx=10, pady=10)

            # Display description
            label_text = tk.Label(
                image_window,
                text=f"{event_subtype}: {damage_description.capitalize()} totaling {formatted_damages}.",
                font=("Arial", 12)
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch damages: {e}")

    def clear_ui(self):
        # Clear all input fields
        self.event_type_var.set("")
        self.subtype_var.set("")
        self.subtype_dropdown["values"] = []

    def back_to_menu(self):
        # Switch back to the main menu
        self.controller.switch_to_menu()