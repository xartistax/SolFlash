
import os

from app_config.app_config import AppConfig



def is_token_in_file(token_address, file_name=AppConfig.LOGGER["TOKENFILE_NAME"]):
    """Check if a token already exists in the file."""
    file_path = os.path.join(AppConfig.LOGGER.get("LOG_DIR"), file_name)
    if not os.path.exists(file_path):
        return False  # File doesn't exist yet, so token is not in it

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if token_address in line:  # Check if token address appears in any line
                return True
    return False