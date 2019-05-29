import json, urllib.request
from datetime import date, timedelta
from urllib.parse import quote
date_api_url = "https://pcc.g0v.ronny.tw/api/listbydate?date="

keywords_list = []
with open('foo.json') as json_file:
	json_data = json.load(json_file)
	for p in json_data['results']['bindings']:
		keywords_list.append(p['itemLabel']['value'])


date_input = input("輸入6碼日期YYYYMMDD: ")
#time_str = date.today().strftime("%Y%m%d")
dated_url = date_api_url + date_input
with urllib.request.urlopen(dated_url) as url:
	data = json.loads(url.read().decode())
	for p in data['records']:
		if any(keyword in str(p['brief']['title']) for keyword in keywords_list):
			print(p['brief']['title'])
