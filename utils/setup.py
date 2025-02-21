import os
import shutil
from app_config.app_config import AppConfig
from services.database import PostgresDB
from services.env import ConfigENV
from services.logger import setup_logger
from utils.add_token_to_db import db_connect



def setup():
    """Initialize environment and check configuration."""
    
    try:
        if AppConfig.DEVELOPMENT:
            log_dir = AppConfig.LOGGER.get("LOG_DIR")

            db = db_connect()
            db.truncate_table(AppConfig.DB_TRADE_TABLE)

            # Remove the existing log directory
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)

                logger = setup_logger("SETUP")
                logger.info(f"Removed existing log directory: {log_dir}")
        
        else:
            logger = setup_logger("SETUP")

        # Initialize the environment configuration
        ConfigENV.initialize()

    


        # Check if all required environment variables are set
        if not ConfigENV.check_env_vars():
            logger.critical("Environment variables are missing! Exiting setup.")
            return False

        # Log successful configuration loading
        logger.debug("Configuration loaded successfully.")
        
        # Log individual configuration settings for debugging (optional for production)
        logger.debug(f"HELIUS_URL: {ConfigENV.HELIUS_URL}")
        logger.debug(f"HELIUS_TX_URL: {ConfigENV.HELIUS_TX_URL}")
        
        return True

    except Exception as e:
        # Log any unexpected error during setup
        logger.error(f"An error occurred during setup: {e}", exc_info=True)
        return False
