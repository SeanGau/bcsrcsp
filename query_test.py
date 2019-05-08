from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
import json

# send any sparql query to the wikidata query service and get full result back
# here we use an example that counts the number of humans
sparql_query = """
SELECT ?item ?itemLabel ?in
WHERE {
  ?item wdt:P31/wdt:P279* wd:Q55659167;
        wdt:P17 wd:Q865.
  OPTIONAL { ?item wdt:P403 ?in. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh-tw, zh-hant, zh, en". }
}
"""
res = return_sparql_query_results(sparql_query)
jsonfile = json.dumps(res)
fo = open("foo.json", "w")
fo.write(jsonfile)
fo.close()