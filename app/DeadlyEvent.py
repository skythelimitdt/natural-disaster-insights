import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei


class DeadlyEvent:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title
        self.title_label = ttk.Label(
            self.main_frame, text="Calculate Disaster Fatalities", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Deadliness type dropdown
        ttk.Label(self.main_frame, text="Select Deadliness Type:").grid(row=1, column=0, padx=10, pady=5)
        self.deadliness_var = tk.StringVar()
        self.deadliness_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.deadliness_var,
            values=["Highest Death Toll", "Lowest Death Toll", "Average Death Toll"],
            state="readonly",
        )
        self.deadliness_dropdown.grid(row=1, column=1, padx=10, pady=10)

        # Disaster type dropdown
        ttk.Label(self.main_frame, text="Select Disaster Type:").grid(row=2, column=0, padx=10, pady=5)
        self.event_type_var = tk.StringVar()
        self.event_type_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_type_var, state="readonly"
        )
        self.event_type_dropdown.grid(row=2, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.update_subtypes)

        # Disaster subtype dropdown
        ttk.Label(self.main_frame, text="Select Disaster Subtype:").grid(row=3, column=0, padx=10, pady=5)
        self.subtype_var = tk.StringVar()
        self.subtype_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.subtype_var, state="readonly"
        )
        self.subtype_dropdown.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.deadly_event).grid(row=4, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=4, column=1, pady=10)

        # Populate event types dynamically
        self.populate_event_types()

    def populate_event_types(self):
        """Fetch and populate disaster types dynamically from the database."""
        try:
            event_types = self.db.fetch_all_event_types()
            if event_types:
                self.event_type_dropdown["values"] = event_types
            else:
                self.event_type_dropdown["values"] = ["No data available"]
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load disaster types: {e}")

    def update_subtypes(self, event=None):
        """Update subtypes based on the selected disaster type."""
        event_type = self.event_type_var.get()
        if not event_type:
            self.subtype_dropdown["values"] = []
            self.subtype_var.set("")
            return

        try:
            subtypes = self.db.fetch_subtypes_by_event_type(event_type)
            self.subtype_dropdown["values"] = subtypes if subtypes else ["No subtypes available"]
            self.subtype_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load subtypes: {e}")

    def get_event_image(self, event_type, event_subtype=None):
        """Returns the image path for the given disaster type and subtype."""
        event_images = {
            "Flood": ei.flood_image(),
            "Wildfire": ei.fire_image(),
            "Earthquake": ei.earthquake_image(),
            "Volcanic activity": ei.volcano_image(),
            "Storm": ei.storm_image(event_subtype) if event_subtype else ei.storm_image("default"),
            "Drought": ei.drought_image(),
            "Extreme temperature": ei.extreme_temp_image(event_subtype) if event_subtype else ei.extreme_temp_image("default"),
            "Epidemic": ei.epidemic_image(),
            "Mass movement (wet)": ei.mass_movement_image(event_subtype) if event_subtype else ei.mass_movement_image("default"),
        }
        return event_images.get(event_type)

    def deadly_event(self):
        """Generate a report on disaster fatalities."""
        event_type = self.event_type_var.get()
        deadliness_type = self.deadliness_var.get()
        event_subtype = self.subtype_var.get() or None  # Use None if empty

        if not event_type or not deadliness_type:
            messagebox.showerror("Error", "Please select disaster type and deadliness type.")
            return

        # Get event image
        event_image_path = self.get_event_image(event_type, event_subtype)
        if not event_image_path:
            messagebox.showerror("Error", "No image available for the selected disaster type.")
            return

        try:
            # Fetch fatalities from the database
            if deadliness_type == "Highest Death Toll":
                fatalities = self.db.fetch_max_fatalities_by_event_type(event_type)
                description = "highest death toll"
            elif deadliness_type == "Lowest Death Toll":
                fatalities = self.db.fetch_min_fatalities_by_event_type(event_type)
                description = "lowest death toll"
            else:
                fatalities = self.db.fetch_avg_fatalities_by_event_type(event_type)
                description = "average death toll"

            # Round fatalities for better readability
            fatalities = round(fatalities) if fatalities is not None else "N/A"

            # Create a new window to display results
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

            # Display fatalities count
            label_text = tk.Label(
                image_window,
                text=f"{event_subtype if event_subtype else event_type}: {description.capitalize()} is {fatalities} fatalities.",
                font=("Arial", 12)
            )
            label_text.pack(padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch fatalities: {e}")

    def clear_ui(self):
        """Clear all input fields."""
        self.event_type_var.set("")
        self.subtype_var.set("")
        self.subtype_dropdown["values"] = []

    def back_to_menu(self):
        """Navigate back to the main menu."""
        self.controller.switch_to_menu()