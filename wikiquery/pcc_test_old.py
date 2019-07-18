import json,datetime,csv,re,codecs,os,requests,sys
import urllib.request
from urllib.parse import quote

date_api_url = "https://pcc.g0v.ronny.tw/api/listbydate?date="
cata_list = ['5132','5133','5134','5139','522','8672','8673','97','98']

query_file=open('wikidata_query_new.json')
query_data = json.load(query_file)

date_format = "%Y%m%d"
date_a = date_b = datetime.datetime.today()
date_input = date_b.strftime(date_format)
if len(sys.argv)>1:
	try:
		date_b = datetime.datetime.strptime(sys.argv[1], date_format) + datetime.timedelta(days=1)
	except:
		if "today" not in sys.argv:
			date_input = input("參數錯誤！輸入起始日期 (6碼日期YYYYMMDD): ")
			date_b = datetime.datetime.strptime(date_input, date_format) + datetime.timedelta(days=1)
else:
	date_input = input("輸入起始日期 (6碼日期YYYYMMDD): ")
	date_b = datetime.datetime.strptime(date_input, date_format) + datetime.timedelta(days=1)
	
delta_days = (date_b - date_a).days
#print("delta:"+str(delta_days))
foname = "pcc_out_since_" + date_b.strftime(date_format) + ".csv"
#time_str = datetime.date.today().strftime(date_format)

def mmsend(message,hasData):
	SERVER_URL = "http://bambooculture.tw:8065"
	CHANNEL_ID = "qyhfekcb5byb8yuc11g3pgsdie"
	mmKey = "fucwsxjmrjfumjjazp4ikbp6ca"

	FILE_PATH = './'+foname
	s = requests.Session()
	s.headers.update({"Authorization": "Bearer "+mmKey})

	form_data = {
		"channel_id": ('', CHANNEL_ID),
		"client_ids": ('', "id_for_the_file"),
		"files": (os.path.basename(FILE_PATH), open(FILE_PATH, 'rb')),
	}
	r = s.post(SERVER_URL + '/api/v4/files', files=form_data)
	if hasData:
		FILE_ID = r.json()["file_infos"][0]["id"]		
		p = s.post(SERVER_URL + '/api/v4/posts', data=json.dumps({
		   "channel_id": CHANNEL_ID,
			"message": message,
			"file_ids": [ FILE_ID ]
		}))
	else:
		p = s.post(SERVER_URL + '/api/v4/posts', data=json.dumps({
		   "channel_id": CHANNEL_ID,
			"message": message
		}))
	
def searchbykey(p):	
	for keyword_dict in query_data['results']['bindings'] :
		keyword=keyword2=keyword_dict['itemLabel']['value']
		try:
			keyword2=keyword_dict['alt']['value']
		except:
			keyword2=keyword
		if keyword in str(p['brief']['title']) or keyword2 in str(p['brief']['title']):
			outdata = {}
			w = csv.writer(fo, dialect='excel')
			#.replace("unit_id=","unit_id="+p['unit_id']) 
			itemurl = p['tender_api_url']+ "&date=" + p['date']
			with urllib.request.urlopen(itemurl) as urlmore:
				datamore = json.loads(urlmore.read().decode())
				datamoreN = datamore['records'][len(datamore['records'])-1]
				outdata['date']=datamoreN['date']
				if keyword is keyword2:
					outdata['key']=keyword
				else:
					outdata['key']=keyword+"("+keyword2+")"
				outdata['unit_name']=datamore['unit_name']
				outdata['type']=datamoreN['brief']['type']
				outdata['title']=datamoreN['brief']['title']
				outdata['url']=itemurl.replace("pcc.g0v.ronny.tw/api/tender?","ronnywang.github.io/pcc-viewer/tender.html?")
				if 'category' in datamoreN['brief']:
					outdata['category']=datamoreN['brief']['category']
				elif '採購資料:標的分類' in datamoreN['detail']:
					outdata['category']=datamoreN['detail']['採購資料:標的分類']
				else:
					outdata['category']=datamoreN['detail'].get('已公告資料:標的分類',"N/A")
				if '採購資料:預算金額' in datamoreN['detail']:
					outdata['funding']=datamoreN['detail']['採購資料:預算金額']
				else:
					outdata['funding']=datamoreN['detail'].get('已公告資料:預算金額',"N/A")
				outdata['funding']=outdata['funding'].strip('元')
				if '其他:履約地點' in datamoreN['detail']:
					outdata['location']=datamoreN['detail']['其他:履約地點']
				elif '採購資料:履約地點（含地區）' in datamoreN['detail']:	
					outdata['location']=datamoreN['detail']['採購資料:履約地點（含地區）']		
				else:
					outdata['location']=datamoreN['detail'].get('已公告資料:履約地點（含地區）',"N/A")
			#fo.write(json.dumps(outdata)+",")
			#	datamore["keyword"]=keyword
			#	fo.write(json.dumps(datamore)+",")
			if outdata['category']=="N/A":
				w.writerow(outdata.values())
				return True	
				
			elif re.findall(r'\d+',outdata['category'])[0] in cata_list:
				w.writerow(outdata.values())
				return True	
	
	return False

with codecs.open(foname, "w+",'utf_8_sig') as fo:
	#fo.write("{")
	titlelist = ""
	while delta_days<=0:
		titlelist+= (date_a + datetime.timedelta(days=delta_days)).strftime(date_format)+"\r\n"
		dated_url = date_api_url + (date_a + datetime.timedelta(days=delta_days)).strftime(date_format)
		#fo.write('"'+(date_a + datetime.timedelta(days=delta_days)).strftime(date_format) + '":[')
		#fo.write((date_a + datetime.timedelta(days=delta_days)).strftime(date_format) + ',\r\n')
		delta_days+=1
		num_datas=0
		print(dated_url)
		with urllib.request.urlopen(dated_url) as url:
			data = json.loads(url.read().decode())
			if len(data)>0:
				for p in data['records']:
					if searchbykey(p):
						titlelist+=(p['brief']['title']+"\r\n")
						num_datas+=1
		#fo.write("{}],")
		print("num_datas: "+ str(num_datas))
		titlelist+="共:"+ str(num_datas)+"筆資料\r\n"
	#fo.write("{}}")
	fo.close()
	'''
	if(num_datas) > 0:
		mmsend(titlelist,True)
	else:
		mmsend(titlelist,False)
	'''
