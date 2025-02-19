from settings import COINFILTER, RUGCHECK
from settings.coinFiler.coinFilter import CoinFilter
from settings.rugcheck.rugcheck import RugCheck


RUG_CHECKER = RugCheck(enabled=RUGCHECK["ENABLED"], is_rugged=RUGCHECK["IS_RUGGED"], is_pumpFun=RUGCHECK["IS_PUMPFUN"], risks=RUGCHECK["RISK"])
COIN_FILTER = CoinFilter(enabled=COINFILTER["ENABLED"], min_marketcap=COINFILTER["MIN_MCAP"], min_volume=COINFILTER["MIN_VOL"])