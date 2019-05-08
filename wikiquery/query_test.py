from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
import json

sparql_query = """
SELECT ?item ?itemLabel ?itemDescription ?in ?out
WHERE {
  ?item wdt:P31/wdt:P279* wd:Q55659167;
        wdt:P17 wd:Q865.
  OPTIONAL { ?item wdt:P403 ?in. }
  OPTIONAL { ?item wdt:P974 ?out. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh-tw, zh-hant, zh, en". }
}
"""
#取得位在中華民國的天然水體
#和他們的上下游(若有)
res = return_sparql_query_results(sparql_query)
jsonfile = json.dumps(res)
fo = open("foo.json", "w")
fo.write(jsonfile)
fo.close()