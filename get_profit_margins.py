#!/usr/bin/env python
#script that sorts by price and profit
import datetime
import json
import io
import time

#from rest import GuildWars2ApiV2
import gw2.currencies
import gw2.tools
from gw2.currencies import Coins
import gw2.rest
from collections import Counter

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def incremental_backoff(item_ids):
	gw2_api = gw2.rest.GuildWars2ApiV2()
	tries = 1
	listings = None
	while tries <= 10 and listings is None:
		try:
			listings = gw2_api.commerce_listings(item_ids)
		except gw2.rest.ApiError:
			print('Failed {0} Times').format(tries)
			time.sleep(10**tries)
			tries += 1
	return listings


def main():
	gw2_api = gw2.rest.GuildWars2ApiV2()
	profit_dict = {}
	all_item_ids = gw2_api.items()
	coins = gw2.currencies.Coins()
	for item_ids in chunker(all_item_ids, 100):
		listings = incremental_backoff(item_ids)
		for listing in listings:
			item_id = listing['id']
			if not (listing['buys'] and listing['sells']):
				continue
			buy_price = listing['buys'][0]['unit_price']
			sell_price = listing['sells'][0]['unit_price']
			profit_margin = gw2.tools.trade_profit(buy_price, sell_price)
			profit_dict[item_id] = {'profit': coins.to_string(profit_margin), 'buy': coins.to_string(buy_price), 'sell': coins.to_string(sell_price)}

	profit_dump = {'time_stamp': datetime.datetime.now().isoformat(), 'profit': profit_dict}
	with open('profit_margins.json', 'w') as f:
		json.dump(profit_dump, f, sort_keys=True, indent=2, separators=(',', ': '))
	return 0

if __name__ == '__main__':
	main()
