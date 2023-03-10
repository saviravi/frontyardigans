# Takes in key value pairs and recommends

from duffel_api import Duffel
from dotenv import load_dotenv
import os
from time import sleep
from typing import List, Union
from dataclasses import dataclass
import requests
import json
import sys
from urllib.parse import urlencode
from yelp import get_businesses_by_lat_long, YelpAPIException, YelpCategory, any_of, UnknownYelpCategory, YelpResult

# Load environment variables
load_dotenv()
DUFFEL_ACCESS_TOKEN = os.getenv('DUFFEL_ACCESS_TOKEN')




def readAPIKey(api_key_filename):
    with open(api_key_filename, 'r+') as keyFile:
        return keyFile.readline()

@dataclass
class Location:
    """
    Class representing a location
    """
    city_name: str
    latitude: float
    longitude: float
    time_zone: str

@dataclass
class Lodging:
    """
    Class representing the lodging for the trip
    """
    name: str
    price: int
    location: Location

@dataclass
class Activity:
    """
    Class representing an activity on your trip
    """
    business: YelpResult
    time: str
    duration: str

@dataclass
class Day_Schedulue:
    """
    Class representing a day's schedulue
    """
    # start_state and end_state should  be type Lodging or type Flight
    date: str
    start_state = None
    list[Activity]
    end_state = None



@dataclass
class Schedulue:
    """
    Class representing the lodging for the trip
    """
    day_schedulue_list = list[Day_Schedulue]



@dataclass
class Flight:
    """
    Class representing a flight
    """
    departure_time: str
    departure_location: Location
    arrival_location: Location
    arrival_time: str
    price: int
    airline: str

@dataclass
class Trip:
    """
    Class representing a trip
    """
    departure_flight: Flight
    return_flight: Flight
    schedule: Schedulue




@dataclass
class Airport:
    """
    Class representing an airport retrieved from Duffel
    """
    airport_name: str
    location: Location

def handleInput(inputData):
    """
    Handles input and returns a list of possible trips :)
    """
    print(inputData[0])
    return "Okay, let me find you some cities that are " + inputData[0] + "[TODO WEATHER API]"

# This takes a couple of seconds and doesn't change between calls so could be cached
def get_duffel_airports() -> List[Airport]:
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
        loc = Location(
        city_name=airport.city.name,
        latitude=airport.latitude,
        longitude=airport.longitude,
        time_zone=airport.time_zone)
        # Save city and airport name, latitude, longitude, and time zone
        result.append(Airport(
            airport_name=airport.name,
            location = loc
        ))

    return result

def get_next_activity(activity_preferences: List[YelpCategory],
                      price_preference: Union[int, str],
                      previous_activity: Activity,
                      radius_meters=3000) -> Activity:
    """

    """
    previous_latitude = previous_activity.business.latitude
    previous_longitude = previous_activity.business.longitude

    # Create filter given user preferences without last activity categories
    for previous_category in previous_activity.business.categories:
        if not isinstance(previous_category, UnknownYelpCategory) and previous_category in activity_preferences:
            activity_preferences.remove(previous_category)
    filter = any_of(activity_preferences)

    # Find a nearby activity within ~2 miles
    # TODO: filter by open time
    businesses = get_businesses_by_lat_long(
        previous_latitude, previous_longitude,
        radius=radius_meters,
        price=price_preference,
        categories=filter
    )

    # Sort businesses by best rating
    businesses.sort(key=lambda b: b.rating, reverse=True)

    # Choose the next activity as the business with the best rating
    business = businesses[0]

    # Convert business to activity
    activity = Activity(
        business=business,
        time=None,
        duration=None
    )

    return activity


def get_local_businesses_from_yelp(city_name, number_to_fetch, api_key_filename):
    # Reads the API key from a file
    YELP_API_KEY = readAPIKey(api_key_filename).strip()
    # Call the Fusion API
    url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=" + number_to_fetch
    headers = {"accept": "application/json",
                "Authorization": "Bearer " + API_KEY}
    response = requests.get(url, headers=headers, params = {"location": city_name})

    # Print all the business names
    data = response.json()["businesses"]
    return data
