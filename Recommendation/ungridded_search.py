from typing import Iterable
import yelp
from pickle import dump
import os
import csv
from functools import partial
from dataclasses import asdict
from tqdm import tqdm

def get_cities() -> Iterable[tuple[str, float, float]]:
    """
    Returns list of (city name, latitude, longitude) from locations.csv.
    """
    with open(
        os.path.join(os.getcwd(), "weather", "flyio", "locations.csv"), 'r'
    ) as f:
        reader = csv.reader(f, delimiter=';')
        # Skip first line
        reader.__next__()
        # Return list of cities with latitude and longitude converted to floats
        return list(
            map(
                lambda l: (l[0], float(l[1]), float(l[2])),
                reader
            )
        )

def category_partials(lat, long) -> Iterable[tuple[yelp.YelpCategory, partial[list[yelp.YelpResult]]]]:
    """
    Returns iterable of (yelp category, partially applied function that takes nothing and returns list of Yelp businesses at specified latitude and longitude for the category).
    """
    return map(
        lambda cat: (cat, partial(yelp.get_businesses_by_lat_long,
                            lat, long, 8050, "1,2,3,4",
                            50, yelp.any_of([cat]))
        ),
        list(yelp.YelpCategory)
    )

def main():
    # Separate list of (city name, latitude, longitude) into lists of city name, latitude, and longitude
    names, lats, longs = zip(*get_cities())
    # Get iterable of cities and their get businesses functions for each category
    city_category_businesses = map(category_partials, lats, longs)
    
    # Where to save reuslts
    result = dict()

    # For each city and its list of (category, get businesses function)
    for city_name, city_categories in tqdm(zip(names, city_category_businesses), total=len(names)):
        result[city_name] = dict()
        
        # For each category and its get_businesses function
        for category, get_businesses in tqdm(city_categories, total=len(list(yelp.YelpCategory))):
            # Get list of businesses as dictionaries
            businesses = get_businesses()
            businesses = list(map(asdict, businesses))
            # Save result
            result[city_name][category.value] = businesses

    # Save all data
    with open('yelp_data.pickle', 'wb') as f:
        dump(result, f)

if __name__ == '__main__':
    main()