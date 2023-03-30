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
from yelp import get_businesses_by_location_name, YelpAPIException
import datetime
from yelp import get_businesses_by_lat_long, YelpAPIException, any_of, YelpResult, YelpCommonCategories, YelpAllCategories
import random

sys.path.append(os.path.realpath(__file__)[:len(os.path.realpath(__file__)) - len("Recommendation.py")] + "flights")

import flight_utils
from flight_utils import Passenger
from flight_utils import Cabin


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
class Day_Schedule:
    """
    Class representing a day's schedule
    """
    # start_state and end_state should  be type Lodging or type Flight
    date: str
    activities: list[Activity]
    def __init__(self):
        self.date = ""
        self.activities = []

    def setDate(self, day):
        self.date = day
    def setActivities(self, stuff):
        for a in stuff:
            self.activities.append(a)
    def addActivity(self, a):
        self.activities.append(a)



@dataclass
class Schedule:
    """
    Class representing the lodging for the trip
    """
    day_schedule_list: list[Day_Schedule]
    def setList(self, day_list):
        self.day_schedule_list = day_list


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
    schedule: Schedule


@dataclass
class PrefCategory:
    """
    Class representing an airport retrieved from Duffel
    """
    value: str


@dataclass
class Airport:
    """
    Class representing an airport retrieved from Duffel
    """
    airport_name: str
    location: Location

def pprintSchedulue(sched):
    toReturn = ""
    for day in sched.day_schedule_list:
        toReturn += "Date: " + str(day.date) + "\n"
        for act in day.activities:
            toReturn += act.business.name + "\n"
        toReturn += "\n"
    return toReturn

def pprintDaySchedulue(day):
    for act in day.activities:
        print(act.business.name)
        print()
    print("-------------------")

def handleInput(inputData):
    """
    Handles input and returns a list of possible trips :)
    """
    print(pprintSchedulue(setUpSchedule("CMH", "ORD", datetime.date(2023, 12, 10),  5, [PrefCategory(value ="bars")])))
    return pprintSchedulue(setUpSchedule("CMH", "ORD", datetime.date(2023, 12, 10),  5, [PrefCategory(value ="bars")]))

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
    for x in range(number_of_activities):
        if x % 2 == 0:
            next_activity = get_next_activity(prefs, 1, previous_activities[-1], term="food")
        else:
            term = random.choice(prefs).value
            print(term)
            next_activity = get_next_activity(prefs, 1, previous_activities[-1], term = term)
        activities_to_return.append(next_activity)
        previous_activities.append(next_activity)
    activities_to_return += eventually
    return activities_to_return

def getLodging(airport):
    businesses = get_businesses_by_lat_long(
        airport.location.latitude, airport.location.longitude,
        radius=40000,
        price=1,
        term="hotels"
    )
    # Sort businesses by best rating
    businesses.sort(key=lambda b: b.rating, reverse=True)

    # Choose the next activity as the business with the best rating
    business = businesses[0]
    return Activity(
        business=business,
        time=None,
        duration=None
    )

def getDestinationAirportLocation(flights_in):
    lat = flights_in[0].slices[0].destination.latitude
    long = flights_in[0].slices[0].destination.longitude
    name = flights_in[0].slices[0].destination.name
    city_name = flights_in[0].slices[0].destination.city_name
    time_zone = flights_in[0].slices[0].destination.time_zone
    return Airport(airport_name=name, location=Location(city_name=city_name, latitude=lat, longitude=long, time_zone=time_zone))

def getOriginAirportLocation(flights_in):
    lat = flights_in[0].slices[0].origin.latitude
    long = flights_in[0].slices[0].origin.longitude
    name = flights_in[0].slices[0].origin.name
    city_name = flights_in[0].slices[0].origin.city_name
    time_zone = flights_in[0].slices[0].origin.time_zone
    return Airport(airport_name=name, location=Location(city_name=city_name, latitude=lat, longitude=long, time_zone=time_zone))


# Polymorphism Abuse
@dataclass
class AirportBusiness:
    """
    Class representing a business that is actually an airport
    """
    latitude: float
    longitude: float
    name: str
def flightInToActivity(flights_in):
    return Activity(business=AirportBusiness(name = flights_in[0].slices[0].destination.name, latitude = flights_in[0].slices[0].destination.latitude, longitude = flights_in[0].slices[0].destination.longitude), time="NONE", duration="NONE")
def flightOutToActivity(flights_out):
    return Activity(business=AirportBusiness(name = flights_out[0].slices[0].origin.name, latitude = flights_out[0].slices[0].origin.latitude, longitude = flights_out[0].slices[0].origin.longitude), time="NONE", duration="NONE")



#   returns a fully formed schedule
def setUpSchedule(start_city, destination, start_date,  duration, preferances):
    first_day = Day_Schedule()
    last_day = Day_Schedule()
    flights_in = flight_utils.get_flights([flight_utils.FlightSlice(start_city, destination, start_date.day, start_date.month, start_date.year).get_slice()], [Passenger.ADULT], Cabin.ECONOMY)
    airportIn = getDestinationAirportLocation(flights_in)
    flightInActivity = flightInToActivity(flights_in)
    lodging = getLodging(airportIn)
    date = start_date
    days = []
    #   Set up first day
    day_sched = Day_Schedule()
    activities_list = [flightInActivity, lodging]
    day_sched.setDate(date)
    first_day_activities = getDayOfActivities(preferances, activities_list, eventually = [lodging], immediates=[flightInActivity, lodging])
    #if isInMorning(flight_out.arrival_time):
    #    number_of_activities = 0
    #elif isInAfterNoon(flight_out.arrival_time):
    #    number_of_activities = 2
    #else:
    #    number_of_activities = 4
    number_of_activities = 2
    first_day_activities = first_day_activities[:number_of_activities]
    day_sched.setActivities(first_day_activities)
    date += datetime.timedelta(days = 1)
    days.append(day_sched)
    #   Set up middle days
    for _ in range(duration - 2):
        day_sched = Day_Schedule()
        day_sched.setDate(date)
        day_sched.setActivities(getDayOfActivities(preferances, activities_list, eventually = [lodging], immediates = [lodging]))
        date += datetime.timedelta(days = 1)
        days.append(day_sched)

    #   Set up final day
    final_date = start_date + datetime.timedelta(duration)
    flight_out = flight_utils.get_flights([flight_utils.FlightSlice(destination, start_city, final_date.day, final_date.month, final_date.year).get_slice()], [Passenger.ADULT], Cabin.ECONOMY)
    flightOutActivity = flightOutToActivity(flight_out)
    day_sched = Day_Schedule()
    day_sched.setDate(date)
    activities = []
    event = [lodging]
    #if isInMorning(flight_out.departure_time):
    #    number_of_activities = 0
    #    event = []
    #elif isInAfterNoon(flight_out.departure_time):
    #    number_of_activities = 2
    #else:
    #    number_of_activities = 4
    number_of_activities = 2
    activities = getDayOfActivities(preferances, activities_list, eventually = event, immediates = [lodging], number_of_activities=number_of_activities)

    activities.append(flightOutActivity)
    day_sched.setActivities(activities)
    days.append(day_sched)

    #   Return the list
    theSchedule = Schedule(day_schedule_list = days)
    theSchedule.setList(days)
    return theSchedule

def get_next_activity(activity_preferences: List[YelpCommonCategories],
                      price_preference: Union[int, str],
                      previous_activity: Activity,
                      radius_meters=3000,
                      exclude: List[YelpCommonCategories] = [], term="") -> Activity:
    """
    Finds a nearby activity that matches preferences but does not include the same type of activity as the previous activity done.
    """
    previous_latitude = previous_activity.business.latitude
    previous_longitude = previous_activity.business.longitude

    # Create filter given user preferences without last activity categories
    for previous_category in previous_activity.business.categories:
        if previous_category in activity_preferences:
            activity_preferences.remove(previous_category)
    for category in exclude:
        if category in activity_preferences:
            activity_preferences.remove(category)
    filter = any_of(activity_preferences)

    # Find a nearby activity within ~2 miles
    # TODO: filter by open time
    businesses = get_businesses_by_lat_long(
        previous_latitude, previous_longitude,
        radius=radius_meters,
        price=price_preference,
        categories=filter,
        term = term
    )

    # Sort businesses by best rating
    businesses.sort(key=lambda b: b.rating, reverse=True)

    # Choose the next activity as the business with the best rating
    upperbound = min(len(businesses), 15)
    idx = random.randrange(0, upperbound)
    business = businesses[idx]

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


handleInput(["cold"])
