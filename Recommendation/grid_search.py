import matplotlib.pyplot as plt
from shapely import Polygon
from shapely.set_operations import intersection
from shapely.geometry import box
import numpy as np
from vincenty import vincenty
from yelp import get_businesses_by_lat_long, YelpCategory, any_of, parse_alias
import matplotlib.patches as pat
import pickle
import tqdm

# Longitude, Latitude 
paris_border = [
    (2.273343, 48.868569),
    (2.321587, 48.900109),
    (2.392419, 48.899560),
    (2.411381, 48.873888),
    (2.410545, 48.834255),
    (2.351983, 48.818099),
    (2.270276, 48.835540),
    (2.255496, 48.845634),
    (2.269439, 48.864350)
]

london_border = [
    (-0.190731, 51.515580),
    (-0.141376, 51.524125),
    (-0.091937, 51.526261),
    (-0.072024, 51.518571),
    (-0.085757, 51.497202),
    (-0.135882, 51.485659),
    (-0.185321, 51.480100),
    (-0.223086, 51.490790),
    (-0.193561, 51.515152)
]

rome_border = [
    (12.501892, 41.988588),
    (12.582092, 41.957448),
    (12.615738, 41.906365),
    (12.573166, 41.812267),
    (12.513428, 41.793840),
    (12.393265, 41.813802),
    (12.372665, 41.865470),
    (12.388458, 41.958469),
    (12.493515, 41.986546)
]

barcelona_border = [
    (2.183876, 41.379642),
    (2.116585, 41.342794),
    (2.090836, 41.344856),
    (2.102509, 41.384022),
    (2.140961, 41.420847),
    (2.194519, 41.448131),
    (2.226791, 41.416213),
    (2.187653, 41.375778)
]

amsterdam_border = [
    (4.912262, 52.419173),
    (4.974060, 52.380629),
    (4.961700, 52.350021),
    (5.007706, 52.324849),
    (4.939728, 52.298402),
    (4.909515, 52.329465),
    (4.810638, 52.337017)
]

fig, ax = plt.subplots()

london = Polygon(amsterdam_border)

minx, miny, maxx, maxy = london.bounds
delta = 0.007
x = np.arange(minx, maxx + delta, delta)
y = np.arange(miny, maxy + delta, delta)

search_size = int(vincenty((minx, miny), (minx + delta, miny)) * 670)

grid = []
max_diameter = 0
for i in range(len(x) - 1):
    for j in range(len(y) - 1):
        grid.append(
            box(
                x[i], y[j],
                x[i + 1], y[j + 1]
            )
        )

x, y = london.exterior.xy
plt.plot(x, y, label="London border", linewidth=3)

# for b in grid:
#     x, y  = b.exterior.xy
#     plt.plot(x, y)

search_points = []

for b in grid:
    i = intersection(london, b)
    if not i.is_empty:
        x, y = i.exterior.xy
        #plt.plot(x, y, color="tab:blue")
        cx, cy = zip(*i.centroid.coords)
        search_points.append((cy[0], cx[0]))
        c = pat.Circle((cx, cy), radius=delta*0.67, fill=False)
        ax.add_patch(c)
        plt.plot(cx, cy, '.', color='tab:red')

print("search will take %d API calls" % (len(grid) * 5))

# with open('businesses.pickle', 'rb') as f:
#     businesses = pickle.load(f)

# nar = dict()
# for b in businesses:
#     for c in b.categories:
#         if type(c) == YelpCategory:
#             t = type(parse_alias(c.value))
#         else:
#             t = type(parse_alias(c.alias))
#     if t not in nar:
#         nar[t] = 0
#     nar[t] += 1
#     #plt.plot(b.longitude, b.latitude, 'x', color='c')

# print(nar)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("London Gridded Search")
plt.show()

all_businesses = []
found_ids = set()
for lat, long in tqdm.tqdm(search_points):
    duplicates = 0

    food_businesses = get_businesses_by_lat_long(lat, long, search_size, categories=any_of([YelpCategory.AllFood]))
    active_life_businesses = get_businesses_by_lat_long(lat, long, search_size, categories=any_of([YelpCategory.AllActiveLife]))
    arts_entertainment_businesses = get_businesses_by_lat_long(lat, long, search_size, categories=any_of([YelpCategory.AllArtsAndEntertainment]))
    nightlife_businesses = get_businesses_by_lat_long(lat, long, search_size, categories=any_of([YelpCategory.AllNightlife]))
    shopping_businesses = get_businesses_by_lat_long(lat, long, search_size, categories=any_of([YelpCategory.AllShopping]))
    
    businesses = food_businesses + active_life_businesses + arts_entertainment_businesses + nightlife_businesses + shopping_businesses
    print("found %d, %d, %d, %d, %d businesses" % (len(food_businesses), len(active_life_businesses), len(arts_entertainment_businesses), len(nightlife_businesses), len(shopping_businesses)))
    for b in businesses:
        if b.id in found_ids:
            duplicates += 1
        else:
            found_ids.add(b.id)
            all_businesses.append(b)

    print("found %d duplicates" % duplicates)
print("found", len(all_businesses), "total")
with open('amsterdam_businesses.pickle', 'wb') as f:
    pickle.dump(all_businesses, f)