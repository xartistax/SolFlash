import asyncio
from app_config.app_config import AppConfig
from services.logger import setup_logger

from settings.filters import RUG_CHECKER, COIN_FILTER
from settings.settings import RUGCHECK
from utils.is_token_in_file import is_token_in_file
from utils.cyan_message import cyan_message
from utils.check_rug_pull import check_rug_pull
from utils.extract_token_address import extract_token_address
from utils.fetch_transaction_details import fetch_transaction_details
from utils.get_dexscreener_data import get_dexscreener_data
from utils.process_token import process_token

logger = setup_logger("TRANSACTIONS")


# Define the max retry attempts and delay (in seconds) between retries


async def handle_transaction(signature: str):
    """
    Handles a transaction by extracting token data, performing a rug check, and fetching additional data
    from DexScreener with retries in case of failure.

    Args:
        signature (str): The signature of the transaction to process.

    Returns:
        None: This function performs various checks and actions, but does not return any data.
    """

    dexscreener_data = None
    rugcheck_enabled = RUGCHECK.get("ENABLED")
    rugcheck_data = None
    MAX_RETRIES = AppConfig.APICLIENT.get("MAX_RETRIES")
    RETRY_DELAY = AppConfig.APICLIENT.get("RETRY_DELAY")

    try:
        # Fetch transaction details asynchronously
        tokens = await fetch_transaction_details(signature)

        if not tokens:
            logger.info(f"Signature {signature[:6]} - No tokens found in transaction. Skipping...")
            return
        
        # Extract token addresses
        try:
            token_addresses = extract_token_address(tokens)
            if not token_addresses:
                logger.info(f"Signature {signature[:6]} - Could not extract token address. Skipping...")
                return
        except (TypeError, KeyError, IndexError) as e:
            logger.error(f"Signature {signature[:6]} - Error extracting token address: {e}")
            return
        
        token = token_addresses[0]

        # Perform DB Check
        logger.debug(f"Token {token} - Checking if already logged...")
        if is_token_in_file(token):
            logger.debug(f"Token {token} is already logged. Skipping...")
            return

        # Check if rugcheck is enabled
        if rugcheck_enabled:
            rugcheck_data = await check_rug_pull(token)

            if not RUG_CHECKER.is_valid(token, rugcheck_data):
                logger.debug(f"Token {token} failed the rug pull check and is skipped.")  
                return  # Return only if the token fails the rug check
        
        # Retry logic for DexScreener data
        retries = 0
        while retries < MAX_RETRIES:
            try:
                dexscreener_data = await get_dexscreener_data(token)

                if dexscreener_data is not None:
                    break  # Exit the loop if DexScreener data is valid
                else:
                    logger.debug(f"DexScreener Data for Token {token} is None. Retrying... ({retries + 1}/{MAX_RETRIES})")
                    retries += 1
                    if retries < MAX_RETRIES:
                        await asyncio.sleep(RETRY_DELAY)  # Wait before retrying
                    else:
                        logger.debug(f"Max retries reached for Token {token}. Skipping...")
                        return  # Exit if max retries reached

            except (KeyError, ValueError, TypeError, ConnectionError) as e:
                logger.error(f"Signature {signature[:6]} - Error fetching DexScreener data: {e}")
                return  # Return to prevent processing an invalid token

        if not COIN_FILTER.is_valid(dexscreener_data):
            logger.debug(f"Token {token} failed the coin filter check and is skipped.")  
            return

        process_token(dexscreener_data)
        
    except Exception as e:
        # Log unexpected errors and re-raise for debugging
        logger.error(f"Signature {signature[:6]} - Unexpected error: {e}", exc_info=True)
        raise  # Re-raise for potential debugging outside the function