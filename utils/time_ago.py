import time

def time_ago(timestamp):
    """
    Returns a human-readable string representing the time ago for the given timestamp.

    Args:
        timestamp (int): The timestamp in milliseconds.

    Returns:
        str: A string representing how long ago the event occurred, e.g. "5 min ago", "2 h ago", or "Unknown" if the timestamp is invalid.
    """
    if not isinstance(timestamp, int): 
        return "Unknown"

    # Convert from milliseconds to seconds
    seconds_ago = int(time.time()) - (timestamp // 1000)  

    # Handle edge cases
    if seconds_ago < 0:
        return "Future time"  # In case timestamp is in the future

    minutes_ago = seconds_ago // 60
    hours_ago = minutes_ago // 60
    days_ago = hours_ago // 24

    # Return more detailed time format
    if minutes_ago < 60:
        return f"{minutes_ago} min ago"
    elif hours_ago < 24:
        return f"{hours_ago} h ago"
    elif days_ago < 7:
        return f"{days_ago} d ago"
    else:
        return f"{days_ago // 7} w ago"  # Weeks ago if more than a week

