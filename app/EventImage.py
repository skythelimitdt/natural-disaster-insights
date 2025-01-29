def flood_image():
    return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Flood2.jpg"

def fire_image():
    return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Fire3.jpg"

def earthquake_image():
    return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\earthquake2.jpg"

def volcano_image():
    return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\\Volcano1.jpg"

def drought_image():
    return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\drought1.jpg"

def epidemic_image():
    return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\pandemic.jpg"

def storm_image(event_subtype=None):
    valid_storm_subtypes = [
        "Blizzard/Winter storm", "Derecho", "Extra-tropical storm", "Hail", 
        "Lightning/Thunderstorms", "Sand/Dust storm", "Tornado", "Tropical cyclone"
    ]
    
    if event_subtype in valid_storm_subtypes:
        storm_images = {
            "Blizzard/Winter storm": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\snowstorm2.jpg",
            "Derecho": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\derecho1.jpg",
            "Extra-tropical storm": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\tropicalstorm3.jpg",
            "Hail": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Hurricane1.jpg",
            "Lightning/Thunderstorms": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Lightning2.jpg",
            "Sand/Dust storm": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\sandstorm1.jpg",
            "Tornado": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Tornado1.jpg",
            "Tropical cyclone": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\cyclone2.jpg",
        }
        return storm_images.get(event_subtype)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\derecho3.jpg"

def extreme_temp_image(event_subtype=None):
    valid_temp_subtypes = ["Cold Wave", "Heat Wave"]
    
    if event_subtype in valid_temp_subtypes:
        extreme_temp_images = {
            "Cold Wave": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\coldwave2.jpg",
            "Heat Wave": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Heatwave1.jpg",
        }
        return extreme_temp_images.get(event_subtype)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Heatwave1.jpg"

def mass_movement_image(event_subtype=None):
    valid_mass_movement_subtypes = ["Landslide", "Mudslide"]
    
    if event_subtype in valid_mass_movement_subtypes:
        mass_movement_images = {
            "Landslide": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\landslide2.jpg",
            "Mudslide": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\mudslide1.jpg",
        }
        return mass_movement_images.get(event_subtype)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\mudslide1.jpg"