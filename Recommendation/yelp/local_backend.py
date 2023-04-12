from typing import Union

from .api import YelpResult
from .cities import City
from functools import reduce
from quadtree import QuadTree, Rect, Point
import matplotlib.pyplot as plt

KM_PER_DEGREE = 111.1

# Load all businesses and store in quadtree
all_businesses = list(map(City.load_businesses, list(City)))
all_businesses = reduce(lambda a, b: a + b, all_businesses)
qt = QuadTree(Rect(0, 0, 360, 180), 50, 0)

for i, b in enumerate(all_businesses):
    if b.latitude is None or b.longitude is None:
        continue
    qt.insert(Point(b.longitude, b.latitude, data=i))

def get_businesses_by_lat_long(latitude: float, longitude: float, radius=8050, price: Union[int, str]="1,2,3,4", limit=50, categories="", term="") -> list[YelpResult]:
    """
    Searches locally-stored Yelp data for businesses by latitude and longitude.
    """
    if latitude is None or longitude is None:
        print("warning: get_businesses_by_lat_long received None for latitude and/or longitude")
        return []

    radius_deg = (radius / 1000) / KM_PER_DEGREE
    nearby_points: list[Point] = qt.query_radius(longitude, latitude, radius_deg)
    nearby_businesses: list[YelpResult] = [all_businesses[p.data] for p in nearby_points]

    # Filter by price
    if type(price) == int:
        nearby_businesses = [b for b in nearby_businesses if b.price == price]
    else:
        prices = [int(p) for p in price.split(",")]
        nearby_businesses = [b for b in nearby_businesses if b.price in prices]

    # Filter by categories
    aliases = categories.split(",")
    if len(aliases) > 0 and aliases[0] != '':
        nearby_businesses = [b for b in nearby_businesses if any(list(map(lambda cat: cat.value in aliases, b.categories)))]

    # Filter by name (term)
    if term != "":
        nearby_businesses = [b for b in nearby_businesses if term.lower() in b.name.lower()]

    return nearby_businesses