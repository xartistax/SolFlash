from services.api_client import APIClient

from services.env import ConfigENV
from services.logger import setup_logger
from utils.cyan_message import cyan_message

def rug_check_api_call(mint_address: str, summary=True):
    """
    Calls the RugCheck API to fetch either summary or detailed report of a token.

    Args:
        mint_address (str): The mint address of the token to check.
        summary (bool): If True, fetches summary data; otherwise, fetches the detailed report.

    Returns:
        dict: A dictionary containing the success status, response data, and status code.
    """
    logger = setup_logger()

    # Build the RugCheck API URL based on environment configuration
    rug_check_api = ConfigENV.ENV["RUGCHECK_API"].rstrip("/")  # Remove trailing slash
    rug_check_route = (
        ConfigENV.ENV["RUGCHECK_TOKEN_ROUTE_SUMMARY"].lstrip("/") 
        if summary 
        else ConfigENV.ENV["RUGCHECK_TOKEN_ROUTE_REPORT"].lstrip("/")  # Remove leading slash
    )
    rug_check_url = f"{rug_check_api}/{rug_check_route.format(mint=mint_address)}"



    # Initialize API client with rate limiting and retries
    api_client = APIClient(rate_limit=10, time_window=60, max_retries=6)





    try:
        # Send GET request to RugCheck API
        response_data, status_code = api_client.get(rug_check_url)

        # Check if response data is empty or None
        if not response_data:
            logger.debug(f"No data found for mint address {mint_address}")
            return {"success": False, "status_code": status_code}

        logger.debug(f"Found data for mint address {mint_address}")
        return {"success": True, "response": response_data, "status_code": status_code}

    except Exception as e:
        # Log any exceptions that occur during the API request
        logger.error(f"Error while fetching data for mint address {mint_address}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
