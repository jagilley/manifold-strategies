from .strategy import Strategy
from datetime import datetime, timedelta
from manifoldpy.manifoldpy.api import Market
from manifoldpy.manifoldpy import api
from .time_utils import get_price_at_timestamp, get_price
import json

class CategorySpecificPermabear(Strategy):
    def __init__(self, hi: float, lo: float, group_slugs: list):
        super().__init__("CategorySpecificPermabear")
        self.hi = hi
        self.lo = lo
        self.group_slugs = group_slugs
        self.group_ids = []
        for slug in group_slugs:
            self.group_ids.append(api.get_group_by_slug(slug).id)

        # get all markets in the groups
        self.group_markets = []
        for group_id in self.group_ids:
            self.group_markets += api.get_group_markets(group_id)


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

        if market.id not in [m.id for m in self.group_markets]:
            return None, None
    
        delta = self.evaluate_strategy(price_at_one_day_after, current_price, position)
        return delta, position
    
    def get_position(self, market: Market):
        position = 'NO'
        amount = 15
        if market.id not in [m.id for m in self.group_markets]:
            return None, None
        
        if not (market.probability < self.hi and market.probability > self.lo):
            return None, None
        
        return position, amount

    def __str__(self):
        return f"CategorySpecificPermabear({self.hi}, {self.lo}, {self.group_slugs})"
