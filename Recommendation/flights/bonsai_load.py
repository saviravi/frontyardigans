from elasticsearch import Elasticsearch, helpers
import os
import json
import re
import es_utils

def create_index(es):
    es.indices.create(
        index="airport-info",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "iata": {"type": "keyword"},
                    "city": {"type": "completion"},
                    "subdivision": {"type": "text"},
                    "country": {"type": "keyword"},
                    "icao": {"type": "keyword"},
                    "elevation": {"type": "float"},
                    "location": {"type": "geo_point"},
                    "timezone": {"type": "text"}
                }
            },
        },
    )
    return

# "AYM": 
#     {
#         "icao": "_AYM", 
#         "iata": "AYM", 
#         "name": "Yas Island Seaplane Base", 
#         "city": "Yas Island", 
#         "subd": "Abu Dhabi", 
#         "country": "AE", 
#         "elevation": 0.0, 
#         "lat": 24.467, 
#         "lon": 54.6103, 
#         "tz": "Asia/Dubai", 
#         "lid": ""}}



def generate_actions():
    elasticdocs = open("elasticdocs.json", "w")
    with open("airportinfo.json", mode="r") as file:
        info = json.loads(file.read())
        # print(info["CMH"])
        for airport in info.values():
            doc = {
                "_op_type": "index",
                "_index": "airport-info",
                "title": airport["iata"],
                "_id": airport["iata"],
                "name": airport["name"],
                "iata": airport["iata"],
                "city": airport["city"],
                "subdivision": airport["subd"],
                "country": airport["country"],
                "icao": airport["icao"],
                "elevation": airport["elevation"],
                "location": {"lat": float(airport["lat"]), "lon": float(airport["lon"])},
                "timezone": airport["tz"],

            }
            json.dump(doc, elasticdocs)
            elasticdocs.write(",\n")
    elasticdocs.close()

    # with open(DATASET_PATH, mode="r") as f:
    #     reader = csv.DictReader(f)

    #     for row in reader:
    #         doc = {
    #             "_id": row["CAMIS"],
    #             "name": row["DBA"],
    #             "borough": row["BORO"],
    #             "cuisine": row["CUISINE DESCRIPTION"],
    #             "grade": row["GRADE"] or None,
    #         }

    #         lat = row["Latitude"]
    #         lon = row["Longitude"]
    #         if lat not in ("", "0") and lon not in ("", "0"):
    #             doc["location"] = {"lat": float(lat), "lon": float(lon)}
    #         yield doc


bonsai = os.environ['BONSAI_URL']
auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')
# optional port
match = re.search('(:\d+)', host)
if match:
  p = match.group(0)
  host = host.replace(p, '')
  port = int(p.split(':')[1])
else:
  port=443
# Connect to cluster over SSL using auth for best security:
es_header = [{
 'host': host,
 'port': port,
 'use_ssl': True,
 'http_auth': (auth[0],auth[1])
}]
# Instantiate the new Elasticsearch connection:
es = Elasticsearch(es_header)
# create_index(es)

# generate_actions()
with open("elasticdocs.json", mode="r") as file:
    docs = json.loads(file.read())
    helpers.bulk(es, docs)




