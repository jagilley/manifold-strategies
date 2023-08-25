from datetime import datetime
from manifoldpy.manifoldpy.api import Market

class Strategy:
    def __init__(self, name: str):
        self.name = name

    def run(self, binary_dataset, since: datetime = None, verbose: bool = False):
        deltas = []
        for bin_market in binary_dataset:
            if since is not None and bin_market.createdTime < since.timestamp() * 1000:
                continue
            delta, position = self.strategy(bin_market)
            if position is not None:
                deltas.append(delta)
            
            if len(deltas) > 0 and len(deltas) % 10 == 0 and verbose:
                print(f"Running average: {sum(deltas) / len(deltas)}")
        return deltas

    def strategy(self, market: Market):
        raise NotImplementedError

    def evaluate_strategy(self, price_init: float, price_final: float, position: str):
        if position == 'YES':
            return price_final - price_init
        elif position == 'NO':
            return price_init - price_final
        else:
            raise ValueError(f"Invalid position: {position}")

    def __str__(self):
        return self.name
