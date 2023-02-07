from vincenty import vincenty
from dataclasses import dataclass
from pickle import load
from tqdm import tqdm
import datetime
import os

# Load data outputted from convert.py
path = os.path.join(os.path.dirname(__file__), 'weather.pickle')
with open(path, 'rb') as f:
    weather_data = load(f)

# Sort (weather station index, latitude) by latitude
weather_lat_sorted = sorted([(i, s["LATITUDE"][0]) for i, s in enumerate(weather_data)], key=lambda p: p[1])
# Sort (weather station index, longitude) by weather station index
weather_long_sorted = sorted([(i, s["LONGITUDE"][0]) for i, s in enumerate(weather_data)], key=lambda p: p[0])

# Binary search recursive call on (weather station index, latitude)
def bsearch_rec(arr: list[tuple[int, float]], start: int, end: int, latitude: float):
    middle = (start + end) // 2
    if latitude == arr[middle][1]:
        return middle
    elif end - start == 1:
        return start
    elif latitude < arr[middle][1]:
        return bsearch_rec(arr, start, middle, latitude)
    else:
        return bsearch_rec(arr, middle, end, latitude)

# Binary search helper
def bsearch(arr: list[tuple[int, float]], latitude: float):
    start = 0
    end = len(arr) - 1
    return bsearch_rec(arr, start, end, latitude)

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
        # Get (weather station index, longitude) of the closest-by-latitude weather stations
        [weather_long_sorted[sidx] for (sidx, _) in closest_lat_stations],
        # Sort by weather station index
        key=lambda p: p[0])
    
    # Combine into (weather station index, latitude, longitude)
    station_locations = [
        (i, latitude, longitude) for ((i, latitude), (_, longitude)) in zip(closest_lat_stations, candidate_long_stations)
    ]

    # Calculate Vincenty distance for each candidate weather stsation
    distances: tuple[int, float] = []
    for (i, s_lat, s_long) in station_locations:
        d = vincenty((latitude, longitude), (s_lat, s_long))
        if d is not None:
            distances.append((i, d))
    
    # Sort [(weather station index, Vincenty distance)] by distance
    sorted_distances: list[tuple[int, float]] = sorted(distances, key=lambda p: p[1])
    # Get closest weather station index
    closest_station_idx = sorted_distances[0][0]
    # Get closest weather station
    closest_station = weather_data[closest_station_idx]

    # Return closest weather station and its corresponding distance to the given latitude and longitude
    return closest_station, distances[0][1]

@dataclass
class WeatherDay:
    """Class representing one day of weather API result"""
    date: str
    min_f: float
    max_f: float
    rain_amt_inches: float
    snow_amt_inches: float

def get_weather(station, time_range: tuple[str, str]) -> list[WeatherDay]:
    end_date = datetime.datetime.strptime(time_range[1], "%Y-%m-%d")
    idxs = []
    for i, _ in enumerate(station["DATE"]):
        date = station["DATE"][i].to_pydatetime()
        if date <= end_date:
            idxs.append(i)

    days = []
    for i in idxs:
        rain_amt = 0 if "99" in str(station["PRCP"][i]) else station["PRCP"][i]
        snow_amt = 0 if "99" in str(station["SNDP"][i]) else station["SNDP"][i]
        day = WeatherDay(
            date=station["DATE"][i],
            min_f=station["MIN"][i],
            max_f=station["MAX"][i],
            rain_amt_inches=rain_amt,
            snow_amt_inches=snow_amt
        )
        days.append(day)
    return days
