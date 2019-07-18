from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
import json

sparql_query = """
SELECT ?item ?itemLabel ?alt ?into ?atLabel ?coord
WHERE {
  ?item wdt:P31/wdt:P279* wd:Q55659167;
        wdt:P17 wd:Q865.
  OPTIONAL { ?item skos:altLabel ?alt. }
  OPTIONAL { ?item wdt:P403 ?into. }
  OPTIONAL { ?item wdt:P131 ?at. }
  OPTIONAL { ?item wdt:P625 ?coord. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh-tw, zh-hant, zh". }
}
"""
# 取得位在中華民國的天然水體
# 和他們的上下游(若有)
res = return_sparql_query_results(sparql_query)
#for p in res['results']['bindings']:
#		print('name: ' + p['itemLabel']['value'])
jsonfile = json.dumps(res)
fo = open("wikidata_query_new.json", "w+")
fo.write(jsonfile)
fo.close()
