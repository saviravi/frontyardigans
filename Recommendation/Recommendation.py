# Takes in key value pairs and recommends

from duffel_api import Duffel
from dotenv import load_dotenv
import os
from time import sleep
from typing import List
from dataclasses import dataclass
import requests
import json
import sys
from urllib.parse import urlencode
from yelp import get_businesses_by_location_name, YelpAPIException
import datetime
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
    location: Location
    price: int

@dataclass
class Day_Schedulue:
    """
    Class representing a day's schedulue
    """
    # start_state and end_state should  be type Lodging or type Flight
    date: str
    activities: list[Activity]
    def setDate(this, day):
        this.date = day
    def setActivities(this, stuff):
        for a in stuff:
            this.activities.append(a)
    def addActivity(this, a):
        this.activities.append(a)



@dataclass
class Schedulue:
    """
    Class representing the lodging for the trip
    """
    day_schedulue_list: list[Day_Schedulue]
    def setList(this, day_list):
        this.day_schedule_list = day_list


@dataclass
class Flight:
    """
    Class representing a flight
    """
    departure_time: datetime
    departure_location: Location
    arrival_location: Location
    arrival_time: datetime
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

def isInMorning(start_time):
    if start_time.hour < 12:
        return True
    return False
def isInAfternoon(start_time):
    if start_time.hour > 12 and start_time.hour < 16:
        return True
    return False


def getDayOfActivities(prefs, previous_activities, eventually=None, immediates=None, number_of_activities=6):
    activities_to_return = immediates
    for _ in range(number_of_activities):
        next_activity = getNextActivity(prefs, previous activities)
        activities_to_return.append(next_activity)
        previous_activities.append(next_activity)
    activities_to_return += eventually
    return activities_to_return

#   returns a fully formed schedulue
setUpSchedulue(start_city, destination, start_date,  duration, preferances):
    first_day = Day_Schedulue()
    last_day = Day_Schedulue()
    flight_in = getFlight(origin, destination, start_date)
    lodging = getLodging(destination, preferances)
    date = start_date
    days = []
    #   Set up first day
    day_sched = Day_Schedulue()
    activities_list = [flight_in, lodging]
    day_sched.setDate(date)
    first_day_activities = getDayOfActivities(preferances, activities_list, eventually = [lodging], immediates=[flight_in, lodging])
    if isInMorning(flight_out.arrival_time):
        number_of_activities = 0
    elif isInAfterNoon(flight_out.arrival_time):
        number_of_activities = 2
    else:
        number_of_activities = 4
    first_day_activities = [number_of_activities:]
    day_sched.setActivities(first_day_activities)
    date += datetime.timedelta(days = 1)
    days.append(day_sched)

    #   Set up middle days
    for _ in duration - 2:
        day_sched = Day_Schedulue()
        day_sched.setDate(date)
        day_sched.setActivities(getDayOfActivities(preferances, activities_list, eventually = [lodging], immediates = [lodging]))
        date += datetime.timedelta(days = 1)
        days.append(day_sched)

    #   Set up final day
    flight_out = getFlight(destination, origin, start_date + duration)
    day_sched = Day_Schedulue()
    day_sched.setDate(date)
    activites = []
    event = [lodging]
    if isInMorning(flight_out.departure_time):
        number_of_activities = 0
        event = []
    elif isInAfterNoon(flight_out.departure_time):
        number_of_activities = 2
    else:
        number_of_activities = 4
    activites = getDayOfActivities(preferances, activities_list, eventually = event, immediates = [lodging], number_of_activities=number_of_activities)
    activites += flight_out
    day_sched.setActivities(activities)
    days.append(day_sched)

    #   Return the list
    theSchedulue = Schedulue()
    theSchedule.setList(days)
    return theSchedule

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
