from datetime import datetime
from manifoldpy.manifoldpy.api import Market

def get_price(bets, timestamp):
    """Use binary search cause I'm fancy"""
    left, right = 0, len(bets) - 1
    while left < right:
        mid = (left + right) // 2
        if bets[mid].createdTime < timestamp:
            left = mid + 1
        else:
            right = mid
    # At this point, left == right.
    # If the timestamp of the bet at this index is greater than the given timestamp,
    # and this is not the first bet, return the price of the previous bet.
    if bets[left].createdTime > timestamp and left > 0:
        return bets[left - 1].probAfter
    # Otherwise, return the price of the bet at this index.
    return bets[left].probAfter

def get_price_at_timestamp(market: Market, timestamp: datetime) -> float:
    """Get the price of a market at a given timestamp"""

    # Find the first bet that was created before the timestamp
    bets = sorted(
        market.bets, key=lambda b: b.createdTime
    )
    return get_price(bets, timestamp)
