import json, urllib.request, time
from urllib.parse import quote
query_url="https://pcc.g0v.ronny.tw/api/searchbytitle?query="
with open('foo_test.json') as json_file:
	json_data = json.load(json_file)
	for p in json_data['results']['bindings']:
		name = p['itemLabel']['value']
		named_url=query_url+quote(name)
		#print(named_url)
		time1 = time.time()
		with urllib.request.urlopen(named_url) as url:
			data = json.loads(url.read().decode())
			if data['total_records']>0:
				current_page = 1
				jsonfile = json.dumps(data)
				fo = open(data['query']+str(current_page)+".json", "w+")
				fo.write(jsonfile)
				fo.close()
				print(str(time.time()-time1)+"msecs "+data['query']+" page:"+str(current_page) )				
				while int(data['total_pages']) > current_page:
					time1 = time.time()
					current_page += 1
					named_url=query_url+quote(name)+"page="+str(current_page)
					with urllib.request.urlopen(named_url) as url2:
						data2 = json.loads(url2.read().decode())
						jsonfile2 = json.dumps(data2)
						fo = open(data['query']+str(current_page)+".json", "w+")
						fo.write(jsonfile2)
						fo.close()
						print(str(time.time()-time1)+"msecs "+data['query']+" page:"+str(current_page) )				