import time
from typing import Union
from app_config.app_config import AppConfig
from settings.settings import RUGCHECK
from utils.rug_check_api_call import rug_check_api_call
from services.logger import setup_logger

logger = setup_logger("RUGCHECK")


async def check_rug_pull(token_mint: str) -> Union[bool, dict]:
    """
    This function checks if RugCheck is enabled and fetches the rug check data
    for a token. If RugCheck is disabled or the API call fails, it returns False
    (indicating an issue). If the API call is successful, it returns a detailed
    report.
    """

    # If RugCheck is disabled, return False, as we cannot perform the check
    if not RUGCHECK:
        return False
    
    try:
        # Perform the first API call to get the full report
        rug_check_report = rug_check_api_call(token_mint, False)
        
        # Check if the first API call failed
        if not rug_check_report.get("success"):
            logger.error("Failed to fetch RugCheck full report.")
            return False
        
        # Respect the rate limit before making the second API call
        # Example: Sleep for 1 second (adjust based on API rate limits)
        time.sleep(  AppConfig.APICLIENT.get("TIMEOUT") / 1000  )  # Replace with your rate limit logic if needed
        
        # Perform the second API call to get the summary
        rug_check_summary = rug_check_api_call(token_mint)
        
        # Check if the second API call failed
        if not rug_check_summary.get("success"):
            logger.error("Failed to fetch RugCheck summary.")
            return False
        
        # Extract response data from the successful API calls
        data_report = rug_check_report.get("response", {})
        data_summary = rug_check_summary.get("response", {})
        
        # Build the token-related information
        token = {
            "rugged": data_report.get("rugged", {}),
            "token_info": data_report.get("token", {}),
            "token_meta": data_report.get("tokenMeta", {}),
            "top_holders": data_report.get("topHolders", []),
            "markets": data_report.get("markets", [])
        }
        
        # Build the risk-related information
        risk = {
            "tokenProgram": data_summary.get("tokenProgram", ""),
            "tokenType": data_summary.get("tokenType", ""),
            "risks": [
                {
                    "name": r.get("name", ""),
                    "value": r.get("value", ""),
                    "description": r.get("description", ""),
                    "score": r.get("score", 0),
                    "level": r.get("level", "")
                }
                for r in data_summary.get("risks", [])
            ],
            "score": data_summary.get("score", 0)
        }

        # Prepare the final report
        report = {
            "data": {
                "risk": risk,
                "token": token,
                "rugged": token.get("rugged", True)
            }
        }
    
    except KeyError as e:
        logger.error(f"No Key: {e}")
        return False
    except TypeError as e:
        logger.error(f"Unexpected API-Response: {e}")
        return False
    except Exception as e:
        logger.exception(f"Error during RugCheck: {e}")
        return False

    # Return the detailed report if everything checks out
    return report