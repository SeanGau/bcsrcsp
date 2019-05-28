import json, urllib.request
from urllib.parse import quote
query_url="https://pcc.g0v.ronny.tw/api/searchbytitle?query="
with open('foo_test.json') as json_file:
	json_data = json.load(json_file)
	for p in json_data['results']['bindings']:
		name = p['itemLabel']['value']
		named_url=query_url+quote(name)
		#print(named_url)		
		with urllib.request.urlopen(named_url) as url:
			data = json.loads(url.read().decode())
			print(data['query']+str(data['total_records']))