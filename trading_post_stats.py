#!/usr/bin/env python
import gw2
from gw2.rest import GuildWars2ApiV2
from collections import Counter
from gw2.currencies import Coins
import json
import argparse
import datetime

#named tuple with mean median mode and range

def listed_prices(id, transaction, number):
	guild_wars_api = GuildWars2ApiV2()
	prices_list = []
	#import pdb; pdb.set_trace
	while number > 0:
		try:
			listings = guild_wars_api.commerce_listings(id)
		except gw2.rest.ApiError:
			return []
		listings = listings[0]
		listings = listings[transaction]
		listings = listings[number]
		number_of_listings = listings['listings']
		listings = listings['unit_price']
		#if number < number_of_listings:
			#return listings
		while number > 0 and number_of_listings > 0:
			prices_list.append(listings)
			number -= 1
			number_of_listings -= 1
	return prices_list

def get_prices_mean(prices):
	average = sum(prices)
	average = average / len(prices)
	return average

def get_prices_mode(prices):
	prices = data = Counter(prices)
	return prices.most_common(1)[0][0]

def get_prices_median(prices):
	prices = sorted(prices)
	median = prices[len(prices)/2]
	return median

def get_prices_range(prices):
	sorted_prices = sorted(prices)
	prices_range = [sorted_prices[0], sorted_prices[-1]]
	return prices_range

def get_item_id(name):
	guild_wars_api = GuildWars2ApiV2()
	with open('organized_items.json', 'r') as f:
		item_name = json.load(f)
	if not name in item_name:
		return None
	return item_name[name]

def get_profit_margin(id):
	buy_listings = buy
	sell_listings = listed_prices(id, 'sells', 1)
	sell_listings = listed_prices(id, 'buys', 1)
	profit = gw2.tools.trade_profit(buy_listings, sell_listings[0])
	date_time = datetime.datetime.now().isoformat()
	import pdb; pdb.set_trace()
	profits[id] = profit
	return profit

def main():
	parser = argparse.ArgumentParser(description='', conflict_handler='resolve')
	parser.add_argument('item_name', help='Select which item name to get ID for ')
	parser.add_argument('-a', '--amount', dest='listing_amount', type=int, default=5, help='Amount of listings it should return')
	args = parser.parse_args()
	#account = gw2.Account("6DA64826-8A64-7E4E-8BAF-597BC2C1A6394302A9B5-9250-4889-9FAF-E108230C862B")

	item_id = get_item_id(args.item_name)
	if item_id is None:
		print('Invalid Item Name')
		return None
	print("The item ID of {0} is {1}").format(args.item_name, item_id)
	prices = listed_prices(item_id, 'buys', args.listing_amount)
	if not prices:
		print('No listings for {0}'.format(args.item_name))
		return
	print("Mean of the  prices for the item is {0}").format(Coins(get_prices_mean(prices)))
	print("The mode, Price and Amount {0}").format(Coins(get_prices_mode(prices)))
	print("The median is {0}").format(Coins(get_prices_median(prices)))
	print("The lowest is {0} and the highest is {1}").format(Coins(get_prices_range(prices)[0]), Coins(get_prices_range(prices)[1]))
	#print("The profit margin is {0}.".format(get_profit_margin(item_id, prices[0])))

	#print("The id for Mithril Ingot is {1}").format(get_item_id(
	#get_listing_mode(19684, 'buys', 5)
if __name__ == '__main__':
	main()

