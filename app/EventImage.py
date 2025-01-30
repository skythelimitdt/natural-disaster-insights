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

def any_image(event_type=None):
    valid_diaster_types = [
        "Wildfire", "Storm", "Drought", "Volcanic activity", 
        "Epidemic", "Extreme temperature", "Earthquake", "Flood", "Mass movement (wet)"
    ]
    
    if event_type in valid_diaster_types:
        any_images = {
            "Wildfire": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Fire3.jpg",
            "Storm": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\derecho3.jpg",
            "Drought": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\tropicalstorm3.jpg",
            "Volcanic activity": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\\Volcano1.jpg",
            "Epidemic": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\pandemic.jpg",
            "Extreme temperature": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Heatwave1.jpg",
            "Earthquake": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\earthquake2.jpg",
            "Flood": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Flood2x.jpg",
            "Mass movement (wet)": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\mudslide1.jpg",
        }
        return any_images.get(event_type)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\derecho3.jpg"

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
            "Hail": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\hail2.jpg",
            "Lightning/Thunderstorms": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Lightning2.jpg",
            "Sand/Dust storm": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\sandstorm1.jpg",
            "Tornado": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Tornado1.jpg",
            "Tropical cyclone": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\cyclone2.jpg",
        }
        return storm_images.get(event_subtype)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\derecho3.jpg"

def extreme_temp_image(event_subtype=None):
    valid_temp_subtypes = ["Cold wave", "Heat wave"]
    
    if event_subtype in valid_temp_subtypes:
        extreme_temp_images = {
            "Cold wave": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\coldwave2.jpg",
            "Heat wave": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Heatwave1.jpg",
        }
        return extreme_temp_images.get(event_subtype)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\Heatwave1.jpg"

def mass_movement_image(event_subtype=None):
    valid_mass_movement_subtypes = ["Landslide (wet)", "Mudslide"]
    
    if event_subtype in valid_mass_movement_subtypes:
        mass_movement_images = {
            "Landslide (wet)": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\landslide2.jpg",
            "Mudslide": r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\mudslide1.jpg",
        }
        return mass_movement_images.get(event_subtype)
    else:
        return r"C:\Users\Ian O'Connor\Github\natural-disaster-insights\resources\Images\EventPhotos\mudslide1.jpg"