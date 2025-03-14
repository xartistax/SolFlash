from babel.numbers import format_number
from utils.time_ago import time_ago

def extract_token_data(token):
    """
    Extracts and formats token data from the provided API response.

    This function ensures the safe extraction of token data such as the token name, 
    symbol, market cap, price, volume, creation time, and social links from a raw 
    token response. It formats the values appropriately and provides defaults 
    when necessary.

    Args:
        token (dict): The token data dictionary, typically from an API response.

    Returns:
        dict: A dictionary containing the extracted and formatted token data.

    Example:
        token_data = extract_token_data(api_response)
        # Returns a dictionary with formatted token details such as name, symbol, etc.
    """
    
    # Social Links extraction
    social_links = "No Socials"
    info = token.get("info", {})  # Ensure 'info' is at least an empty dict
    socials = info.get("socials", [])

    # Ensure socials is a valid list and format the social links string
    if isinstance(socials, list) and socials:
        social_links = " | ".join(
            [f"[{s.get('type', 'Unknown').capitalize()}]({s.get('url', '#')})" for s in socials if "type" in s and "url" in s]
        )
    # Check if the `pairCreatedAt` field exists and is valid
    created_at = token.get("pairCreatedAt", None)
    if created_at:
        created_time = time_ago(created_at)  # Assuming `time_ago` works with timestamps
    else:
        created_time = "Unknown"  # Default if missing


    print(token)

    # Extract and format data safely
    return {
        "address": token.get("baseToken", {}).get("address", "Unknown"),
        "name": token.get("baseToken", {}).get("name", "Unknown"),
        "symbol": token.get("baseToken", {}).get("symbol", "Unknown"),
        "market_cap": float(token.get("marketCap", 0) or 0),  # Handle None safely
        "price_usd": float(token.get("priceUsd", 0) or 0),  # Ensure numeric value
        "volume_5m": token.get("volume", {}).get("m5", "N/A"),
        "price_change_5m" : token.get("priceChange", {}).get("m5", 0),
        "txn_buy_5min" : token.get("txns", {}).get("m5", {}).get("buys", 0),
        "txn_sell_5min": token.get("txns", {}).get("m5", {}).get("sells", 0),
        "liquidity_usd" : token.get("liquidity", {}).get("usd", 0),
        "fdv": token.get("fdv", 0),
        "url": token.get("url", "N/A"),
        "created": created_time,
        "created_raw": token.get("pairCreatedAt"),
        "social_links": social_links  # Default value, will update if available
        

        

    }
