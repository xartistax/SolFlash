import os


from dotenv import load_dotenv

from app_config.app_config import AppConfig

# Load environment variables from .env file
load_dotenv()

class ConfigENV:
    ENV = {
        "MAINNET": AppConfig.MAINNET ,  # Convert string to boolean
        "HELIUS_WSS_DEV_URL": os.getenv("HELIUS_WSS_DEV_URL", None),
        "HELIUS_WSS_URL": os.getenv("HELIUS_WSS_URL", None),
        "HELIUS_HTTPS_URL_TX_DEV": os.getenv("HELIUS_HTTPS_URL_TX_DEV", None),
        "HELIUS_HTTPS_URL_TX": os.getenv("HELIUS_HTTPS_URL_TX", None),
        "RUGCHECK_API": os.getenv("RUGCHECK_API", None),
        "RUGCHECK_TOKEN_ROUTE_REPORT": os.getenv("RUGCHECK_TOKEN_ROUTE_REPORT", None),
        "RUGCHECK_TOKEN_ROUTE_SUMMARY": os.getenv("RUGCHECK_TOKEN_ROUTE_SUMMARY", None),
        "DEXSCREENER_API": os.getenv("DEXSCREENER_API", None),
        "HELIUS_API_KEY": os.getenv("HELIUS_API_KEY", None),
        "TELEGRAM_URL": os.getenv("TELEGRAM_URL", None),
        "TELEGRAM_CHAT": os.getenv("TELEGRAM_CHAT", None),
        "PGHOST": os.getenv("PGHOST", None),
        "PGDATABASE": os.getenv("PGDATABASE", None),
        "PGUSER": os.getenv("PGUSER", None),
        "PGPASSWORD": os.getenv("PGPASSWORD", None),

    }

    @classmethod
    def load_env(cls):
        """Reload environment variables dynamically."""
        load_dotenv(override=True)
        cls.ENV.update({
            "MAINNET": ConfigENV.ENV.get("MAINNET") , 
            "HELIUS_WSS_DEV_URL": os.getenv("HELIUS_WSS_DEV_URL", None),
            "HELIUS_WSS_URL": os.getenv("HELIUS_WSS_URL", None),
            "HELIUS_HTTPS_URL_TX_DEV": os.getenv("HELIUS_HTTPS_URL_TX_DEV", None),
            "HELIUS_HTTPS_URL_TX": os.getenv("HELIUS_HTTPS_URL_TX", None),
            "HELIUS_API_KEY": os.getenv("HELIUS_API_KEY", None),
            "TELEGRAM_URL": os.getenv("TELEGRAM_URL", None),
            "TELEGRAM_CHAT": os.getenv("TELEGRAM_CHAT", None),
        })

    @classmethod
    def get_helius_wss_url(cls):
        """Constructs the correct Helius WebSocket URL based on the environment."""
        main_enironment = cls.ENV["MAINNET"]
        base_url = cls.ENV["HELIUS_WSS_URL"] if main_enironment else  cls.ENV["HELIUS_WSS_DEV_URL"]
        helius_api_key = os.getenv("HELIUS_API_KEY", "")
        return f"{base_url}{helius_api_key}"
    
    @classmethod
    def get_helius_tx_url(cls):
        """Constructs the correct Helius Transaction URL based on the environment."""
        main_enironment = cls.ENV["MAINNET"]
        base_url = cls.ENV["HELIUS_HTTPS_URL_TX"] if main_enironment else  cls.ENV["HELIUS_HTTPS_URL_TX_DEV"]
        helius_api_key = os.getenv("HELIUS_API_KEY", "")
        return f"{base_url}{helius_api_key}"

    @classmethod
    def check_env_vars(cls):
        """Check for missing or empty environment variables."""
        missing_or_empty_vars = [
            key for key, value in cls.ENV.items() if value is None or (value == "" and key != "DEV_ENVIRONMENT")
        ]  # Skip DEV_ENVIRONMENT if it's set to False (string "false")
        
        if missing_or_empty_vars:
            print(f"Error: Missing or empty environment variables: {', '.join(missing_or_empty_vars)}")
            return False
        return True
    
    @classmethod
    def initialize(cls):
        """Initialize the class and set the HELIUS_URL and HELIUS_TX_URL."""
        if cls.check_env_vars():
            cls.HELIUS_URL = cls.get_helius_wss_url()
            cls.HELIUS_TX_URL = cls.get_helius_tx_url()

