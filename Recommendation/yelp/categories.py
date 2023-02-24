from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Union

@dataclass
class UnknownYelpCategory:
    """
    Placeholder for Yelp categories that haven't been enumerated yet.
    """
    alias: str
    title: str

class YelpCategory(Enum):
    """
    Enumeration of Yelp business categories.
    See https://docs.developer.yelp.com/docs/resources-categories
    """
    # Active life
    Aquariums = "aquariums"
    Beaches = "beaches"
    BikeRentals = "bikerentals"
    BikePaths = "bicyclepaths"
    ScubaDiving = "scubadiving"
    Hiking = "hiking"
    PublicPlazas = "publicplazas"
    Skydiving = "skydiving"
    Zoos = "zoos"

    # Arts & Entertainment
    ArtGalleries = "galleries"
    Casinos = "casinos"
    Castles = "castles"
    MovieTheaters = "movietheaters"
    CulturalCenter = "culturalcenter"
    ChristmasMarkets = "xmasmarkets"
    Festivals = "generalfestivals,funfair"
    Museums = "museums"
    ArtMuseums = "artmuseums"
    Observatories = "observatories"
    Opera = "opera"
    Theater = "theater"
    Planetarium = "planetarium"
    Rodeo = "rodeo"
    Wineries = "wineries"

    # Food
    Food = "food"
    Breakfast = "breakfast_brunch"
    Bagels = "bagels"
    Bakeries = "bakeries"
    Breweries = "breweries"
    Cafes = "cafes"
    Coffee = "coffee"
    Desserts = "desserts"
    FoodTrucks = "foodtrucks"

    # Shopping
    MediaStores = "media"
    DepartmentStores = "deptstores"
    FashionStores = "fashion"
    GiftStores = "giftshops"
    

    # Nightlife
    Bars = "bars"
    ComedyClub = "comedyclubs"

    # Travel
    Hotels = "hotels"
    Parking = "parking"
    CurrencyExchange = "currencyexchange"
    EmergencyRooms = "emergencyrooms"
    Airports = "airports"
    CarRental = "carrental"
    Tours = "tours"

    # All
    All = "all"

    @staticmethod
    def values() -> list[str]:
        return [x.value for x in YelpCategory]

    @staticmethod
    def from_json(category: dict) -> Union[YelpCategory, UnknownYelpCategory]:
        """
        Attempts to convert a `{'alias': ..., 'name': ...}` category result from the Yelp Fusion API to a `YelpCategory` instance.
        If no matching `YelpCategory` is found, returns an instance of `UnknownYelpCategory`.
        """
        alias: str = category["alias"]
        title: str = category["title"]

        values = YelpCategory.values()

        if alias in values:
            return YelpCategory(alias)
        elif title.lower() in values:
            return YelpCategory(title.lower())

        for value in values:
            if alias in value or title in value:
                return YelpCategory(value)
    
        return UnknownYelpCategory(alias, title)

def any_of(categories: list[Union[UnknownYelpCategory, YelpCategory]]) -> str:
    """
    Returns query string that combines multiple categories.
    """
    filter = []
    for category in categories:
        if isinstance(category, UnknownYelpCategory):
            filter.append(category.alias)
        else:
            filter.append(category.value)
    return ",".join(filter)