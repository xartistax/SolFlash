from app_config.app_config import AppConfig
from services.api_client import APIClient
from services.env import ConfigENV
from services.logger import setup_logger
from utils.cyan_message import cyan_message
from requests.exceptions import RequestException, HTTPError, Timeout




def rug_check_api_call(mint_address: str, summary=True):
    """
    Calls the RugCheck API to fetch either summary or detailed report of a token.

    Args:
        mint_address (str): The mint address of the token to check.
        summary (bool): If True, fetches summary data; otherwise, fetches the detailed report.

    Returns:
        dict: A dictionary containing the success status, response data, and status code.
    """
    logger = setup_logger("RUGCHECK API CALL")

    # Validate mint address before proceeding
    if not mint_address or not mint_address.strip():
        logger.warning("Invalid mint address provided.")
        return {"success": False, "error": "Invalid mint address", "status_code": 400}

    # Build the RugCheck API URL safely
    try:
        rug_check_api = ConfigENV.ENV["RUGCHECK_API"].rstrip("/")
        rug_check_route = (
            ConfigENV.ENV["RUGCHECK_TOKEN_ROUTE_SUMMARY"].lstrip("/")
            if summary
            else ConfigENV.ENV["RUGCHECK_TOKEN_ROUTE_REPORT"].lstrip("/")
        )
        rug_check_url = f"{rug_check_api}/{rug_check_route.format(mint=mint_address)}"
    except KeyError as e:
        logger.error(f"Missing environment configuration key: {e}")
        return {"success": False, "error": f"Missing config key: {e}", "status_code": 500}

    # Initialize API client
    api_client = APIClient(
        rate_limit=AppConfig.APICLIENT.get("RATE_LIMIT"),
        time_window=AppConfig.APICLIENT.get("TIME_WINDOW"),
        max_retries=AppConfig.APICLIENT.get("MAX_RETRIES"),
    )

    try:
        response_data, status_code = api_client.get(rug_check_url)
        
        if status_code == 400:
            logger.error(f"RugCheck API returned 400 Bad Request for mint address: {mint_address}")
            return {"success": False, "error": "Bad request", "status_code": 400}
        
        if status_code == 429:
            logger.warning(f"Rate limit exceeded for RugCheck API while fetching {mint_address}")
            return {"success": False, "error": "Rate limit exceeded", "status_code": 429}
        
        if not response_data:
            logger.warning(f"No data found for mint address {mint_address}")
            return {"success": False, "error": "No data found", "status_code": status_code}
        
        logger.info(f"Successfully fetched data for mint address {mint_address}")
        return {"success": True, "response": response_data, "status_code": status_code}
    
    except Timeout:
        logger.error(f"Request timed out while fetching RugCheck report for {mint_address}")
        return {"success": False, "error": "Request timed out", "status_code": 408}
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred for {mint_address}: {http_err}")
        return {"success": False, "error": str(http_err), "status_code": 500}
    except RequestException as req_err:
        logger.error(f"Request error occurred for {mint_address}: {req_err}")
        return {"success": False, "error": str(req_err), "status_code": 500}
    except Exception as e:
        logger.exception(f"Unexpected error while fetching RugCheck report for {mint_address}: {e}")
        return {"success": False, "error": "An unexpected error occurred", "status_code": 500}
