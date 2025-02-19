import os

from app_config.app_config import AppConfig
from utils.print_token_alert import print_token_alert
from utils.cyan_message import cyan_message
from services.logger import setup_logger

logger = setup_logger("WRTITE TOKEN TO FILE")

# Add this function to write token data to a file
def write_token_data_to_file(token_data, file_name="tokens.txt"):
    """
        Writes the extracted token data to a text file.

        This function formats the given token data into a human-readable alert message and 
        appends it to a specified text file. The default file is `tokens.txt`. The file path 
        is determined by the log directory specified in the application configuration.

        Args:
            token_data (dict): A dictionary containing the token information to be written to the file.
            file_name (str, optional): The name of the file to write the data to. Defaults to "tokens.txt".

        Raises:
            TypeError: If the provided token_data is not a dictionary.
            Exception: If any other error occurs while writing the token data to the file.

        Returns:
            None
        """

    try:
        # Ensure token_data is a dictionary
        if not isinstance(token_data, dict):
            raise TypeError("Expected 'token_data' to be a dictionary.")

        # Define the path for the file
        file_path = os.path.join(AppConfig.LOGGER.get("LOG_DIR"), file_name)

        # Format the token data into a single line string
        alert_message = print_token_alert(token_data)

        # Open the file in append mode
        with open(file_path, "a", encoding="utf-8") as file:
            # Write the alert message to the file
            file.write(alert_message + "\n")  # Add newline after each token
            logger.info(cyan_message(f"Token data written to {file_path}"))
            print(cyan_message(f"Token data written to {file_path}"))

    except Exception as e:
        logger.error(f"Failed to write token data to file: {e}")
