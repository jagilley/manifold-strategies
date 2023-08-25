from .strategy import Strategy
from datetime import datetime, timedelta
from manifoldpy.manifoldpy.api import Market
from .time_utils import get_price_at_timestamp, get_price
import json

class Permabear(Strategy):
    """Be a permabear, and always bet NO when the price is below hi and above lo"""
    def __init__(self, hi: float, lo: float):
        super().__init__("Permabear")
        self.hi = hi
        self.lo = lo

    def strategy(self, market: Market):
        position = 'NO'

        created_datetime = datetime.fromtimestamp(market.createdTime / 1000)
        one_day_after = created_datetime + timedelta(hours=6)
        one_day_after_timestamp = one_day_after.timestamp()
        one_day_after_timestamp_ms = one_day_after_timestamp * 1000

        price_at_one_day_after = get_price_at_timestamp(market, one_day_after_timestamp_ms)
        current_price = get_price_at_timestamp(market, datetime.now().timestamp() * 1000)

        if not (price_at_one_day_after < self.hi and price_at_one_day_after > self.lo):
            return None, None
    
        delta = self.evaluate_strategy(price_at_one_day_after, current_price, position)
        return delta, position

    def __str__(self):
        return f"Permabear({self.hi}, {self.lo})"
