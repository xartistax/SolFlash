
from services.logger import setup_logger



logger = setup_logger("COINFILTER")


class CoinFilter:
    def __init__(self, enabled=True, min_marketcap=None, max_marketcap=None, min_volume=None, max_volume=None):
        self.enabled = enabled
        self.min_marketcap = min_marketcap
        self.max_marketcap = max_marketcap
        self.min_volume = min_volume
        self.max_volume = max_volume

    def is_valid(self, coin):
        """Check if a single coin meets the filter criteria."""
        if not self.enabled:
            logger.warning("Filtering disabled, accepting all coins.")
            return True  

        marketcap = coin.get("marketCap", 0)
        volume = coin.get("volume", {}).get("m5", 0)  # Using 5min volume

        logger.debug(f"Checking coin: marketCap={marketcap}, volume={volume}")

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

        logger.warning("Coin passed all filters.")
        return True
