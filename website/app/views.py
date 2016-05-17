import argparse
import json

import flask

from app import app
import profit_margin
import gw2
#min and max query
def organize_profits(*args, **kwargs):
	profit_prices = profit_margin.organize_profits(*args, **kwargs)
	for item in profit_prices.keys():
		profit_prices[item]['name'] = profit_margin.get_item_name(item)
	return profit_prices

def query_to_int(arg, default):
	arg = flask.request.values.get(arg)
	if arg is None:
		return default
	if not arg.isdigit():
		return default
	return int(arg)

def query_to_coin(arg, default):
	arg = flask.request.values.get(arg)
	if arg is None:
		return default
	arg = gw2.currencies.Coins.from_string(arg)
	return arg


@app.route('/')
@app.route('/index')
def index():
	count = query_to_int('count', 10)
	min_sell = query_to_coin('min-sell', None)
	max_sell = query_to_coin('max-sell', None)
	min_buy = query_to_coin('min-buy', None)
	max_buy = query_to_coin('max-buy', None)
	profit_prices = organize_profits('profit_margins.json', count, max_buy, min_buy, max_sell, min_sell)
	return flask.render_template(
		'index.html',
		title='Home',
		profit_prices=profit_prices
	)
