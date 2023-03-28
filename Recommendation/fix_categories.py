from yelp import UnknownYelpCategory, YelpCategory, parse_alias, YelpResult
from sys import argv
from pickle import load, dump

if len(argv) != 2:
    print("specify path")
    exit(1)
path = argv[1]

with open(path, 'rb') as f:
    data = load(f)

for business in data:
    business: YelpResult = business
    categories = []
    for c in business.categories:
        if type(c) == UnknownYelpCategory:
            categories.append(parse_alias(c.alias))
        elif type(c) == YelpCategory:
            categories.append(parse_alias(c.value))
        else:
            print("data is already in correct format")
            exit(1)
    business.categories = categories

file_name = path.split(".")[0] + "-conv.pickle"
with open(file_name, 'wb') as f:
    dump(data, f)