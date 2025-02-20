import pytest
from unittest.mock import patch
from babel.numbers import format_decimal


import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract_token_data import extract_token_data


# Sample token data with all fields
sample_token_data = {
    "baseToken": {
        "address": "0x1234567890abcdef",
        "name": "Sample Token",
        "symbol": "SAMP"
    },
    "marketCap": 1000000,
    "priceUsd": 2.5,
    "volume": {"m5": 1000},
    "url": "https://sampletoken.com",
    "pairCreatedAt": "2874 w ago",  # Unix timestamp
    "info": {
        "socials": [
            {"type": "twitter", "url": "https://twitter.com/sampletoken"},
            {"type": "website", "url": "https://sampletoken.com"}
        ]
    }
}






def test_extract_token_data():
    # Sample data with Unix timestamp
    sample_token_data = {
        "baseToken": {
            "address": "0x1234567890abcdef",
            "name": "Sample Token",
            "symbol": "SAMP"
        },
        "marketCap": 1000000,
        "priceUsd": 2.5,
        "volume": {"m5": 1000},
        "url": "https://sampletoken.com",
        "pairCreatedAt": 1624550400,  # Unix timestamp (example)
        "info": {
            "socials": [
                {"type": "twitter", "url": "https://twitter.com/sampletoken"},
                {"type": "website", "url": "https://sampletoken.com"}
            ]
        }
    }

    # Mock time_ago function to return a fixed value
    with patch("utils.time_ago.time_ago", return_value="2874 w ago"):
        result = extract_token_data(sample_token_data)

    expected_result = {
        "address": "0x1234567890abcdef",
        "name": "Sample Token",
        "symbol": "SAMP",
        "market_cap": format_decimal(1000000, locale='de_DE'),
        "price_usd": 2.5,
        "volume_5m": 1000,
        "url": "https://sampletoken.com",
        "created": "2874 w ago",
        "social_links": "[Twitter](https://twitter.com/sampletoken) | [Website](https://sampletoken.com)"
    }

    assert result == expected_result





def test_extract_token_data_with_missing_keys():
    # Mock the time_ago function to return a fixed value
    with patch("utils.time_ago.time_ago", return_value="2874 w ago"):
        result = extract_token_data(sample_token_data)
    assert result['created'] == "2874 w ago"
