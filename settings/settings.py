RUGCHECK = {
    "ENABLED": False,
    "IS_RUGGED": True,
    "IS_PUMPFUN": True,
    "RISK": {
        "Copycat token": {"enabled": False, "score_threshold": 500},
        "Low amount of LP Providers": {"enabled": True, "score_threshold": 0},
        "Mutable metadata": {"enabled": False, "score_threshold": 600},
        "Single holder ownership": {"enabled": False, "score_threshold": 700},
        "Low Liquidity": {"enabled": False, "score_threshold": 300},
        "High holder concentration": {"enabled": False, "score_threshold": 800},
    }
}

COINFILTER = {
    "ENABLED": True,
    "MIN_MCAP": 50_000,
    "MIN_VOL": 0
}