import requests
from urllib.parse import quote
from dataclasses import dataclass

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
        return response.json()
    else:
        raise WeatherAPIException(str(response.content))

def get_all_data():
    response = requests.get(WEATHER_API_URL)
    return response.json()