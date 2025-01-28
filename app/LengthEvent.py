import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei

class LengthEvent:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Generate Disaster Duration", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Dropdown for length type
        ttk.Label(self.main_frame, text="Select Duration Type:").grid(row=1, column=0, padx=10, pady=10)
        self.length_type_var = tk.StringVar(value="")
        self.length_type_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.length_var,
            values=["Longest Duration", "Shortest Duration", "Average Duration"],
            state="readonly",
        )
        self.length_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.length_dropdown.bind("<<ComboboxSelected>>", self.update_length_type)

        # Dropdown for disaster type
        ttk.Label(self.main_frame, text="Select Disaster Type:").grid(row=1, column=0, padx=10, pady=10)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_type_var, state="readonly")
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_event_subtypes)

        # Dropdown for disaster subtype
        ttk.Label(self.main_frame, text="Select Disaster SubType:").grid(row=2, column=0, padx=10, pady=10)
        self.event_subtype_var = tk.StringVar(value="")
        self.event_subtype_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_subtype_var, state="readonly")
        self.event_subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Load event types into the dropdown
        self.load_event_types()

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.length_event).grid(row=4, column=0, pady=10)
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
        return event_images.get(event_type, None)

    def load_event_types(self):
        try:
            # Fetch all event types from the database
            event_types = self.db.fetch_all_event_types()
            if event_types:
                # Update the combobox
                self.event_type_dropdown['values'] = event_types
            else:
                messagebox.showerror("Error", "No event types found in the database")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load event types: {e}")

    def load_event_subtypes(self, event):
     try:
         event_type = self.event_type_var.get()
         if event_type:
             subtypes = self.db.fetch_subtypes_by_event_type(event_type)
             if subtypes:
                 self.event_subtype_dropdown['values'] = subtypes
             else:
                 self.event_subtype_dropdown['values'] = []
                 messagebox.showinfo("No Subtypes", "No subtypes found")
         else:
             self.event_subtype_dropdown['values'] = []
     except Exception as e:
         messagebox.showerror("Error", f"Failed to load subtypes: {e}")

    def length_event(self):
        event_type = self.event_type_var.get()
        if not event_type:
            messagebox.showerror("Error", "Please select an event type")
            return
        
        # Get the corresponding event image
        event_image_path = self.get_event_image(event_type)
        if not event_image_path:
            messagebox.showerror("Error", "No image available for the selected disaster type")
            return

        try:
            # Fetch the disaster count from the database
            length = self.db.fetch_length_by_event_type(event_type)
            if length is None:
                messagebox.showerror("Error", "No data available for the selected disaster type")
                return

            # Create a new window to show the image and count
            image_window = tk.Toplevel(self.master)
            image_window.title(f"Disaster Type: {event_type}")
            
            # Load and display the image
            img = Image.open(event_image_path)
            img = img.resize((400, 275), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label_image = tk.Label(image_window, image=photo)
            label_image.image = photo
            label_image.pack(padx=10, pady=10)

            # Display the count
            label_text = tk.Label(
                image_window,
                text=f"Duration of {event_type}: {length}",
                font=("Arial", 12)
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch event duration: {e}")

    def back_to_menu(self):
        self.controller.switch_to_menu()