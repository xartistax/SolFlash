import asyncio
from app_config.app_config import AppConfig
from services.logger import setup_logger

from settings.filters import RUG_CHECKER
from utils.cyan_message import cyan_message
from utils.check_rug_pull import check_rug_pull
from utils.extract_token_address import extract_token_address
from utils.fetch_transaction_details import fetch_transaction_details
from utils.get_dexscreener_data import get_dexscreener_data

logger = setup_logger("TRANSACTIONS")

async def handle_transaction(signature: str):
    """
    Handles a transaction by extracting token data, performing a rug check, and fetching additional data
    from DexScreener with retries in case of failure.

    Args:
        signature (str): The signature of the transaction to process.

    Returns:
        None: This function performs various checks and actions, but does not return any data.
    """
    max_retries = AppConfig.DEXSCREENER.get("MAX_RETRIES", 3)  # Default max retries to 3 if not set
    fetch_delay = (AppConfig.DEXSCREENER.get("FETCH_DELAY", 1000)) / 1000  # Default delay 1000ms

    try:
        # Fetch transaction details asynchronously
        tokens = await fetch_transaction_details(signature)
        if not tokens:
            logger.warning(f"Signature {signature[:6]} - No tokens found in transaction. Skipping...")
            return
        
        # Extract token addresses
        try:
            token_addresses = extract_token_address(tokens)
            if not token_addresses:
                logger.warning(f"Signature {signature[:6]} - Could not extract token address. Skipping...")
                return
        except (TypeError, KeyError, IndexError) as e:
            logger.error(f"Signature {signature[:6]} - Error extracting token address: {e}")
            return

        logger.info(f"Signature {signature[:6]} - Extracted token addresses: {token_addresses}")

        # Take the first token address for processing (assuming it's the target)
        token = token_addresses[0]

        # Perform rug check
        rugcheck = await check_rug_pull(token)

        if not rugcheck:
            logger.warning(f"Token {token} - Rug check failed, skipping...")
            return

        if not RUG_CHECKER.is_valid(token, rugcheck):
            logger.warning(f"Token {token} failed the rug pull check and is skipped.")
            return
        
        
        # Retry logic for fetching DexScreener data
        for attempt in range(1, max_retries + 1):
            try:
                await get_dexscreener_data(token)  # Fetch token data from DexScreener
                break  # Exit retry loop on success
            except (KeyError, ValueError, TypeError, ConnectionError) as e:

                logger.error(f"Signature {signature[:6]} - Error fetching DexScreener data (Attempt {attempt}): {e}")

                if attempt < max_retries:
                    await asyncio.sleep(fetch_delay)  # Wait before retrying
                else:
                    logger.error(f"Signature {signature[:6]} - Max retries reached for DexScreener data.")
                    return None

    except Exception as e:
        # Log unexpected errors and re-raise for debugging
        logger.error(f"Signature {signature[:6]} - Unexpected error: {e}", exc_info=True)
        raise  # Re-raise for potential debugging outside the function























