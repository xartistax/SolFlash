import logging
import os
from datetime import datetime
from app_config.app_config import AppConfig

# ANSI Escape Codes für Farben (nur für Datei-Logs)
LOG_COLORS = {
    "DEBUG": "\033[94m",  # Blau
    "INFO": "\033[92m",  # Grün
    "WARNING": "\033[93m",  # Gelb
    "ERROR": "\033[91m",  # Rot
    "CRITICAL": "\033[1;91m",  # Helles Rot
    "RESET": "\033[0m"  # Reset
}

# Mapping für Log-Level
LOGGING_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# Log-Verzeichnis erstellen
LOG_DIR = AppConfig.LOGGER.get("LOG_DIR")
os.makedirs(LOG_DIR, exist_ok=True)


class ColorizedFileFormatter(logging.Formatter):
    """Formatter für farbige Logs in der Log-Datei"""
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS["RESET"])
        reset = LOG_COLORS["RESET"]
        record.msg = f"{log_color}{record.msg}{reset}"
        return super().format(record)


def setup_logger(name="MainLogger"):
    """Erstellt einen Logger mit täglichem Logfile und farbigen Logs in der Datei."""
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger  # Verhindert doppelte Handler
    
    # Always set logger level to DEBUG to ensure all logs are captured
    logger.setLevel(logging.DEBUG)

    # Formatter für Log-Nachrichten
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    )

    # Console-Handler (ohne Farben), level from config
    console_handler = logging.StreamHandler()
    console_level = LOGGING_LEVEL_MAP.get(AppConfig.LOGGER.get("CONSOLE_LEVEL"), logging.INFO)  # Use config for console
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Datei-Handler (farbig), always at DEBUG level for file logging
    log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"  # Gleiches Logfile pro Tag
    log_filepath = os.path.join(LOG_DIR, log_filename)

    file_handler = logging.FileHandler(log_filepath, mode="a", encoding="utf-8")
    file_level = LOGGING_LEVEL_MAP.get(AppConfig.LOGGER.get("FILE_LEVEL"), logging.INFO)  # Use config for console
    file_handler.setLevel(file_level)  # Force file handler to always log at DEBUG level
    file_handler.setFormatter(ColorizedFileFormatter(formatter._fmt))
    logger.addHandler(file_handler)

    return logger
