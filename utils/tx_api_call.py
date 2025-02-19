from app_config.app_config import AppConfig
from services.api_client import APIClient
from services.logger import setup_logger
from services.env import ConfigENV

logger = setup_logger("TRANSACTION API CALL")

def tx_api_call(signature: str):
    """
    Fetches transaction details from the Helius transaction API for a given signature.
    It handles retries, response validation, and logging.

    Args:
        signature (str): The transaction signature to fetch details for.

    Returns:
        dict: A dictionary containing the success status, response data, and status code.
    """
    tx_url = ConfigENV.HELIUS_TX_URL

    api_client = APIClient(
        rate_limit=AppConfig.APICLIENT.get("RATE_LIMIT") , 
        time_window=AppConfig.APICLIENT.get("TIME_WINDOW"),
        max_retries=AppConfig.APICLIENT.get("MAX_RETRIES"))

    try:
        # Make API request
        response_data, status_code = api_client.post(
            tx_url,
            {
                "transactions": [signature],
                "commitment": "finalized",
                "encoding": "jsonParsed"
            }
        )  # Receive both response data and status code

        # Check if response data is empty or invalid
        if not response_data:
            logger.warning(f"Signature: {signature[:6]} - No transaction data found. Skipping...")
            return {"success": False, "status_code": status_code}

        logger.debug(f"Signature: {signature[:6]} - Found transaction data. Processing further.")
        return {"success": True, "response": response_data, "status_code": status_code}

    except Exception as e:
        logger.error(f"Signature: {signature[:6]} - Error while fetching transaction data: {e}")
        return {"success": False, "error": str(e)}
