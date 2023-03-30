import requests
from urllib.parse import quote
from dataclasses import dataclass
import os
import json

@dataclass
class WeatherDay:
    date: str
    min_f: float
    max_f: float
    precipitation: float

@dataclass
class Station:
    city_name: str
    station_name: str
    weather: list[WeatherDay]

def weather_day_from_json(json: dict[str, any]) -> WeatherDay:
    return WeatherDay(
        date=json["date"],
        min_f=json["min_f"],
        max_f=json["max_f"],
        precipitation=json["precipitation"]
    )

def station_from_json(json: dict[str, any]) -> Station:
    return Station(
        city_name=json["city_name"],
        station_name=json["station_name"],
        weather=list(map(weather_day_from_json, json["weather"]))
    )

WEATHER_API_URL = "https://travis-weatherapi.fly.dev"
WEATHER_CITIES_API_URL_SUFFIX = "/cities"

class WeatherAPIException(Exception):
    """
    Raised when a weather API request fails.
    """
    pass

def get_cities():
    response = requests.get(
        WEATHER_API_URL
        + WEATHER_CITIES_API_URL_SUFFIX
    )
    return response.json()

def get_weather(city: str) -> list[WeatherDay]:
    response = requests.get(
        WEATHER_API_URL
        + WEATHER_CITIES_API_URL_SUFFIX
        + "/" + quote(city)
    )
    if response.status_code == 200:
        return list(map(weather_day_from_json, response.json()))
    else:
        raise WeatherAPIException(str(response.content))

def get_all_data() -> list[Station]:
    response = requests.get(WEATHER_API_URL)
    if response.status_code == 200:
        return list(map(station_from_json, response.json()))
    else:
        raise WeatherAPIException(str(response.content))

with open(os.path.join(os.path.dirname(__file__), "weather.json"), 'rb') as f:
    _weather = json.load(f)
def get_monthly_weather(city: str) -> dict:
    return _weather[city]