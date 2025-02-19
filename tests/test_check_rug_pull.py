

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.check_rug_pull import check_rug_pull



# Mock the RugCheck API call function to control its behavior
@pytest.fixture
def mock_rug_check_api_call():
    with patch("utils.rug_check_api_call.rug_check_api_call") as mock_api_call:
        yield mock_api_call

# Test for check_rug_pull function
@pytest.mark.asyncio
async def test_check_rug_pull(mock_rug_check_api_call):
    # Mock the logger to bypass logging
    with patch("services.logger.setup_logger") as mock_logger:
        mock_logger.return_value = MagicMock()

        # Mock the RugCheck API call responses
        mock_rug_check_api_call.return_value = {
            "success": True,
            "response": {
                "rugged": False,
                "token": {
                    "mintAuthority": None,
                    "supply": 952039822315783,
                    "decimals": 6,
                    "isInitialized": True,
                    "freezeAuthority": None
                },
                "tokenMeta": {
                    "name": "TomTom",
                    "symbol": "SolFi",
                    "uri": "https://ipfs.io/ipfs/QmWWciuAXexvpFBMNE74fW2A35FccnKXwNZkmLcgfKm5md",
                    "mutable": False,
                    "updateAuthority": "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
                },
                "topHolders": [],
                "markets": []
            }
        }

        # Call the function with a test mint address
        result = await check_rug_pull("99dWcBiDuhHUVHk8Ggu4V2HswpZCurcK7cDRMEGhpump")

        # Debug print to verify the response structure
        print(result)

        # Assertions to verify the expected output
        assert result is not False
        assert "data" in result
        assert "risk" in result["data"]
        assert "token" in result["data"]
        assert "token_meta" in result["data"]["token"]
        assert result["data"]["token"]["token_meta"]["name"] == "TomTom "  # Corrected key path

