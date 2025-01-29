import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei
import traceback

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

        # Dropdown to select the type of duration
        ttk.Label(self.main_frame, text="Select Duration:").grid(row=1, column=0, padx=10, pady=10)
        self.length_type_var = tk.StringVar(value="")
        self.length_type_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.length_type_var,
            values=["Longest Duration", "Shortest Duration", "Average Duration"],
            state="readonly",
        )
        self.length_type_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.length_type_dropdown.bind("<<ComboboxSelected>>", self.update_length_type)

        # Dropdown to select disaster type
        ttk.Label(self.main_frame, text="Select Disaster Type:").grid(row=2, column=0, padx=10, pady=10)
        self.event_type_var = tk.StringVar(value="")
        self.event_type_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_type_var, state="readonly")
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_event_subtypes)

        # Dropdown to select disaster subtype
        ttk.Label(self.main_frame, text="Select Disaster SubType:").grid(row=3, column=0, padx=10, pady=10)
        self.event_subtype_var = tk.StringVar(value="")
        self.event_subtype_dropdown = ttk.Combobox(self.main_frame, textvariable=self.event_subtype_var, state="readonly")
        self.event_subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Load event types
        self.load_event_types()

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.length_event).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=1, pady=10)

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

    def load_event_types(self):
        # Fetch and load event types
        try:
            event_types = self.db.fetch_all_event_types()
            self.event_type_dropdown['values'] = event_types if event_types else []
            if not event_types:
                messagebox.showinfo("No Event Types", "No event types found in the database")
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to load event types: {e}")

    def load_event_subtypes(self, event):
        # Fetch and load event subtypes
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

    def update_length_type(self, event=None):
        # Handles updates when the duration type
        selected_type = self.length_type_var.get()
        print(f"Selected length type: {selected_type}")

    def length_event(self):
        # Fetches and displays the event's duration
        event_type = self.event_type_var.get()
        event_subtype = self.event_subtype_var.get()
        length_type = self.length_type_var.get()

        # Validate selections
        if not event_type:
            messagebox.showerror("Error", "Please select an event type")
            return

        if not event_subtype:
            messagebox.showerror("Error", "Please select a disaster subtype")
            return

        if not length_type:
            messagebox.showerror("Error", "Please select a duration type")
            return

        # Get image based on selected disaster type
        event_image_path = self.get_event_image(event_type)
        if not event_image_path:
            messagebox.showerror("Error", "No image available for the selected disaster type")
            return

        try:
            # Fetch the event duration
            if length_type == "Longest Duration":
                length = self.db.fetch_max_duration_by_event_type(event_type)
            elif length_type == "Shortest Duration":
                length = self.db.fetch_min_duration_by_event_type(event_type)
            else:
                length = self.db.fetch_avg_duration_by_event_type(event_type)

            # Handle no data
            if length is None:
                messagebox.showerror("Error", "No data available for the selected disaster type")
                return

            # Round the duration
            rounded_length = round(length)

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

            # Display the duration
            label_text = tk.Label(
                image_window,
                text=f"{length_type} for {event_subtype}: {rounded_length} days",
                font=("Arial", 12)
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to fetch event duration: {e}")

    def back_to_menu(self):
        # Navigate back to the main menu
        self.controller.switch_to_menu()