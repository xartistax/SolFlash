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
        "LEVEL": "INFO"  # Change to DEBUG, INFO, WARNING, ERROR, or CRITICAL as needed
    }

    APICLIENT = {
        "TIMEOUT": 10000,  # Timeout for API requests in milliseconds
        "RETRY_DELAY": 3000,  # Initial delay (in milliseconds) between retries for rate-limited responses (429)
        "MAX_RETRIES": 5,  # Maximum number of retries when a 429 status code (Too Many Requests) is encountered
        "RATE_LIMIT": 10,  # Maximum number of retries when a 429 status code (Too Many Requests) is encountered
        "TIME_WINDOW": 6
    
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

    

    



