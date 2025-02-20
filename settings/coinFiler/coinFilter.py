import re
from services.logger import setup_logger
from utils.time_ago import time_ago
from utils.cyan_message import cyan_message
from datetime import datetime, timezone

logger = setup_logger("COINFILTER")

class CoinFilter:
    def __init__(
        self,
        enabled=True,
        min_marketcap=None,
        max_marketcap=None,
        min_volume=None,
        max_volume=None,
        blacklist=None,
        whitelist=None,
        min_pair_created_at=None,
        min_buys_5m=None,
        max_sells_5m=None,
        min_buy_sell_ratio=None,
        socials=None,
        min_price_change_5m=None,

        #new values to filter
        min_liquidity_usd=None,
        max_fdv_ratio=None,
        min_holder_count=None,
        no_renounced_contracts=True,

    ):
        self.enabled = enabled
        self.min_marketcap = min_marketcap
        self.max_marketcap = max_marketcap
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.blacklist = set(blacklist) if blacklist else set()
        self.whitelist = set(whitelist) if whitelist else set()
        self.min_pair_created_at = min_pair_created_at
        self.min_buys_5m = min_buys_5m
        self.max_sells_5m = max_sells_5m
        self.min_buy_sell_ratio = min_buy_sell_ratio
        self.socials = socials
        self.min_price_change_5m = min_price_change_5m

        #new values to filter
        self.min_liquidity_usd = min_liquidity_usd
        self.max_fdv_ratio = max_fdv_ratio
        self.min_holder_count = min_holder_count
        self.no_renounced_contracts = no_renounced_contracts



    def is_valid(self, coin):
        """Check if a single coin meets the filter criteria."""
        if not self.enabled:
            logger.warning("Filtering disabled, accepting all coins.")
            return True  
        

    
    
        name = coin.get("baseToken").get("name", "").upper()
        marketcap = coin.get("marketCap", 0)
        volume = coin.get("volume", {}).get("m5", 0)  # Using 5min volume
        pair_created_at = coin.get("pairCreatedAt", 0)
        txn_data = coin.get("txns", {})
        buys_5m = txn_data.get("m5", {}).get("buys", 0)
        sells_5m = txn_data.get("m5", {}).get("sells", 0)
        buys_1h = txn_data.get("h1", {}).get("buys", 0)
        sells_1h = txn_data.get("h1", {}).get("sells", 0)
        price_change_5m = coin.get("priceChange", {}).get("m5", 0)


        socials = None
        if coin.get("info", {}).get("socials", []):
            socials = coin.get("info", {}).get("socials", [])
        

        





        print(
            cyan_message(
            f"Checking coin: name={name}, marketCap={marketcap}, volume={volume}, "
            f"created_at={pair_created_at} ({time_ago(pair_created_at)} ago), "
            f"buys_5m={buys_5m}, sells_5m={sells_5m}, buy/sell ratio_5m={buys_5m / max(sells_5m, 1):.2f}, "
            f"buys_1h={buys_1h}, sells_1h={sells_1h}, buy/sell ratio_1h={buys_1h / max(sells_1h, 1):.2f}"
            )
        )



        # Minimum Liquidity Filter
        liquidity = coin.get("liquidity", {}).get("usd", 0)
        if self.min_liquidity_usd is not None and liquidity < self.min_liquidity_usd:
            logger.warning(f"Rejecting {coin['baseToken']['name']}: Liquidity {liquidity} USD is below min {self.min_liquidity_usd} USD.")
            return False

        # FDV Ratio Filter
        fully_diluted_valuation = coin.get("fdv", 0)
        if self.max_fdv_ratio is not None and marketcap > 0:
            fdv_ratio = fully_diluted_valuation / marketcap
            if fdv_ratio > self.max_fdv_ratio:
                logger.warning(f"Rejecting {coin['baseToken']['name']}: FDV ratio {fdv_ratio:.2f} exceeds max {self.max_fdv_ratio}.")
                return False


   


        # Price change filter (reject if price change is below the threshold)
        if self.min_price_change_5m is not None and price_change_5m < self.min_price_change_5m:
            logger.warning(f"Rejecting {coin['baseToken']['name']}: Price change in last 5 minutes is below {self.min_price_change_5m}% ({price_change_5m}%).")
            return False

        # Social filter check based on the value of self.socials
        if self.socials is not None:  # If SOCIALS is enabled or disabled (True or False)
            if self.socials:  # If SOCIALS is True, check for socials
                if not socials:  # Reject if no socials are found
                    logger.warning(f"Rejecting {coin['baseToken']['name']}: This coin has no Socials!")
                    return False
            else:  # If SOCIALS is False, ensure no socials are present
                if socials:  # Reject if socials are found
                    logger.warning(f"Rejecting {coin['baseToken']['name']}: This coin has Socials, but they are not allowed!")
                    return False

        if (self.min_buys_5m is not None) and (buys_5m < self.min_buys_5m):
            logger.warning(f"Rejecting {coin['baseToken']['name']}: Not enough buys in the last 5 min ({buys_5m}).")
            return False


        if (self.max_sells_5m is not None) and (sells_5m > self.max_sells_5m):
            logger.warning(f"Rejecting {coin['baseToken']['name']}: Too many sells in the last 5 min ({sells_5m}).")
            return False


        if sells_1h > 0 and self.min_buy_sell_ratio is not None:
            if (buys_1h / max(sells_1h, 1)) < self.min_buy_sell_ratio:
                logger.warning(f"Rejecting {coin['baseToken']['name']}: Low buy/sell ratio ({buys_1h}/{sells_1h}).")
                return False
        


        # Whitelist check (only allow listed coins, ignore others)
        if self.whitelist and not any(word.upper() in name for word in self.whitelist):
            logger.warning(f"Rejecting coin: '{name}' not in whitelist.")
            return False


        # Blacklist check (reject if name contains blacklisted word)
        if any(re.search(r'\b' + re.escape(word.upper()) + r'\b', name) for word in self.blacklist):
            logger.warning(f"Rejecting coin: '{name}' contains blacklisted keyword.")
            return False
        
        # **Pair Created At filter (token age)**
        if self.min_pair_created_at is not None:
            current_time_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
            token_age = current_time_ms - pair_created_at  # Alter des Tokens in ms

            if token_age > self.min_pair_created_at:  # Ablehnen, wenn älter als 30min
                logger.warning(f"Rejecting coin: Pair created {time_ago(pair_created_at)}, max. required age {time_ago(current_time_ms - self.min_pair_created_at)}.")
                return False  # Coin ablehnen


        # MarketCap & Volume filters
        if self.min_marketcap is not None and marketcap < self.min_marketcap:
            logger.warning(f"Rejecting coin: marketCap {marketcap} < min_marketcap {self.min_marketcap}")
            return False
        if self.max_marketcap is not None and marketcap > self.max_marketcap:
            logger.warning(f"Rejecting coin: marketCap {marketcap} > max_marketcap {self.max_marketcap}")
            return False
        if self.min_volume is not None and volume < self.min_volume:
            logger.warning(f"Rejecting coin: volume {volume} < min_volume {self.min_volume}")
            return False
        if self.max_volume is not None and volume > self.max_volume:
            logger.warning(f"Rejecting coin: volume {volume} > max_volume {self.max_volume}")
            return False

        logger.warning(f"Coin '{name}' passed all filters.")
        return True
