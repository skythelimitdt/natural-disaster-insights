from datetime import datetime

def valid_date_range(from_date, to_date):
    try:
        from_date_obj = datetime.strptime(from_date, "%m-%d-%Y")
        to_date_obj = datetime.strptime(to_date, "%m-%d-%Y")
        return from_date_obj <= to_date_obj
    except ValueError:
        return False

def is_valid_date(from_date, to_date):
    if not valid_date_range(from_date, to_date):
        return False, "From date must be before or equal to the To date."
    return True, "Dates are valid."

def is_valid_millenium_year(year):
    if int(year) < 2000:
        return False, "Please choose a year between 2000 and 2024."
    return True, None
