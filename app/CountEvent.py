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
        self.event_type_var = tk.StringVar(value="Any")
        self.event_type_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_type_var, state="readonly"
        )
        self.event_type_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.event_type_dropdown.bind("<<ComboboxSelected>>", self.load_disaster_subtypes)

        # Create and configure the dropdown for disaster subtype selection
        ttk.Label(self.main_frame, text="Select Disaster Subtype:").grid(row=2, column=0, padx=10, pady=5)
        self.event_subtype_var = tk.StringVar(value="Any")
        self.event_subtype_dropdown = ttk.Combobox(
            self.main_frame, textvariable=self.event_subtype_var, state="readonly"
        )
        self.event_subtype_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Load disaster types
        self.load_disaster_types()

        # Add buttons for generating the count and returning to the menu
        ttk.Button(self.main_frame, text="Generate", command=self.count_events).grid(row=3, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=3, column=1, pady=10)

    def load_disaster_types(self):
        try:
            disaster_types = self.db.fetch_all_event_types()
            disaster_types.insert(0, "Any")
            self.event_type_dropdown["values"] = disaster_types
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def load_disaster_subtypes(self, event=None):
        event_type = self.event_type_var.get()
        if not event_type or event_type == "Any":
            self.event_subtype_dropdown["values"] = ["Any"]
            self.event_subtype_var.set("Any")
            return

        try:
            subtypes = self.db.fetch_subtypes_by_event_type(event_type)
            if subtypes:
                subtypes.insert(0, "Any")
                self.event_subtype_dropdown["values"] = subtypes
                self.event_subtype_var.set("Any")
            else:
                self.event_subtype_dropdown["values"] = ["Any"]
                self.event_subtype_var.set("Any")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load disaster subtypes: {e}")

    def get_event_image_path(self, event_type, event_subtype):
        if event_type == "Flood":
            return ei.flood_image()
        elif event_type == "Fire":
            return ei.fire_image()
        elif event_type == "Earthquake":
            return ei.earthquake_image()
        elif event_type == "Volcano":
            return ei.volcano_image()
        elif event_type == "Drought":
            return ei.drought_image()
        elif event_type == "Epidemic":
            return ei.epidemic_image()
        elif event_type == "Extreme Temperature":
            return ei.extreme_temp_image(event_subtype)
        elif event_type == "Storm":
            return ei.storm_image(event_subtype)
        elif event_type == "Mass Movement":
            return ei.mass_movement_image(event_subtype)
        else:
            return ei.any_image(event_type)

    def count_events(self):
        event_type = self.event_type_var.get()
        event_subtype = self.event_subtype_var.get()

        # Convert "Any" to None for database query compatibility
        if event_type == "Any":
            event_type = None
        if event_subtype == "Any":
            event_subtype = None

        # Create the image window first
        image_window = tk.Toplevel(self.master)

        try:
            # Fetch disaster count based on selected type and subtype
            count = self.db.count_disasters_by_event_type_and_subtype(event_type, event_subtype)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch event count: {e}")

        else:
            # Otherwise, count by the selected type and subtype
            try:
                # Fetch disaster count based on selected type and subtype
                count = self.db.count_disasters_by_event_type_and_subtype(event_type, event_subtype)

                image_window.title(f"Disaster Type: {event_type or 'All Types'}")

                # Get the disaster image
                event_image_path = self.get_event_image_path(event_type, event_subtype)

                # Load and display the image if available
                if event_image_path:
                    try:
                        img = Image.open(event_image_path)
                        img = img.resize((400, 275), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(img)

                        label_image = tk.Label(image_window, image=photo)
                        label_image.image = photo
                        label_image.pack(padx=10, pady=10)
                    except Exception as e:
                        messagebox.showwarning("Image Error", f"Failed to load image: {e}")

                        # Provide fallback image or message
                        fallback_image = Image.new("RGB", (400, 275), (200, 200, 200))
                        fallback_photo = ImageTk.PhotoImage(fallback_image)

                        label_fallback = tk.Label(image_window, image=fallback_photo, text="Image Not Available")
                        label_fallback.image = fallback_photo
                        label_fallback.pack(padx=10, pady=10)

                # Modify this section to handle the specific message for 'Any' subtype
                if event_type is None and event_subtype is None:
                    label_text = tk.Label(
                        image_window,
                        text=f"All Disaster Types: Number of disasters is {count}",
                        font=("Arial", 12),
                    )
                elif event_subtype is None:
                    label_text = tk.Label(
                        image_window,
                        text=f"All {event_type} Subtypes: Number of disasters is {count}",
                        font=("Arial", 12),
                    )
                else:
                    label_text = tk.Label(
                        image_window,
                        text=f"{event_subtype}: Number of disasters is {count}",
                        font=("Arial", 12),
                    )
                label_text.pack(padx=10, pady=5)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch event count: {e}")

    def back_to_menu(self):
        self.controller.switch_to_menu()

    def clear_ui(self):
        # Clear all input fields
        self.event_type_var.set("")
        self.event_subtype_var.set("")
        self.event_subtype_dropdown["values"] = []