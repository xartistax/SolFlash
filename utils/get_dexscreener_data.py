from services.logger import setup_logger
from settings.filters import COIN_FILTER, RUG_CHECKER
from utils.cyan_message import cyan_message
from utils.dexscreener_api_call import dexscreener_api_call
from utils.process_token import process_token

logger = setup_logger("DEXSCREENER DATA")

async def get_dexscreener_data(token: str):
    """
    Fetches token data from DexScreener for a given token, processes the data, and checks for any rug-pull indicators.

    Args:
        token (str): The token address or mint address to fetch data for.

    Returns:
        dict or None: The first response from DexScreener if successful, else None.
    """

    if not token:
        logger.warning("Invalid token provided. Skipping...")
        return None

    logger.debug(f"Fetching DexScreener data for Token: {token}...")

    try:
        data = dexscreener_api_call(token)
        if not data:
            logger.error(f"Token {token} - API response is None. Skipping...")
            return None
        
        success = data.get("success")
        if not success:
            logger.error(f"Token {token} - DexScreener API call failed. Response: {data}")
            return None

        response = data.get("response")
        if not response:
            logger.error(f"Token {token} - Empty 'response' field. Skipping...")
            return None

        first_response = response[0] if response else None
        if not first_response:
            logger.error(f"Token {token} - No data found in the first response. Skipping...")
            return None

        logger.debug(f"Token {token} - Successfully fetched DexScreener data.")
        return first_response

    except Exception as e:
        logger.error(f"Token {token} - Unexpected error while fetching DexScreener data: {e}", exc_info=True)
        return None
