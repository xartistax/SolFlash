from settings import COINFILTER, RUGCHECK
from settings.coinFiler.coinFilter import CoinFilter
from settings.rugcheck.rugcheck import RugCheck


RUG_CHECKER = RugCheck(enabled=RUGCHECK["ENABLED"], is_rugged=RUGCHECK["IS_RUGGED"], is_pumpFun=RUGCHECK["IS_PUMPFUN"], risks=RUGCHECK["RISK"])
COIN_FILTER = CoinFilter(
    enabled=COINFILTER["ENABLED"], 
    min_marketcap=COINFILTER["MIN_MCAP"], 

    min_volume_5m=COINFILTER["MIN_VOL_5M"],


    blacklist=COINFILTER["BLACKLIST"],  # Ensure this is passed
    whitelist=COINFILTER["WHITELIST"],
    min_pair_created_at=COINFILTER["TIME_AGO"],
    min_buys_5m=COINFILTER["MIN_BUYS_5M"],
    min_buy_sell_ratio=COINFILTER["MIN_BUY_SELL_RATIO"],
    max_sells_5m=COINFILTER["MAX_SELLS_5M"],
    socials=COINFILTER["SOCIALS"],
    min_price_change_5m=COINFILTER["MIN_PRICE_CHANGE_5M"],
    min_liquidity_usd=COINFILTER["MIN_LIQUIDITY_USD"],
    max_fdv_ratio=COINFILTER["MAX_FDV_RATIO"],




    
    
    )



