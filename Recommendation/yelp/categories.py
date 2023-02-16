from enum import Enum

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



def any_of(*args) -> str:
    """
    Returns query string that combines multiple categories.
    """
    return ",".join([x.value for x in args])