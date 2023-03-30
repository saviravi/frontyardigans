from yelp import YelpResult
from sys import argv
from pickle import load, dump
import matplotlib.pyplot as plt

if len(argv) != 2:
    print("specify path")
    exit(1)
path = argv[1]

businesses: list[YelpResult]
with open(path, 'rb') as f:
    businesses = load(f)

counts = dict()
for b in businesses:
    for c in b.categories:
        if c is None:
            continue
        if type(c).__name__ not in counts:
            counts[type(c).__name__] = 0
        
        counts[type(c).__name__] += 1

print(counts)