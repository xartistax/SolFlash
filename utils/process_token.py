import os

from app_config.app_config import AppConfig
from services.logger import setup_logger
from utils.add_token_to_db import add_token_to_db
from utils.is_token_in_file import is_token_in_file
from utils.cyan_message import cyan_message
from utils.print_token_alert import print_token_alert
from utils.extract_token_data import extract_token_data
from utils.send_message_to_telegram import send_message_to_telegram
from utils.write_tokens_to_file import write_token_data_to_file

logger = setup_logger("PROCESS TOKEN")

TOKEN_FILE = "tokens.log"  # Ensure this is the correct file path


def process_token(token):
    """
    Processes the token data: extracts required fields, writes to file, and sends a message to Telegram
    if enabled.

    Args:
        token (dict): Token data to process.

    Returns:
        None or str: Returns a message if an error occurs, otherwise None.
    """
    try:
        if not isinstance(token, dict):
            raise TypeError(f"Expected token to be a dict, but received {type(token)}.")

        if not token:
            logger.error("Received empty token data. Skipping...")
            return "Error: No token data found."

        logger.debug(f"Extracting data from token...")

        token_data = extract_token_data(token)

        token_address = token_data.get("address")  # Ensure this key is correct
        if not token_address:
            logger.error("Token data missing 'address' key. Skipping...")
            return "Error: Missing 'address' key in token data."

        logger.debug(f"Token {token_address} - Writing data to file...")

        write_token_data_to_file(token_data)
        add_token_to_db(token_data)
        


        if AppConfig.TELEGRAM.get("ENABLED"):
            result = send_message_to_telegram(token_data)
            logger.info(f"Token {token_address} - Message sent to Telegram: {result}")
        else:
            logger.info(f"Token {token_address} - Telegram notifications are disabled.")

        return None

    except KeyError as e:
        logger.error(f"Token processing failed - Missing key: {e}")
        return f"Error: Missing key {e} in token data."
    except (ValueError, TypeError) as e:
        logger.error(f"Token processing failed - Invalid data format: {e}")
        return f"Error: Invalid data format - {e}"
    except Exception as e:
        logger.error(f"Token processing failed - Unexpected error: {e}", exc_info=True)
        return f"Error: Unexpected error - {e}"
