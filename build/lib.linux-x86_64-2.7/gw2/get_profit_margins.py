#!/usr/bin/env python
from rest import GuildWars2ApiV2
import json
import io
import trading_post_stats

from collections import Counter
from currencies import Coins
import argparse

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def main():
	gw2_api = GuildWars2ApiV2()
	item_ids = gw2_api.items()
	profit_dict = {}
	chunked_item_ids = []
	import pdb; pdb.set_trace()
	for group in chunker(item_ids, 100):
		listings = gw2_api.commerce_listings(group)
		import pdb; pdb.set_trace()
		for id in group:
			item_profits[id] = trading_post_stats.get_profit_margin(listings[id]['buys'][0]['unit_price'], listings[id]['sells'][0]['unit_price'])
		for profit in items_profits:
			if not 'name' in item_details:
				continue
			#profit_dict[item_profits] = item_details['id']


	import pdb; pdb.set_trace()
	with open('organized_items.json', 'w') as f:
		json.dump(name_dict, f, sort_keys=True, indent=2, separators=(',', ': '))
	return 0

if __name__ == '__main__':
	main()
