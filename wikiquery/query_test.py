from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
import json

sparql_query = """
SELECT ?item ?itemLabel ?itemDescription ?into ?atLabel
WHERE {
  ?item wdt:P31/wdt:P279* wd:Q55659167;
        wdt:P17 wd:Q865.
  OPTIONAL { ?item wdt:P403 ?into. }
  OPTIONAL { ?item wdt:P131 ?at. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh-tw, zh-hant, zh, en". }
}
"""
# 取得位在中華民國的天然水體
# 和他們的上下游(若有)
res = return_sparql_query_results(sparql_query)
#for p in res['results']['bindings']:
#		print('name: ' + p['itemLabel']['value'])
jsonfile = json.dumps(res)
fo = open("/usr/bcsrcsp/wikiquery/foo.json", "w")
fo.write(jsonfile)
fo.close()