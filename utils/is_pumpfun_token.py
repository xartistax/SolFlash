def is_pumpfun_token(token_address: str) -> bool:
    """
    Check if the given token address is a Pump.fun token.
    
    Pump.fun tokens typically have 'pump' at the end of their address.
    """
    return token_address.lower().endswith("pump")