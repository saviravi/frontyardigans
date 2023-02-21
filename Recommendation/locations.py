import os
from weather import closest_station_bf
import csv
import pickle

data_file = open('data.pickle', 'wb')
data = []

with open('locations.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    line_count = 0

    for row in reader:
        if line_count == 0:
            line_count += 1
            continue
        row[1] = float(row[1])
        row[2] = float(row[2])

        station, distance = closest_station_bf(row[1], row[2])
        data.append({
            "name": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "closest_station_name": station["NAME"][0],
            "date": station["DATE"],
            "min_f": station["MIN"],
            "max_f": station["MAX"],
            "precipitation": station["PRCP"]
        })
        print("closest station to %s is %s (%f km)" % (row[0], station["NAME"][0], distance))

pickle.dump(data, data_file)
data_file.close()