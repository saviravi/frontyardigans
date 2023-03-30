from yelp import YelpRecommendationCategories, City
from stats import nar, wnar, category_index_mapping

def recommend_cities_nar(preference: YelpRecommendationCategories, limit=1, exclude: list[City] = []) -> City:
    cities = list(City)
    cities = [c for c in city if c not in exclude]
    nars = []
    for city in cities:
        nars.append((city, nar(City.load_businesses(city))))

    sorted_nars = sorted(nars, key=lambda city_nar: city_nar[1][category_index_mapping[preference]], reverse=True)

    cities, _ = list(zip(*sorted_nars))

    return cities[:limit]

def recommend_cities_wnar(preference: YelpRecommendationCategories, limit=1, exclude: list[City] = []) -> City:
    cities = list(City)
    cities = [c for c in city if c not in exclude]
    wnars = []
    for city in cities:
        wnars.append((city, wnar(City.load_businesses(city))))

    sorted_wnars = sorted(wnars, key=lambda city_nar: city_nar[1][category_index_mapping[preference]], reverse=True)

    cities, _ = list(zip(*sorted_wnars))

    return cities[:limit]