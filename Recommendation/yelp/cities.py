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

    def __init__(self, value: str):
        super(Enum, self).__init__()
        self.businesses = self.load_businesses()
        self.hotels = self.load_hotels()
        self.airport_code = "LAX"

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
        longitude = [b.longitude for b in self.businesses if b.longitude is not None and b.latitude is not None and (category is None or category in b.categories)]
        latitude = [b.latitude for b in self.businesses if b.longitude is not None and b.latitude is not None and (category is None or category in b.categories)]
        plt.plot(longitude, latitude, 'r.')
        plt.show()