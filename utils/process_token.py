from app_config.app_config import AppConfig
from services.logger import setup_logger
from utils.cyan_message import cyan_message
from utils.print_token_alert import print_token_alert
from utils.extract_token_data import extract_token_data
from utils.send_message_to_telegram import send_message_to_telegram
from utils.write_tokens_to_file import write_token_data_to_file

logger = setup_logger("PROCESS TOKEN")

def process_token(tokens):
    """
    Processes the token data: extracts required fields, writes to file, and sends a message to Telegram
    if enabled.

    Args:
        tokens (list): List of token data to process.

    Returns:
        None or str: Returns a message if an error occurs, otherwise None.
    """
    try:
        # Ensure tokens is a list
        if not isinstance(tokens, list):
            raise TypeError("Expected 'tokens' to be a list.")

        # Check if the list is empty
        if not tokens:
            logger.error("No token data found.")
            return "Error: No token data found."

        # Debugging: Log raw token data
        logger.debug(f"Raw token data: {tokens[0]}")

        # Extract required fields from the first token in the list
        token_data = extract_token_data(tokens[0])

        logger.debug(f"Extracted token data: {token_data}")

        # Write the extracted token data to a file
        write_token_data_to_file(token_data)

        # Send the message to Telegram if enabled
        if AppConfig.TELEGRAM.get("ENABLED"):
            result = send_message_to_telegram(token_data)  # Send data to Telegram
            logger.info(f"Message sent to Telegram: {result}")
        else:
            logger.info("Telegram notifications are disabled.")

        return

    except KeyError as e:
        logger.error(f"Missing expected key in token data: {e}")
        return f"Error: Missing key {e} in token data"
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid data format: {e}")
        return f"Error: Invalid data format - {e}"
    except Exception as e:
        logger.error(f"Unexpected error while processing token: {e}", exc_info=True)
        return f"Error: Unexpected error - {e}"
