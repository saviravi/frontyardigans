# Takes in key value pairs and recommends

from duffel_api import Duffel
from dotenv import load_dotenv
import os
from time import sleep
from typing import List
from dataclasses import dataclass

# Load environment variables
load_dotenv()
DUFFEL_ACCESS_TOKEN = os.getenv('DUFFEL_ACCESS_TOKEN')

def handleInput(inputData):
    print(inputData)
    return "This connection works"

@dataclass
class Location:
    """
    Class representing a location retrieved from Duffel
    """
    city_name: str
    airport_name: str
    latitude: float
    longitude: float
    time_zone: str

# This takes a couple of seconds and doesn't change between calls so could be cached
def get_duffel_locations() -> List[Location]:
    """
    Gets a list of Location objects from the list of Duffel airports.
    """
    result = []
    duffel = Duffel(access_token=DUFFEL_ACCESS_TOKEN)
    # Counter that resets once all airports from current requested page processed
    counter = 0
    for airport in duffel.airports.list(limit=200):
        # Reset once we've processed all airports on current page
        counter = (counter + 1) % 200
        # Wait a little before requesting the next page otherwise we get a rate limit error
        # See: https://github.com/duffelhq/duffel-api-python/blob/8de084dd54957ce55ea26d0357daccabcdf3de88/duffel_api/http_client.py#L36 
        if counter == 0:
            sleep(0.05)
    
        # Only save airports that have a defined city with them    
        if airport is None or airport.city is None:
            continue

        # Save city and airport name, latitude, longitude, and time zone
        result.append(Location(
            city_name=airport.city.name,
            airport_name=airport.name,
            latitude=airport.latitude,
            longitude=airport.longitude,
            time_zone=airport.time_zone
        ))
    
    return result

# Then get resturants and weather

# pick the one that matches the user's input the best
