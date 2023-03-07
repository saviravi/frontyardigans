from typing import Iterable
import yelp
from pickle import dump
import os
import csv
from functools import partial
from tqdm import tqdm

def get_cities() -> Iterable[tuple[str, float, float]]:
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

def category_partials(lat, long) -> Iterable[partial]:
    return map(
        lambda cat: (cat, partial(yelp.get_businesses_by_lat_long,
                            lat, long, 8050, "1,2,3,4",
                            50, yelp.any_of([cat]))
        ),
        list(yelp.YelpCategory)
    )

def main():
    names, lats, longs = zip(*get_cities())
    city_category_businesses = map(category_partials, lats, longs)
    
    result = dict()

    for city_name, city_categories in tqdm(zip(names, city_category_businesses), total=len(names)):
        result[city_name] = dict()
        
        for category, get_businesses in tqdm(city_categories, total=len(list(yelp.YelpCategory))):
            result[city_name][category] = get_businesses()

    with open('yelp_data.pickle', 'wb') as f:
        dump(result, f)

if __name__ == '__main__':
    main()