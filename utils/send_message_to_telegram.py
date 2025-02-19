from services.api_client import APIClient
from services.env import ConfigENV
from utils.extract_token_data import extract_token_data
from utils.time_ago import time_ago
from services.logger import setup_logger

logger = setup_logger("WEBSOCKET")

def send_message_to_telegram(token):
    """
    Sends a formatted message to Telegram with information about the token.

    Args:
        token (dict): The token data to extract and send to Telegram.

    Returns:
        dict: A dictionary indicating success or failure, including the response and status code.
    """
    telegram_url = ConfigENV.ENV["TELEGRAM_URL"].rstrip("/").format(method="sendMessage")  # Remove trailing slash
    telegram_id = ConfigENV.ENV["TELEGRAM_CHAT"]

    try:
        # Extract token data
        token_data = extract_token_data(token)

        # Format the message with token information
        message = f"""
        🚀 <b>New Token Detected!</b>  
        🏷️ <b>Name:</b> {token_data["name"]}  
        🔤 <b>Symbol:</b> {token_data["symbol"]}  
        💰 <b>MarketCap:</b> {token_data["market_cap"]} USD  
        📈 <b>Price:</b> {token_data["price_usd"]} USD  
        📊 <b>Volume (5m):</b> {token_data["volume_5m"]} USD  
        🔗 <b>[DexScreener]({token_data["url"]})</b> | {token_data["social_links"]}  
        🕒 <b>Created:</b> {time_ago(token_data["created"])}  
        """

        # Initialize API client and send the message to Telegram
        api_client = APIClient()
        
        response_data, status_code = api_client.post(
            telegram_url, 
            {
                "chat_id": telegram_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
        )  # Receive both response data and status code

        # Check if the message was sent successfully
        if not response_data:
            logger.warning("Failed to send Telegram message.")
            return {"success": False, "status_code": status_code}

        logger.debug("Telegram message sent successfully.")
        return {"success": True, "response": response_data, "status_code": status_code}

    except Exception as e:
        # Log unexpected errors and return failure
        logger.error(f"Error while sending message to Telegram: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
