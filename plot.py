import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import json

# Load JSON file
with open('bets/003.2023-07-28.2023-07-25.json') as f:
    data = json.load(f)

# load markets data
with open('manifold-dump-markets-04082023.json') as f:
    markets = json.load(f)

# turn markets into df using json_normalize
markets_df = pd.json_normalize(markets)

# print sample of markets_df
print(markets_df.head())

# print stats on markets_df
print("len of markets df is", len(markets_df))

# Convert to pandas DataFrame
df = pd.DataFrame(data)

# Filter by contractId
contractId = "ucpkgCHN4RSvTS8pxoi4"  # replace with your contractId
df_filtered = df[df['contractId'] == contractId]

# get the 'question' column from markets_df where the 'contractId' column matches the contractId
question = markets_df[markets_df['id'] == contractId]['question'].values[0]

# Sort by timestamp
df_filtered = df_filtered.sort_values(by='createdTime')

# Convert timestamp to datetime
df_filtered['createdTime'] = pd.to_datetime(df_filtered['createdTime'], unit='ms')

# Plot probability history
plt.plot(df_filtered['createdTime'], df_filtered['probAfter'])
plt.xlabel('Time')
plt.ylabel('Probability')
plt.title(question)
plt.show()

# example rule: buy when probAfter is 0.5

def test_rule(df):
    # if probAfter is lower than 0.1, buy 'NO'
    if df['probAfter'] < 0.1:
        return 'NO'
    # if probAfter is higher than 0.9, buy 'YES'
    elif df['probAfter'] > 0.7:
        return 'YES'
    
    return 'NA'

# evaluate what would happen if you bought 100 shares of 'YES' when the market opened
# and sold 100 shares of 'YES' when the market closed
# first we need to know the price of 'YES' at the market open and close
initial_price = df_filtered.iloc[0]['probAfter']
final_price = df_filtered.iloc[-1]['probAfter']

# calculate the profit
profit = 100 * (final_price - initial_price)
print("profit is", profit)

# test the rule on df_filtered
df_filtered['test_rule'] = df_filtered.apply(test_rule, axis=1)

# print the first 10 rows of df_filtered
print(df_filtered['test_rule'])