import pickle
import glob
from dataclasses import asdict
from yelp import YelpResult
import os
import json

def to_dict(business: YelpResult) -> dict:
    business = asdict(business)
    categories = [c.value for c in business['categories'] if c is not None]
    business["categories"] = categories

    return business

f_paths = glob.glob("yelp/business_data/*.pickle")
for path in f_paths:
    with open(path, 'rb') as f:
        file_name = os.path.basename(path).split(".")[0] + ".json"
        business_data = pickle.load(f)
        with open("yelp/business_data/%s" % file_name, 'w') as out_f:
            dict_business_data = list(map(to_dict, business_data))
            json.dump(dict_business_data, out_f)