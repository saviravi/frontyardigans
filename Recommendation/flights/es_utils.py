from elasticsearch import Elasticsearch
import os
import re
# import utils
import json

AIRPORT_INDEX = "airport-info"


class ElasticSearcher:
    
    def __init__(self):
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
        # utils.log(msg=f"host - {host}, port - {port}, auth - {auth}")
        # Connect to cluster over SSL using auth for best security:
        es_header = [{
            'host': host,
            'port': port,
            'use_ssl': True,
            'http_auth': (auth[0],auth[1])
            }]
            # Instantiate the new Elasticsearch connection:
        print("connected!!")
        self.es = Elasticsearch(es_header)
    
    def create_index(self, index_name: str, properties: dict):
        """ creates an index, 
            properties is a dict of attributes of an ES doc and their types, i.e. "attribute": {"type": <type>} """
        self.es.indices.create(
            index=index_name,
            body={
                "settings": {"number_of_shards": 1},
                "mappings": {
                    "properties": properties
                }
            }
        )
        return


    def multifield_search(self, index, search_phrase, fields):
        """ Multi-Match search that can specify which fields to search to find your phrase"""
        resp = self.es.search(index=index, body={"query": 
            {"multi_match": {
                "fields":  fields,
                "query": search_phrase,
                }
            }
        })
        # utils.log(msg=f"Got {resp['hits']['total']['value']} Search Hits\n")
        return resp["hits"]["hits"]
    

    def airport_search(self, search_phrase: str, fields=["city"]):
        """ Search specialized for airports, can specify fields but defaults to city"""
        
        return self.multifield_search(index=AIRPORT_INDEX, search_phrase=search_phrase, fields=fields)[0]["_source"]
    
    def distance_search(self, index_name:str, latitude: float, longitude: float, distance: float):
        """ Search specialized for finding locations within a certain distance (in miles) of a point """
        resp =  self.es.search(index=index_name, body={"query": {
                    "geo_distance": {
                        "distance": f"{distance}mi",
                        "location": {
                            "lat": latitude,
                            "lon": longitude,
                        }
                    }
                
            }
        })
        # utils.log(msg=f"Got {resp['hits']['total']['value']} Search Hits\n")
        return resp["hits"]["hits"]
        

def __create_bonsai_connection():
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
    # utils.log(msg=f"host - {host}, port - {port}, auth - {auth}")
    # Connect to cluster over SSL using auth for best security:
    es_header = [{
        'host': host,
        'port': port,
        'use_ssl': True,
        'http_auth': (auth[0],auth[1])
        }]
        # Instantiate the new Elasticsearch connection:
    print("connected!!")
    return Elasticsearch(es_header)




