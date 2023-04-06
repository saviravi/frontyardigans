from api import get_cities, get_weather
import json
from tqdm import tqdm
import datetime

if __name__ == "__main__":
    city_name_mapping = {
        "Amsterdam, Netherlands": "amsterdam",
        "Barcelona, Spain": "barcelona",
        "Cairns, Australia": "cairns",
        "Cancun, Mexico": "cancun",
        "Hong Kong, China": "hong_kong",
        "Honolulu, Hawaii": "honolulu",
        "Istanbul, Turkey": "istanbul",
        "Las Vegas, USA": "las_vegas",
        "London, England": "london",
        "Los Angeles, USA": "los_angeles",
        "Madrid, Spain": "madrid",
        "Maui, Hawaii": "maui",
        "Mexico City, Mexico": "mexico_city",
        "Miami, USA": "miami",
        "New York City, USA": "new_york_city",
        "Orlando, USA": "orlando",
        "Paris, France": "paris",
        "Prague, Czech Republic": "prague",
        "Queenstown, New Zealand": "queenstown",
        "Rio de Janeiro, Brazil": "rio",
        "Rome, Italy": "rome",
        "San Francisco, USA": "san_francisco",
        "Seville, Spain": "seville",
        "Sydney, Australia": "sydney",
        "Tokyo, Japan": "tokyo",
        "Tulum, Mexico": "tulum",
        "Vienna, Austria": "vienna",
        "Venice, Italy": "venice",
        "Ibiza, Spain": "ibiza",
        "Lake Tahoe, USA": "lake_tahoe"
    }

    results = dict()
    cities = get_cities()

    for city in tqdm(cities):
        mapped_city = city_name_mapping[city]
        if mapped_city in ["venice", "ibiza", "lake_tahoe"]:
            continue

        results[mapped_city] = dict()
        weather = get_weather(city)
        for day in weather:
            date = datetime.datetime.strptime(day.date, "%a, %d %b %Y %H:%M:%S %Z")
            if int(date.month) not in results[mapped_city]:
                results[mapped_city][int(date.month)] = {
                    'min_f': 0,
                    'max_f': 0,
                    'precipitation': 0,
                    'count': 0
                }
            
            results[mapped_city][date.month]['min_f'] += day.min_f
            results[mapped_city][date.month]['max_f'] += day.max_f
            results[mapped_city][date.month]['precipitation'] += day.precipitation
            results[mapped_city][date.month]['count'] += 1

        for month in results[mapped_city]:
            count = results[mapped_city][month]['count']
            results[mapped_city][month]['min_f'] /= count
            results[mapped_city][month]['max_f'] /= count
            results[mapped_city][month]['precipitation'] /= count
        
    with open('weather.json', 'w') as f:
        json.dump(results, f)