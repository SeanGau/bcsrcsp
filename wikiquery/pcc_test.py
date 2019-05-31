import json, urllib.request
import datetime
from urllib.parse import quote
date_api_url = "https://pcc.g0v.ronny.tw/api/listbydate?date="

keywords_list = []
json_file=open('foo.json')
json_data = json.load(json_file)
#for p in json_data['results']['bindings']:
#	keywords_list.append(p['itemLabel']['value'])
#print(keywords_list)

date_input = input("輸入起始日期 (6碼日期YYYYMMDD): ")
date_format = "%Y%m%d"
date_a = datetime.datetime.today()
date_b = datetime.datetime.strptime(date_input, date_format)
delta_days = (date_b - date_a).days+1
#time_str = datetime.date.today().strftime("%Y%m%d")
with open("out.json", "w+") as fo:
	fo.write("[")
	while delta_days<=0:
		dated_url = date_api_url + (date_a + datetime.timedelta(days=delta_days)).strftime("%Y%m%d")
		delta_days+=1
		num_datas=0
		print(dated_url)
		with urllib.request.urlopen(dated_url) as url:
			data = json.loads(url.read().decode())
			if len(data)>0:
				for p in data['records']:
					for keyword_json in json_data['results']['bindings'] :
						keyword=keyword_json['itemLabel']['value']
						if keyword in str(p['brief']['title']) :
							#print(p['brief']['title'])
							p["keyword"]=keyword
							fo.write(json.dumps(p)+",")
							num_datas+=1
		print("num_datas: "+ str(num_datas))
	fo.write("{}]")
	fo.close()