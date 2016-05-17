1#!/usr/bin/env python
import argparse
import collections
import json
import os
"""
Mighty Worn Chain Greaves
  buy:    1g
  sell:   1g
  profit: 0g

 Next Item
"""
import gw2.currencies

def get_item_id(name, data_file=None):
	if data_file is None:
		data_file = os.path.join(os.path.dirname(__file__), 'organized_items.json')
	with open(data_file, 'r') as f:
		item_name = json.load(f)
	return item_name['name'][name]

def get_item_name(id, data_file=None):
	if data_file is None:
		data_file = os.path.join(os.path.dirname(__file__), 'organized_items.json')
	with open(data_file, 'r') as f:
		item_name = json.load(f)
	return item_name['id'][str(id)]

def organize_profits(file_name, number_of_profits, max_buy=None, min_buy=None, max_sell=None, min_sell=None):
	with open(file_name, 'r') as f:
		prices = json.load(f)
	prices = prices['profit']
	profit_prices = prices.items()
	if max_buy is not None:
		profit_prices = filter(lambda x: int(gw2.currencies.Coins.from_string(x[1]['buy'])) <= max_buy, profit_prices)
	if min_buy is not None:
		profit_prices = filter(lambda x: int(gw2.currencies.Coins.from_string(x[1]['buy'])) >= min_buy, profit_prices)

	if max_sell is not None:
		profit_prices = filter(lambda x: int(gw2.currencies.Coins.from_string(x[1]['sell'])) <= max_sell, profit_prices)
	if min_sell is not None:
		profit_prices = filter(lambda x: int(gw2.currencies.Coins.from_string(x[1]['sell'])) >= min_sell, profit_prices)

	profit_prices = sorted(profit_prices, key=lambda x: int(gw2.currencies.Coins.from_string(x[1]['profit'])))

	profit_prices.reverse()
	profit_prices = profit_prices[:number_of_profits]
	profit_prices = collections.OrderedDict(profit_prices)

	return profit_prices

def print_prices(top_items, profit_prices):
	for item in top_items:
		print(str(get_item_id(item)))
		print("{0: <10} {1}").format('  Buy:', profit_prices[item]['buy'])
		print("{0: <10} {1}").format('  Sell:', profit_prices[item]['sell'])
		print("{0: <10} {1}").format('  Profit:', profit_prices[item]['profit'])
		print('')


def main():
	parser = argparse.ArgumentParser(description='', conflict_handler='resolve')
	parser.add_argument('-f', '--file', dest='file_name', type=str, help='Name of file to use for profits')
	parser.add_argument('-n', '--number', default=5, dest='number_of_profits', type=int, help='number of profits shown')
	parser.add_argument('--max-buy', dest='max_buy', help='maximum buy price')
	parser.add_argument('--max-sell', dest='max_sell', help='maximum sell price')
	parser.add_argument('--min-buy', dest='min_buy', type=gw2.currencies.Coins.from_string, help='minimum buy price')
	parser.add_argument('--min-sell', dest='min_sell', type=gw2.currencies.Coins.from_string, help='minimum sell price')
	arguments = parser.parse_args()

	top_items = organize_profits(arguments.file_name, arguments.number_of_profits, arguments.max_buy, arguments.min_buy, arguments.max_sell, arguments.min_sell)
	print_prices(top_items[0], top_items[1])
		#print("{0} has a profit of {1}").format(str(get_item_id(item)), str(profit_prices[item]['profit']))
	return 0

if __name__ == '__main__':
	main()
