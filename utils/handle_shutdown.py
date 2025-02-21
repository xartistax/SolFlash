
import sys
import signal
from services.logger import setup_logger
from utils.cyan_message import cyan_message
logger = setup_logger("SHUT DOWN")


def handle_shutdown(signum, frame):
    """Handle clean shutdown when Ctrl+C is pressed."""
    logger.warning("Application interrupted by user (Ctrl+C). Shutting down...")
    logger.info(cyan_message("System Shutted down!"))

    print(frame)
    
    print(cyan_message("System Shutted down!"))
    sys.exit(0)  # Exit with status code 0 (successful exit)
