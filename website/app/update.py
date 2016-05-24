
@app.route('/')
@app.route('/update')
def index():
	with open("profit_margins.json") as json_file:
	 json_data = json.load(json_file)
	 last_updated = json_data['time_stamp']
	return flask.render_template(
		'index.html',
		title='Home',
		profit_prices=profit_prices,
		last_updated=last_updated
	)