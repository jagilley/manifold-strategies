from manifoldpy.manifoldpy import api

with open('api_key.txt', 'r') as f:
    api_key = f.read().strip()

from datetime import datetime, timedelta

# get the current time
now = datetime.now()

# subtract one day
one_day_ago = now - timedelta(days=1)

# convert to Unix timestamp
timestamp = int(one_day_ago.timestamp())
print(timestamp)

markets = api.get_all_markets(after=timestamp)