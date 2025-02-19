import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.print_token_alert import print_token_alert


def test_print_token_alert():
    # Example token data for testing
    token_data = {
        "address": "0x1234567890abcdef",
        "name": "TomTom",
        "symbol": "TOM",
        "market_cap": "500M USD",
        "created": "2025-02-19 14:30",
        "volume_5m": "10,000",
        "url": "https://dexscreener.com/token/12345",
        "social_links": "https://twitter.com/TomTomCoin"
    }

    # Expected output based on the new format without color codes
    expected_message = (
        "Address: 0x1234567890abcdef | "
        "Name: TomTom | "
        "Symbol: TOM | "
        "MarketCap: 500M USD | "
        "Created: 2025-02-19 14:30 | "
        "Volume (5m): 10,000 USD | "
        "DexScreener URL: https://dexscreener.com/token/12345 | "
        "Socials: https://twitter.com/TomTomCoin"
    )

    # Call the function with the test data
    result = print_token_alert(token_data)

    # Assert that the result matches the expected message
    assert result == expected_message, f"Expected: {expected_message}, but got: {result}"
