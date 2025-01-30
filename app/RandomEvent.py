import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Database import Database
import EventImage as ei

class RandomEvent:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.db = Database()

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Title label
        self.title_label = ttk.Label(
            self.main_frame, text="Generate Random Disaster", font=("Arial", 16, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Load random event types
        self.load_random_event()

        # Buttons
        ttk.Button(self.main_frame, text="Generate", command=self.random_event).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_frame, text="Back", command=self.back_to_menu).grid(row=2, column=1, pady=10)

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

    def load_random_event(self):
        # Loads available event types
        try:
            # Fetch event types from the database
            self.db.fetch_all_event_types()  
        except Exception as e:
            # Error if event types cannot be fetched
            messagebox.showerror("Error", f"Failed to load disaster types: {e}")

    def random_event(self):
        try:
            # Fetch random disaster from the database
            random_disaster = self.db.fetch_random_disaster()
            
            if random_disaster and random_disaster[0]:
                event_type = random_disaster[0]
                event_subtype = random_disaster[1] if len(random_disaster) > 1 else "Unknown"

                # Get the image for the random disaster
                event_image_path = self.get_event_image(event_type, event_subtype)
                if not event_image_path:
                    messagebox.showerror("Error", f"No image available for disaster type: {event_type}")
                    return

                # Create a new window
                image_window = tk.Toplevel(self.master)
                image_window.title(f"Disaster Type: {event_type}")
                
                try:
                    # Load and display the image
                    img = Image.open(event_image_path)
                    img = img.resize((400, 275), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    label_image = tk.Label(image_window, image=photo)
                    label_image.image = photo
                    label_image.pack(padx=10, pady=10)
                except Exception as e:
                    messagebox.showwarning("Image Error", f"Failed to load image: {e}")
                    # Create a blank image as fallback
                    fallback_image = Image.new("RGB", (400, 275), (200, 200, 200))  # Grey fallback image
                    fallback_photo = ImageTk.PhotoImage(fallback_image)

                    label_fallback = tk.Label(image_window, image=fallback_photo, text="Image Not Available", font=("Arial", 12))
                    label_fallback.image = fallback_photo
                    label_fallback.pack(padx=10, pady=10)

                # Display disaster type and subtype
                label_text = tk.Label(
                    image_window,
                    text=f"Random Disaster: {event_subtype}",
                    font=("Arial", 12),
                )
                label_text.pack(padx=10, pady=5)

            else:
                # Show warning if no valid disaster found
                messagebox.showwarning("No disasters found", "No valid disaster type found.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch random disaster: {e}")

    def clear_ui(self):
        # Resets the UI fields
        self.location_var.set("")

    def back_to_menu(self):
        # Handles navigation back to menu
        self.controller.switch_to_menu()