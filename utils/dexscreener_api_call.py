from services.api_client import APIClient
from services.env import ConfigENV
from services.logger import setup_logger
from utils.cyan_message import cyan_message

logger = setup_logger("DEXSCREENER CALL")


def dexscreener_api_call(mint_address: str):
    
    """
    Fetches token data from the DexScreener API based on the provided mint address.

    This function constructs the URL for the DexScreener API using the provided mint address, 
    fetches the data using a rate-limited API client, and returns a response indicating 
    whether the data was successfully retrieved.

    Args:
        mint_address (str): The mint address of the token to retrieve data for.

    Returns:
        dict: A dictionary containing the success status, the response data if available,
              and the HTTP status code.
              Example:
                {
                    "success": True,
                    "response": <response_data>,
                    "status_code": <status_code>
                }
                or
                {
                    "success": False,
                    "status_code": <status_code>
                }

    Raises:
        Any exceptions raised by the API client during the request will be logged but 
        not re-raised in this function.

    Notes:
        - The function uses a rate-limited API client that allows 10 requests per minute 
          with a maximum of 3 retries in case of failure.
        - The DexScreener API URL is fetched from the environment configuration and formatted 
          using the mint address.
    """
    # Fetch the DexScreener API URL from the environment variable and remove trailing slash
    dexscreener_api = ConfigENV.ENV["DEXSCREENER_API"].rstrip("/")  # Remove trailing slash

    # Format the URL with the mint address
    dexscreener_url = f"{dexscreener_api.format(mint=mint_address)}"

    # Initialize the API client with rate limit and retry settings
    api_client = APIClient(rate_limit=10, time_window=60, max_retries=6)

    try:
        # Make the API call and get both the response data and status code
        response_data, status_code = api_client.get(dexscreener_url)

        # If data is found, log it and return the success response
        if response_data:
            logger.debug(f"Found data for mint address {mint_address}")
            return {"success": True, "response": response_data, "status_code": status_code}
        else:
            # Log the warning if no data is found for the mint address
            logger.warning(f"No data found for mint address {mint_address}")
            return {"success": False, "status_code": status_code}

    except Exception as e:
        # Log any exceptions that occur during the request
        logger.error(f"Error during API call to DexScreener for mint address {mint_address}: {e}")
        return {"success": False, "status_code": 500}  # Return failure with status code 500 in case of error
