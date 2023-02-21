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