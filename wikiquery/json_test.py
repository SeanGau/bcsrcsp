import json

with open('foo.json') as json_file:
	json_data = json.load(json_file)
	for p in json_data['results']['bindings']:
		print('name: ' + p['itemLabel']['value'])