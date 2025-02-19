from app_config.app_config import AppConfig

def extract_token_address(addresses):
    """
    Extracts token addresses from a list of addresses, filtering out the system address.

    This function filters out any addresses that match the system-defined 'wsol_pc_mint' address 
    which is stored in the application configuration. Only non-system token addresses are returned.

    Args:
        addresses (list): A list of token addresses to filter.

    Returns:
        list: A list containing the filtered token addresses, excluding the system address.

    Example:
        addresses = ["addr1", "addr2", AppConfig.LIQUIDITY_POOL["wsol_pc_mint"], "addr4"]
        result = extract_token_address(addresses)
        # result will be ["addr1", "addr2", "addr4"]
    """
    # Filter out the system address defined in the application config
    return [addr for addr in addresses if addr != AppConfig.LIQUIDITY_POOL["wsol_pc_mint"]]
