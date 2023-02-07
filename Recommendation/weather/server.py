from vincenty import vincenty
from dataclasses import dataclass
from pickle import load
from tqdm import tqdm
import datetime

# Load data outputted from convert.py
with open('weather.pickle', 'rb') as f:
    weather_data = load(f)

# Sort (weather station index, latitude) by latitude
weather_lat_sorted = sorted([(i, s["LATITUDE"][0]) for i, s in enumerate(weather_data)], key=lambda p: p[1])
# Sort (weather station index, longitude) by weather station index
weather_long_sorted = sorted([(i, s["LONGITUDE"][0]) for i, s in enumerate(weather_data)], key=lambda p: p[0])

def bsearch_rec(arr, start, end, x):
    middle = (start + end) // 2
    if arr[middle][1] == x:
        return middle
    elif end - start == 1:
        return start
    elif x < arr[middle][1]:
        return bsearch_rec(arr, start, middle, x)
    else:
        return bsearch_rec(arr, middle, end, x)

def bsearch(arr, x):
    start = 0
    end = len(arr) - 1
    return bsearch_rec(arr, start, end, x)

Station = dict[str, any]
def closest_station(latitude: float, longitude: float, range: int = 30) -> tuple[Station, float]:
    # Get station in middle of search grid, this is the station that is closest to the given latitude
    lat_idx: int = bsearch(weather_lat_sorted, latitude)
    closest_lat_stations: tuple[int, float] = sorted(
        # Get (range / 2) closest weather stations to left and right of middle station by latitude
        weather_lat_sorted[max(lat_idx - (range // 2), 0) : min(lat_idx + (range // 2), len(weather_lat_sorted) - 1)],
        # Sort by weather station index
        key=lambda p: p[0]
        )
    
    candidate_long_stations: tuple[int, float] = sorted(
        # Get (station index, longitude) of the closest-by-latitude weather stations
        [weather_long_sorted[sidx] for (sidx, _) in closest_lat_stations],
        # Sort by weather station index
        key=lambda p: p[0])
    
    station_locations = [(i, latitude, longitude) for ((i, latitude), (_, longitude)) in zip(closest_lat_stations, candidate_long_stations)]
    distances = []
    for (i, s_lat, s_long) in station_locations:
        d = vincenty((latitude, longitude), (s_lat, s_long))
        if d is not None:
            distances.append((i, d))
    sorted_distances = sorted(distances, key=lambda p: p[1])
    closest_station_idx = sorted_distances[0][0]
    closest_station = weather_data[closest_station_idx]

    return closest_station, distances[0][1]

@dataclass
class WeatherDay:
    """Class representing one day of weather API result"""
    date: str
    min_f: float
    max_f: float
    rain_amt: float
    snow_amt: float

def get_weather(station, time_range: tuple[str, str]) -> list[WeatherDay]:
    end_date = datetime.datetime.strptime(time_range[1], "%Y-%m-%d")
    idxs = []
    for i, _ in enumerate(station["DATE"]):
        date = station["DATE"][i].to_pydatetime()
        if date <= end_date:
            idxs.append(i)

    days = []
    for i in idxs:
        days.append(station["MIN"][i])
    return days

lat = 40.915548
lon = -81.440739
#for _ in tqdm(range(10000)):
print("starting search")
station, dist = closest_station(lat, lon, range=300)
weather = get_weather(station, ("2022-01-01", "2022-01-05"))
print(weather)
