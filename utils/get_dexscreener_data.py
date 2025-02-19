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
        rugcheck (bool): Flag to determine whether to perform a rug-check validation on the token.

    Returns:
        None: The function processes the token data and logs results or errors.
    """

    # Fetch data from DexScreener API
    data = dexscreener_api_call(token)
    success = data.get("success")

    
    
    # Check if the data is None or if the 'success' key is missing
    if not data or not success:
        logger.error(f"Error fetching DexScreener data for token: {token}")
        return
    
    response = data.get("response")
    if not response:
        logger.error(f"No valid response found for token: {token}")
        return 

    first_response = response[0]

    # Check if first_response is None or empty
    if not first_response:
        logger.error(f"No data found for the first response of token: {token}")
        return 
    

    if COIN_FILTER.enabled:
        if not COIN_FILTER.is_valid(first_response):
            logger.warning(f"Token {token} failed the filter checks")
            return

    # Process token if valid
    process_token(response)