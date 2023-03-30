# import es_utils
import csv
import pickle
from yelp import YelpCategory, YelpResult, YelpActiveLifeCategory, YelpArtsAndEntertainmentCategory, YelpFoodCategory, YelpHotelsAndTravelCategory, YelpNightlifeCategory, YelpRestaurantsCategory, YelpShoppingCategory 
import statistics


METRICS_DICT = {} # key is city, value is [nars, rnar, wrnar, wrs]
CATEGORIES = ["active_life", "arts_n_ent", "food", "shopping", "nightlife", "travel", "restaurant"]

def get_city_info(filename):
    city_info = pickle.load(open(filename, "rb")) # list of yelp results
    cat_nums = {"active_life": 0, "arts_n_ent": 0, "food": 0, "shopping": 0, "nightlife": 0, "travel": 0, "restaurant": 0}
    active_life_rating = 0
    arts_n_ent_rating = 0
    food_rating = 0
    shopping_rating = 0
    nightlife_rating = 0
    travel_rating = 0
    restaurant_rating = 0
    for business in city_info:
        active_life = False
        arts_n_ent = False
        food = False
        shopping = False
        nightlife = False
        travel = False
        restaurant = False
        cats = business.__dict__['categories']
        rating = business.__dict__['rating']
        for cat in cats:
            if (type(cat) == YelpActiveLifeCategory):
                active_life = True
            if (type(cat) == YelpArtsAndEntertainmentCategory):
                arts_n_ent = True
            if (type(cat) == YelpFoodCategory):
                food = True
            if (type(cat) == YelpShoppingCategory):
                shopping = True
            if (type(cat) == YelpNightlifeCategory):
                nightlife = True
            if (type(cat) == YelpHotelsAndTravelCategory):
                travel = True
            if (type(cat) == YelpRestaurantsCategory):
                restaurant = True
        if active_life:
            cat_nums['active_life'] += 1
            active_life_rating += rating
        if arts_n_ent:
            cat_nums['arts_n_ent'] += 1
            arts_n_ent_rating += rating
        if food:
            cat_nums['food'] += 1
            food_rating += rating
        if shopping:
            cat_nums['shopping'] += 1
            shopping_rating += rating
        if nightlife:
            cat_nums['nightlife'] += 1
            nightlife_rating += rating
        if travel:
            cat_nums['travel'] += 1
            travel_rating += rating
        if restaurant:
            cat_nums['restaurant'] += 1
            restaurant_rating += rating
    cat_avg_rating = {"active_life": active_life_rating/cat_nums['active_life'], 
                   "arts_n_ent": arts_n_ent_rating/cat_nums['arts_n_ent'], 
                   "food": food_rating/cat_nums['food'], 
                   "shopping": shopping_rating/cat_nums['shopping'], 
                   "nightlife": nightlife_rating/cat_nums['nightlife'], 
                   "travel": travel_rating/cat_nums['travel'], 
                   "restaurant": restaurant_rating/cat_nums['restaurant']
    }
    return cat_nums, len(city_info), cat_avg_rating


def calc_nars(city_info, total_businesses):
    """ calculates the Normalized Attribute Ratio for each category in a city"""
    nars = {cat: (city_info[cat]/total_businesses) for cat in CATEGORIES}
    return nars

def calc_rnar(city_nars):
    """ calculates the ranking of each category's nar value in a city"""
    sorted_nars = [(k, v) for k, v in sorted(city_nars.items(), key=lambda item: item[1])]
    r_nars = {sorted_nars[6]: 1, sorted_nars[5]: 2, sorted_nars[4]: 3, sorted_nars[3]: 4, sorted_nars[2]: 5, sorted_nars[1]: 6, sorted_nars[0]: 7}
    return r_nars

def calc_wrnar(city_nars, avg_ratings):
    """ weights the nar by the average star rating of that category then ranks """
    # get average star rating per category
    sorted_wnars = [(k, v) for k, v in sorted(city_nars.items(), key=lambda item: item[1]*avg_ratings[item[0]])] # increasing order
    wr_nars = {sorted_wnars[6]: 1, sorted_wnars[5]: 2, sorted_wnars[4]: 3, sorted_wnars[3]: 4, sorted_wnars[2]: 5, sorted_wnars[1]: 6, sorted_wnars[0]: 7}
    return wr_nars

def calc_well_rounded_score(nars):
    """ rank cities by their min nars"""
    # get standard deviation of a city's nars: smaller std dev => more well-rounded 
    # sorted_minnars = [cat for cat, info in sorted(METRICS_DICT.items(), key=lambda item: item[1]["min_nar"])]
    # max(METRICS_DICT, key=METRICS_DICT.get)
    return statistics.stdev(nars)


# create dictionary of city metrics indexed by city
def calc_city_metrics():
    with open("/Users/savitharavi/cse5914/frontyardigans/Recommendation/weather/flyio/locations.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        for row in csv_reader:
            loc = row[0].split(", ")
            city_name = loc[0]
            if city_name == "Istanbul":
                break
            country_name = loc[1]
            lat = row[1]
            lon = row[2]
            num_cat_info, num_businesses, avg_ratings = get_city_info("/Users/savitharavi/cse5914/frontyardigans/Recommendation/" + city_name + "_businesses-conv.pickle")

            nars = calc_nars(num_cat_info, num_businesses)
            # min_nar_cat = min(nars, key=nars.get)

            METRICS_DICT[city_name] = {
                "country_name": country_name, 
                "latitude": lat, 
                "longitude": lon,
                "nars": nars,
                "rnars": calc_rnar(nars),
                "wrnars": calc_wrnar(nars, avg_ratings), 
                "wrs": calc_well_rounded_score(nars.values())
                # "min_nar": (min_nar_cat, nars[min_nar_cat]),
            }
    return



# filename = "/Users/savitharavi/cse5914/frontyardigans/Recommendation/paris_businesses-conv.pickle"
# num_cat_info, num_businesses, avg_ratings = get_city_info(filename)
# print("num per cat: ", num_cat_info.items())
# print("total number of businesses: ", num_businesses)
# print("avg ratings: ", avg_ratings)
# nars = calc_nars(num_cat_info, num_businesses)
# print("nars: ", nars)
# r_nars = calc_rnar(nars)
# wr_nars = calc_wrnar(nars, avg_ratings)
# print("rnars: ", r_nars)
# print("wrnars: ", wr_nars)
# wrs = calc_well_rounded_score(nars.values())
# print("wrs: ", wrs)

# METRICS_DICT["Paris"] = {"country": "France", }

calc_city_metrics()
for city, entry in METRICS_DICT.items():
    print(city)
    print(entry)
# print(METRICS_DICT)