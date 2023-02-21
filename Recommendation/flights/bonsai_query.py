
# DocViewer
# Pages
# from elasticsearch import Elasticsearch, helpers
import es_utils
# bonsai = os.environ['BONSAI_URL']
# auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
# host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')
# # optional port
# match = re.search('(:\d+)', host)
# if match:
#   p = match.group(0)
#   host = host.replace(p, '')
#   port = int(p.split(':')[1])
# else:
#   port=443
# print(host)
# print(port)
# print(auth)
# # Connect to cluster over SSL using auth for best security:
# es_header = [{
#  'host': host,
#  'port': port,
#  'use_ssl': True,
#  'http_auth': (auth[0],auth[1])
# }]
# # Instantiate the new Elasticsearch connection:
# es = Elasticsearch(es_header)

es = es_utils.ElasticSearcher()
# hits = es.airport_search("Ohio", ["subdivision"])
hits = es.distance_search("airport-info", 39.9969466666667, -82.8921591666667, 100 )
# print(hits["hits"]["hits"])
print(hits)



# es = es_utils.create_bonsai_connection()

# resp = es.get(index="airport-info", id=1)
# print(resp['_source'])

# resp = es.search(index="airport-info", body={"query": {    "multi_match": {
#       "fields":  [ "city" ],
#       "query":     "New York",
#     }}})
# print("Got %d Hits:" % resp['hits']['total']['value'])
# for hit in resp['hits']['hits']:
#     print(hit["_source"])

# res = es.search(index="airport-info", body={"query": {"match": {"doc": "KNX"}}})
# print(len(res["hits"]["hits"]))
# for doc in res["hits"]["hits"]:
#   print(doc)
# res = es.search (index="newsgroup", body={"query": {"match": {"doc": "Phille"}}})
# print(len(res["hits"]["hits"]))
# res = es.search (index="newsgroup", body={"query": {"match": {"doc":{"query": 
# "Phille", "fuzziness": "AUTO"}}}}, size =10000)
# print(len(res["hits"]["hits"]))
# res = es.search(index = "newsgroup", body={"query": {"more_like_this": {"fields":
# ["doc"], "like": """The first ice resurfacer was invented by Frank Zamboni, who was 
# originally in the refrigeration business. Zamboni created a plant for making ice 
# blocks that could be used in refrigeration applications. As the demand for ice 
# blocks waned with the spread of compressor-based refrigeration, he looked for 
# another way to capitalize on his expertise with ice production"""
# print(len(res["hits"]["hits"]))
# for doc in res["hits"]["hits"]:
#   print(doc)

