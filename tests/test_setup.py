import sys
import os



# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from unittest.mock import patch, MagicMock
from services.env import ConfigENV
from utils.setup import setup

@pytest.fixture
def mock_config_env():
    with patch.object(ConfigENV, 'initialize') as mock_initialize, \
         patch.object(ConfigENV, 'check_env_vars') as mock_check_env_vars:
        # Mock the environment methods
        mock_initialize.return_value = None
        mock_check_env_vars.return_value = True
        yield mock_initialize, mock_check_env_vars

def test_setup_success(mock_config_env):
    mock_initialize, mock_check_env_vars = mock_config_env

    # Ensure the mock for check_env_vars returns True
    mock_check_env_vars.return_value = True

    # Mock the necessary attributes in ConfigENV
    ConfigENV.HELIUS_URL = "http://example.com"
    ConfigENV.HELIUS_TX_URL = "http://tx.example.com"

    # Test that the setup function works successfully
    result = setup()

    # Assertions to ensure setup completed successfully
    assert result is True
    mock_initialize.assert_called_once()
    mock_check_env_vars.assert_called_once()

def test_setup_missing_env_vars(mock_config_env):
    mock_initialize, mock_check_env_vars = mock_config_env

    # Ensure the mock for check_env_vars returns False
    mock_check_env_vars.return_value = False

    # Test that the setup fails when environment variables are missing
    result = setup()

    # Assertions to ensure setup failed due to missing env vars
    assert result is False

def test_setup_exception_handling(mock_config_env):
    mock_initialize, mock_check_env_vars = mock_config_env

    # Ensure the mock for initialize raises an exception
    mock_initialize.side_effect = Exception("Test exception")

    # Test that the setup handles unexpected errors
    result = setup()

    # Assertions to ensure setup failed due to the exception
    assert result is False
