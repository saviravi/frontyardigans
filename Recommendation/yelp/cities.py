from __future__ import annotations
from enum import Enum
from typing import Union
from .api import YelpResult
import os
from json import load
import matplotlib.pyplot as plt

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

    @classmethod
    def load_businesses(self, city: Union[City, str]) -> list[YelpResult]:
        if type(city) == City:
            city_name = city.value
        else:
            city_name = city
        
        path = os.path.join(
            os.path.dirname(__file__),
            "business_data",
            "%s_businesses.json" % city_name
        )

        with open(path, 'rb') as f:
            json_businesses = load(f)
            return list(map(YelpResult.from_dict, json_businesses))
    
    @classmethod
    def load_hotels(self, city: Union[City, str]) -> list[YelpResult]:
        if type(city) == City:
            city_name = city.value
        else:
            city_name = city
        
        path = os.path.join(
            os.path.dirname(__file__),
            "business_data",
            "%s_hotels.json" % city_name
        )

        with open(path, 'rb') as f:
            json_businesses = load(f)
            return list(map(YelpResult.from_dict, json_businesses))


def plot_businesses(businesses):
    longitude = [b.longitude for b in businesses if b.longitude is not None and b.latitude is not None]
    latitude = [b.latitude for b in businesses if b.longitude is not None and b.latitude is not None]
    plt.plot(longitude, latitude, 'r.')
    plt.show()