from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import os

from tqdm import tqdm
from yelp import YelpCategory
from pickle import load
import json

load_dotenv()

if __name__ == "__main__":
    es = Elasticsearch(os.environ['BONSAI_URL'])
    print("connected to ES {0}".format(es.info()['name']))

    with open('yelp_data.pickle', 'rb') as f:
        yelp_data = load(f)

    cities = list(yelp_data)
    categories = list(yelp_data[cities[0]])

    documents = []
    for city in cities:
        for category in categories:
            for doc in yelp_data[city][category]:
                if doc["latitude"] is None or doc["longitude"] is None:
                    continue
                doc_categories = []
                for c in doc["categories"]:
                    if type(c) == YelpCategory:
                        doc_categories.append(c.value)
                    else:
                        doc_categories.append(c['alias'])
                
                documents.append({
                    "_index": "businesses",
                    "city_name": city,
                    "id": doc["id"],
                    "name": doc["name"],
                    "categories": doc_categories,
                    "review_count": doc["review_count"],
                    "rating": doc["rating"],
                    "location": {"lat": doc["latitude"], "lon": doc["longitude"]},
                    "price": doc["price"]
                })

    yelp_business_mapping = {
        "mappings": {
            "properties": {
                "city_name": {"type": "text"},
                "id": {"type": "text"},
                "name": {"type": "text"},
                "categories": {"type": "text"},
                "review_count": {"type": "integer"},
                "rating": {"type": "integer"},
                "location": {"type": "geo_point"},
                "price": {"type": "integer"}
            }
        }
    }

    if es.indices.exists("businesses"):
        print("businesses index already exists, deleting")
        es.indices.delete("businesses")

    print("creating businesses index")
    es.indices.create(index="businesses", body=yelp_business_mapping)

    # Insert all documents
    print("inserting documents")
    helpers.bulk(es, documents)
    es.indices.refresh("businesses")
    num_inserted = es.cat.count(index="businesses").split(" ")[2].strip()
    print("inserted %s documents" % num_inserted)

    # resp = es.search(index="businesses", body={
    #     "query": {
    #         "match": {
    #             "city_name": "Paris"
    #         }
    #     },
    #     "size": "1000",
    # })

    # for hit in resp['hits']['hits']:
    #     print(hit)