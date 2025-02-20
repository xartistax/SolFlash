RUGCHECK = {
    "ENABLED": False,  # If False, rug check is disabled, and all tokens are accepted.
    "IS_RUGGED": True,  # If True, identifies tokens that have already rugged.
    "IS_PUMPFUN": True,  # If True, detects pump-and-dump tokens.

    "RISK": {
        "Copycat token": {
            "enabled": False,  # If True, filters out tokens that are clones of existing projects.
            "score_threshold": 500  # The risk score above which the token is considered a copycat.
        },
        "Low amount of LP Providers": {
            "enabled": True,  # If True, flags tokens with too few liquidity providers (higher risk).
            "score_threshold": 0  # Minimum risk score needed to trigger this filter.
        },
        "Mutable metadata": {
            "enabled": False,  # If True, flags tokens with metadata that can still be changed (potential scam).
            "score_threshold": 600  # The risk score above which this condition is considered dangerous.
        },
        "Single holder ownership": {
            "enabled": False,  # If True, filters tokens where one wallet holds most of the supply.
            "score_threshold": 700  # The risk score threshold for single-holder risk.
        },
        "Low Liquidity": {
            "enabled": False,  # If True, flags tokens with insufficient liquidity (high rug risk).
            "score_threshold": 300  # Minimum liquidity risk score for flagging.
        },
        "High holder concentration": {
            "enabled": False,  # If True, flags tokens where a few wallets hold most of the supply.
            "score_threshold": 800  # The risk score threshold for holder concentration risk.
        },
    }
}


# If whitelist is empty, the system ignores it and only applies the blacklist.
# If whitelist is not empty, the system only allows tokens from that list.
# If both are defined, whitelist takes priority (tokens must be whitelisted and not blacklisted).



COINFILTER = {
    "ENABLED": True,
    "SOCIALS": True,
    "MIN_MCAP": 25_000,             # Minimum market cap to avoid micro-cap scams
    "MIN_VOL_5M": 5_000,              # Minimum volume to ensure liquidity
    "MIN_LIQUIDITY_USD": 10_000,     # Stellt sicher, dass Coins genug Liquidität haben  
    "MAX_FDV_RATIO": 3,              # Vermeidet Coins mit überhöhter Fully Diluted Valuation (FDV)  
    "MIN_PRICE_CHANGE_5M": 2.5,    # The price change in the last 5 minutes (in percentage).,
    "BLACKLIST": [
        "pepe", "shiba", "inu", "doge", "elon", "baby", "floki", "moon", "pump",  
        "shit", "scam", "safe", "bonk", "bobo", "pink", "kitty", "wojak", "rug",  
        "100x", "1000x", "next", "whale", "diamond", "hands", "ape", "pajeet",  
        "yolo", "fomo", "rekt", "bsc", "degen", "casino", "metaverse", "nft", "porn",  
        "bet", "gamb", "casino", "play", "web3", "rekt", "loser", "rich", "trust",  
        "sol", "eth", "bnb", "btc"  # (Prevents fake versions of major cryptos)
],
    "WHITELIST": [],          
    "TIME_AGO": 48 * 60 * 60 * 1000,      # Shorter time frame to catch fresh pumps
    "MIN_BUYS_5M": None,             # More buys in 5 min indicates bullish momentum
    "MIN_BUY_SELL_RATIO": 1,      # More aggressive buy ratio for strong uptrends
    "MAX_SELLS_5M": None,         # Lower max sells to avoid coins with early dumpers
}

