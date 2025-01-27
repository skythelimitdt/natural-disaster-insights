from datetime import datetime

# Constants
START_YEAR = 2000
END_YEAR = 2025

def valid_date_range(from_date, to_date):
    try:
        # Convert string dates to datetime objects
        from_date_obj = datetime.strptime(from_date, "%m-%d-%Y")
        to_date_obj = datetime.strptime(to_date, "%m-%d-%Y")
        
        # Check if the from_date is earlier than or equal to to_date
        return from_date_obj <= to_date_obj
    except ValueError:
        return False

def is_valid_date(from_date, to_date):
    # Check if the date range is valid
    if not valid_date_range(from_date, to_date):
        return False, "From date must be before or equal to the To date"
    
    # Check if the dates are within the allowed range
    try:
        from_date_obj = datetime.strptime(from_date, "%m-%d-%Y")
        to_date_obj = datetime.strptime(to_date, "%m-%d-%Y")
        
        # Check if both dates are within the allowed range
        if from_date_obj.year < START_YEAR or to_date_obj.year > END_YEAR:
            return False, f"Dates must be between {START_YEAR} and {END_YEAR}"
    except ValueError:
        return False, "Invalid date format. Please use MM-DD-YYYY"
    return True, ""

def is_valid_string(input_string):
    # Check if the string is empty
    if not input_string.strip():
        return False, "Input cannot be empty"
    return True, ""

def is_valid_name(name):
    # Check if name is empty
    if not name.strip():
        return False, "Name cannot be empty"
    return True, ""