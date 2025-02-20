import os

from app_config.app_config import AppConfig
from utils.print_token_alert import print_token_alert
from utils.cyan_message import cyan_message
from services.logger import setup_logger

logger = setup_logger("WRITE TOKEN TO FILE")


def write_token_data_to_file(token_data, file_name=None):
    """
    Writes the extracted token data to a text file.

    This function formats the given token data into a human-readable alert message and 
    appends it to a specified text file. The default file is defined in the application configuration.

    Args:
        token_data (dict): A dictionary containing the token information to be written to the file.
        file_name (str, optional): The name of the file to write the data to. Defaults to AppConfig.LOGGER["TOKENFILE_NAME"].

    Raises:
        TypeError: If the provided token_data is not a dictionary.
        FileNotFoundError: If the log directory does not exist.
        PermissionError: If the program lacks write permissions.
        Exception: If any other error occurs while writing the token data to the file.

    Returns:
        None
    """
    try:
        if not isinstance(token_data, dict):
            raise TypeError(f"Expected 'token_data' to be a dictionary, but received {type(token_data)}.")

        file_name = file_name or AppConfig.LOGGER["TOKENFILE_NAME"]
        log_dir = AppConfig.LOGGER.get("LOG_DIR")

        if not log_dir:
            raise ValueError("Log directory is not defined in AppConfig.")

        file_path = os.path.join(log_dir, file_name)

        logger.debug(f"Preparing to write token data to {file_path}...")

        if not os.path.exists(log_dir):
            raise FileNotFoundError(f"Log directory '{log_dir}' does not exist. Please create it.")

        # Format the token data into a single-line string
        alert_message = print_token_alert(token_data)

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(alert_message + "\n")

        logger.info(cyan_message(f"Token data written to {file_path}"))
        # print(cyan_message(f"Token data written to {file_path}"))
        return

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
    except PermissionError:
        logger.error(f"Permission denied: Cannot write to {file_path}")
    except TypeError as e:
        logger.error(f"Data format error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while writing token data: {e}", exc_info=True)
