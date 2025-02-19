from services.logger import setup_logger

logger = setup_logger("TOKEN PRINT")

def print_token_alert(token_data):
    """Generates a formatted alert message for new tokens in a single line."""


    
    # Construct the formatted message in one line
    alert_message = (
        f"Address: {token_data['address']} | "
        f"Name: {token_data['name']} | "
        f"Symbol: {token_data['symbol']} | "
        f"MarketCap: {token_data['market_cap']} | "
        f"Created: {token_data['created']} | "
        f"Volume (5m): {token_data['volume_5m']} USD | "
        f"DexScreener URL: {token_data['url']} | "
        f"Socials: {token_data['social_links']}"
    )

    # Return the single-line formatted message
    return alert_message
