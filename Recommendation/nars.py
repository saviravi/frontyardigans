# import es_utils
import csv
import pickle
import sys
import os

METRICS_DICT = {}
CATEGORIES = ["active_life", "arts_n_ent", "food", "shopping", "nightlife", "travel"]

# create dictionary of city metrics indexed by city
def calc_city_metrics():
    with open("frontyardigans/Recommendation/weather/flyio/locations.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)
        for row in csv_reader:
            loc = row[0].split(", ")
            city_name = loc[0]
            country_name = loc[1]
            lat = row[1]
            lon = row[2]
            nars = {cat: calc_nar(city_name, cat) for cat in CATEGORIES}
            min_nar_cat = min(nars, key=nars.get)
            METRICS_DICT[city_name] = {
                "country_name": country_name, 
                "latitude": lat, 
                "longitude": lon,
                "nars": nars,
                "rnars": calc_rnar(nars),
                "wrnars": calc_wrnar(nars),
                "min_nar": (min_nar_cat, nars[min_nar_cat]),
            }
    return

def read_city_info(filename):
    pickleFile = open(filename,"rb")
    city_info = pickle.load(open(filename, "rb")) # list of yelp results
    
    print(city_info[234])



def calc_nar(city, category):
    """ calculates the Normalized Attribute Ratio for each category in a city"""
    num_in_cat = 0
    num_total = 1
    return num_in_cat / num_total

def calc_rnar(city_nars):
    """ calculates the ranking of each category's nar value in a city"""
    sorted_nars = [(k, v) for k, v in sorted(city_nars.items(), key=lambda item: item[1])]
    r_nars = {cat: rank for (cat, rank) in sorted_nars}
    return r_nars

def calc_wrnar(city_nars):
    """ weights the nar by the average star rating of that category then ranks """
    # get average star rating per category
    avg_ratings = {cat: stars for cat, stars in []}
    sorted_wnars = [(k, v) for k, v in sorted(city_nars.items(), key=lambda item: item[1]*avg_ratings[item[0]])]
    wr_nars = {cat: rank for (cat, rank) in sorted_wnars}
    return wr_nars

def calc_well_rounded_score():
    """ rank cities by their min nars"""
    sorted_minnars = [cat for cat, info in sorted(METRICS_DICT.items(), key=lambda item: item[1]["min_nar"])]
    max(METRICS_DICT, key=METRICS_DICT.get)
    
    return 


filename = "/Users/savitharavi/cse5914/frontyardigans/Recommendation/rome_businesses.pickle"
# read_city_info(directory + "/" + filename)
read_city_info(filename)
# print(sys.path)


# # Get a list of all files in the directory
# files = os.listdir(directory)

# # Print out the filenames
# for file in files:
#     print(file)