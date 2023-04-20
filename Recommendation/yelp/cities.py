from __future__ import annotations
from enum import Enum
from .api import YelpResult
import os
from json import load
import matplotlib.pyplot as plt
import re
from elasticsearch import Elasticsearch
# from flights.es_utils import ElasticSearcher

# es = __create_bonsai_connection()

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
    return Elasticsearch(es_header)

def airport_search(city_name):

    resp = es.search(index="airport-info", body={"query": 
        {"multi_match": {
            "fields":  ["city"],
            "query": city_name,
            }
        }
    })
    return resp["hits"]["hits"]
    # return resp["hits"]["hits"][0]["_source"]["iata"]

es = __create_bonsai_connection()


class City(Enum):
    Amsterdam = "amsterdam"
    Barcelona = "barcelona"
    Cairns = "cairns"
    Cancun = "cancun"
    HongKong = "hong_kong"
    Honolulu = "honolulu"
    Istanbul = "istanbul"
    LasVegas = "las_vegas"
    London = "london"
    LosAngeles = "los_angeles"
    Madrid = "madrid"
    Maui = "maui"
    MexicoCity = "mexico_city"
    Miami = "miami"
    NewYorkCity = "new_york_city"
    Orlando = "orlando"
    Paris = "paris"
    Prague = "prague"
    #Queenstown = "queenstown"
    Rio = "rio"
    Rome = "rome"
    SanFrancisco = "san_francisco"
    Seville = "seville"
    Sydney = "sydney"
    Tokyo = "tokyo"
    #Tulum = "tulum"
    Vienna = "vienna"

    def __init__(self, value: str):
        super(Enum, self).__init__()
        self.businesses = self.load_businesses()
        self.hotels = self.load_hotels()
        search_val = value.replace("_", " ")
        valu = airport_search(search_val)
        if value == "maui":
            self.airport_code = "OGG"
        elif value == "new_york_city":
            self.airport_code = "JFK"
        elif value == "rio":
            self.airport_code = "GIG"
        elif value == "seville":
            self.airport_code = "SVQ"
        else:
            self.airport_code = valu[0]["_source"]["iata"]

    def load_businesses(self) -> list[YelpResult]:
        path = os.path.join(
            os.path.dirname(__file__),
            "business_data",
            "%s_businesses.json" % self.value
        )

        with open(path, 'rb') as f:
            json_businesses = load(f)
            return list(map(YelpResult.from_dict, json_businesses))
    
    def load_hotels(self) -> list[YelpResult]:
        path = os.path.join(
            os.path.dirname(__file__),
            "business_data",
            "%s_hotels.json" % self.value
        )

        with open(path, 'rb') as f:
            json_businesses = load(f)
            return list(map(YelpResult.from_dict, json_businesses))

    def get_city_center(self) -> tuple[float, float]:
        """
        Takes in a list of businesses and returns the (latitude, longitude).
        """
        average_lat = 0
        average_long = 0
        count = 0

        for b in self.businesses:
            if b.latitude is not None and b.longitude is not None:
                average_lat += b.latitude
                average_long += b.longitude
                count += 1
        for b in self.hotels:
            if b.latitude is not None and b.longitude is not None:
                average_lat += b.latitude
                average_long += b.longitude
                count += 1

        return (average_lat / count, average_long / count)

    def plot_businesses(self, category=None):
        longitude = [b.longitude for b in self.businesses
                    if b.longitude is not None
                     and b.latitude is not None
                     and (category is None or category in b.categories)]
        latitude = [b.latitude for b in self.businesses
                    if b.longitude is not None
                    and b.latitude is not None
                    and (category is None or category in b.categories)]
        plt.plot(longitude, latitude, 'r.')
        plt.show()



# print("hi")
# city = City("amsterdam")
# print(city.__dict__)

