class AppConfig:

    BOTNAME = "SOLFLASH"

    MAINNET = True
    
    PAPER_TRADER = {
        "ENABLED": True,
        "SETTINGS" : {
            "initial_balance": 1000,  # Startkapital in USDC
            "slippage_pct": 0.5,  # Slippage in Prozent
            "fee_pct": 0.3,  # Handelsgebühr in Prozent
            "market_prices": {"SOL": 100, "BTC": 45000, "ETH": 3000}  # Simulierte Marktpreise
        }
    }

    LOGGER = {
        "LOG_DIR": "logs",
        "LEVEL": "WARNING"  # Change to DEBUG, INFO, WARNING, ERROR, or CRITICAL as needed
    }


    APICLIENT = {
        "TIMEOUT": 3000,  # Timeout for API requests in milliseconds
        "RETRY_DELAY": 10000,  # Initial delay between retries (in milliseconds) for rate-limited responses (429)
        "MAX_RETRIES": 6,  # Maximum number of retries when a 429 status code (Too Many Requests) is encountered
        "RATE_LIMIT": 30,  # Maximum number of requests allowed in the given time window
        "TIME_WINDOW": 60,  # Time window in seconds (you might want to extend this to 60 seconds)
    }



    DEXSCREENER = {
        "MAX_RETRIES" : 10,
        "FETCH_DELAY" : 30000
    }

    TX = {
        "FETCH_TX_MAX_RETRIES": 1000,
        "FETCH_TX_INITIAL_DELAY": 3000,
        "TIMEOUT": 10000
    }

    LIQUIDITY_POOL = {
        "RADIYUM_PROGRAM_ID": "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",
        "wsol_pc_mint": "So11111111111111111111111111111111111111112",
        "COMMITMENT": "processed"
    }

    TELEGRAM = {
        "ENABLED" : False
    }

    

    



