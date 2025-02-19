import pytest
from unittest.mock import patch
from app_config.app_config import AppConfig

import sys
import os

from utils.extract_token_address import extract_token_address

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_extract_token_address():
    # List of addresses, including the system address
    addresses = ["addr1", "addr2", "wsol_pc_mint", "addr4"]

    # Mock AppConfig.LIQUIDITY_POOL["wsol_pc_mint"]
    with patch.object(AppConfig, 'LIQUIDITY_POOL', {"wsol_pc_mint": "wsol_pc_mint"}):
        # Call the function with the test data
        result = extract_token_address(addresses)

        # Expected result, where the system address is removed
        expected_result = ["addr1", "addr2", "addr4"]

        # Assert that the result matches the expected filtered list
        assert result == expected_result
