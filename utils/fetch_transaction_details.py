import time
from app_config.app_config import AppConfig
from services.logger import setup_logger
from utils.tx_api_call import tx_api_call

logger = setup_logger("FETCH TRANSACTION")

async def fetch_transaction_details(signature: str) -> dict | None:
    """
    Fetches transaction details from Helius for a given signature.
    Retries the request up to 'max_retries' times if it fails.
    
    This function makes an API call to fetch transaction details for a specific signature.
    It checks for the presence of Raydium instructions and token transfers and returns the token information.

    Args:
        signature (str): The transaction signature to fetch details for.

    Returns:
        dict | None: A list of token mint addresses if Raydium instructions are found,
                     otherwise None if the transaction does not match expected criteria.
    """

    # Try to fetch the transaction details, retrying up to 'max_retries' times if necessary
    try:
        # Fetch transaction data
        tx_data_raw = tx_api_call(signature)

        if not tx_data_raw.get("success"):
            logger.info(f"Signature: {signature[:6]} - Failed to fetch transaction data. Retrying...")

        transaction_data = tx_data_raw.get("response")
        if not transaction_data:
            logger.info(f"Signature: {signature[:6]} - No transaction data found!")
            return None

        first_transaction_data = transaction_data[0]

        # Check if the transaction has instructions
        instructions = first_transaction_data.get("instructions", [])
        if not instructions:
            logger.info(f"Signature: {signature[:6]} - No instructions found in the transaction! Skipping...")
            return None

        # Find Raydium instructions
        ray_id = AppConfig.LIQUIDITY_POOL["RADIYUM_PROGRAM_ID"]
        matched_instructions = next((ix for ix in instructions if ix.get("programId") == ray_id), None)

        if not matched_instructions:
            logger.info(f"Signature: {signature[:6]} - No Raydium instructions found in the transaction! Skipping...")
            return None

        # Extract token mint addresses from tokenTransfers
        token = [transfer['mint'] for transfer in first_transaction_data.get('tokenTransfers', [])]

        # Return token data if available
        if token:
            return token

        logger.info(f"Signature: {signature[:6]} - No token transfer found in the transaction!")
        return None

    except ValueError as e:
        logger.error(f"Signature: {signature[:6]} - Data validation failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Signature: {signature[:6]} - Unexpected error: {e}")
        return None
