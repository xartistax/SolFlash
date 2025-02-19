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
    # Return the single-line formatted message instead of printing it
    return alert_message


def cyan_message(message: str) -> str:
    """Returns the message formatted in cyan color for terminal output."""
    CYAN = "\033[96m"
    RESET = "\033[0m"
    return f"{CYAN}{message}{RESET}"




