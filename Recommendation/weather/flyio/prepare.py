import os
from weather import closest_station_bf
import csv
import pickle
from weathertypes import Station, WeatherDay

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

        station_dict, distance = closest_station_bf(row[1], row[2])

        weather = []
        for i in range(len(station_dict["DATE"])):
            day = WeatherDay(
                date=station_dict["DATE"][i],
                min_f=station_dict["MIN"][i],
                max_f=station_dict["MAX"][i],
                precipitation=station_dict["PRCP"][i]
            )
            weather.append(day)

        station = Station(
            city_name=row[0],
            station_name=station_dict["NAME"][0],
            weather=weather
        )

        data.append(station)

        print("closest station to %s is %s (%f km)" % (row[0], station.station_name, distance))

pickle.dump(data, data_file)
data_file.close()