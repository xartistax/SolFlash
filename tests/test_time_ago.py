import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from utils.time_ago import time_ago




def test_valid_timestamp():
    # Using a timestamp of 5 minutes ago
    five_minutes_ago = int((time.time() - 300) * 1000)  # 300 seconds ago in milliseconds
    result = time_ago(five_minutes_ago)
    assert result == "5 min ago"

def test_future_timestamp():
    # Using a timestamp in the future
    future_timestamp = int((time.time() + 300) * 1000)  # 5 minutes in the future in milliseconds
    result = time_ago(future_timestamp)
    assert result == "Future time"

def test_invalid_timestamp_string():
    # Using an invalid timestamp (non-integer)
    result = time_ago("not_a_timestamp")
    assert result == "Unknown"

def test_invalid_timestamp_float():
    # Using a float value
    result = time_ago(1632945813000.5)  # float instead of int
    assert result == "Unknown"

def test_edge_case_just_now():
    # Using a timestamp for "just now" (current time)
    current_timestamp = int(time.time() * 1000)  # current time in milliseconds
    result = time_ago(current_timestamp)
    assert result == "0 min ago"

def test_edge_case_older_than_week():
    # Using a timestamp older than a week (7+ days ago)
    seven_days_ago = int((time.time() - 7 * 24 * 60 * 60) * 1000)  # 7 days ago
    result = time_ago(seven_days_ago)
    assert result == "1 w ago"
