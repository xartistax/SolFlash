from services.env import ConfigENV
from services.logger import setup_logger

logger = setup_logger("SETUP")

def setup():
    """Initialize environment and check configuration."""
    
    try:
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
