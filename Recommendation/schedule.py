from enum import Enum
from typing import Union
from yelp import City, YelpRecommendationCategories, any_of, YelpResult, YelpArtsAndEntertainmentCategory, YelpRestaurantsCategory, YelpFoodCategory, YelpNightlifeCategory, YelpActiveLifeCategory, YelpShoppingCategory
from yelp.local_backend import get_businesses_by_lat_long
from dataclasses import dataclass
import datetime
import sys
from functools import reduce
import os
import numpy as np
import pickle

sys.path.append(os.path.realpath(__file__)[:len(os.path.realpath(__file__)) - len("schedule.py")] + "flights")
from flights.flight_utils import get_flights, FlightSlice, Passenger, Cabin

city_info = pickle.load(open(os.path.realpath(__file__)[:len(os.path.realpath(__file__)) - len("schedule.py")] + "city_nar_info_weather.pickle", "rb")) # list of nar info for cities

@dataclass
class Flight:
    departure_time: datetime
    departure_airport: str
    arrival_time: datetime
    arrival_airport: str
    price: float

@dataclass
class Day:
    activities: list[YelpResult]

    def __str__(self):
        result = ""
        for activity in self.activities:
            result += "\t" + activity.name + "\n"
        
        return result

def get_best_of_category(cat_name):
    cat_wrnars = {}
    for city in city_info.keys():
        cat_wrnars[city] = city_info[city]['wrnars'][cat_name]
    sorted_wrnars = [k for k, v in sorted(cat_wrnars.items(), key=lambda item: item[1])]
    return sorted_wrnars


def pick_city(inputData):
    # cat1 = inputData[2]
    # cat2 = inputData[3]
    # cat3 = inputData[4]

    cat = inputData[2]
    best = get_best_of_category(city_info, cat)


    def adjust_cat_name(cat):
        if cat == "arts & entertainment":
            return "arts_n_ent"
        elif cat == "being active":
            return "active_life"
        elif cat == "food":
            return "restaurant"
    # cat1 = adjust_cat_name(cat1)
    # cat2 = adjust_cat_name(cat2)
    # cat3 = adjust_cat_name(cat3)

    # best1 = get_best_of_category(city_info, cat1)
    # best2 = get_best_of_category(city_info, cat2)
    # best3 = get_best_of_category(city_info, cat3)

    # print(best)
    rec_city = ""
    found = False
    i = 0
    while i < len(best) and not found:
        print(city_info[best[i]])
        print(city_info[best[i]]["weather"])
        if city_info[best[i]]["weather"] == inputData[0]:
            found = True
            rec_city = best[i]
    if not found:
        rec_city = best[0]
    
    print(rec_city)
    return rec_city

@dataclass
class Schedule:
    days: list[Day]
    hotel: YelpResult
    inbound_flight: Flight
    outbound_flight: Flight

    def already_scheduled(self, activity: YelpResult) -> bool:
        all_activities = reduce(lambda a, b: a + b, [day.activities for day in self.days])

        for act in all_activities:
            if act.id == activity.id:
                return True
            elif act.name == activity.name:
                return True
        
        return False

    def __repr__(self):
        result = ""
        for i, day in enumerate(self.days):
            result += "Day %d" % (i + 1) + "\n"
            if i == 0:
                result += "Inbound flight lands at %s at %s\n" % (self.inbound_flight.arrival_airport, self.inbound_flight.arrival_time)
            result += str(day)
            if i == len(self.days) - 1:
                result += "Outbound flight leaves from %s at %s\n" % (self.outbound_flight.departure_airport, self.outbound_flight.departure_time)
        
        return result


def get_flight(departure_airport: str, arrival_airport: str, date: datetime.date) -> Flight:
    """
    Returns a flight from the departure airport to the arrival airport on the specified day.

    `departure_airport` and `arrival_airport` are IATA city codes.
    """

    # if date.day()

    offers = get_flights(
        [FlightSlice(departure_airport, arrival_airport, date.day, date.month, date.year).get_slice()],
        [Passenger.ADULT],
        Cabin.ECONOMY
    )

    offer = offers[0]
    flight = offer.slices[0]
    segment = flight.segments[0]

    return Flight(
        departure_time=segment.departing_at,
        departure_airport=flight.origin.iata_city_code,
        arrival_time=segment.arriving_at,
        arrival_airport=flight.destination.iata_city_code,
        price=float(offer.total_amount)
    )

def get_hotel(city: City, price_preference: Union[int, str], radius=3000) -> YelpResult:
    """
    Finds and returns a good hotel (by rating and amount of ratings) within a 3km radius of the approximate city center.
    """
    # Get hotels within a 3km radius of the city center
    city_lat, city_long = city.get_city_center()
    hotels = get_businesses_by_lat_long(city_lat, city_long, radius=radius, price=price_preference, categories="hotels,hostels,resorts")
    
    # If no hotels in radius, expand
    if len(hotels) > 0:
        hotel = top_random_choice(hotels)
    else:
        return get_hotel(city, price_preference, radius * 1.25)

    return hotel

def top_random_choice(businesses: list[YelpResult], limit=30) -> YelpResult:
    """
    Randomly returns a business from the top n (default 30) choices sorted by number of ratings * average rating.
    
    `businesses` cannot be empty.
    """
    # Sort hotels by rating * number of ratings in descending order
    businesses = sorted(businesses, key=lambda b: b.rating * b.review_count, reverse=True)

    # Pick randomly from the top n places
    upper_bound = min(len(businesses), limit)
    random_business_idx = np.random.randint(0, upper_bound)

    business = businesses[random_business_idx]

    return business

def get_breakfast_activity(schedule: Schedule, price_preference: Union[int, str]) -> YelpResult:
    categories = any_of([YelpRestaurantsCategory.BreakfastAndBrunch,
                  YelpRestaurantsCategory.Cafes,
                  YelpFoodCategory.CoffeeAndTea])
    
    places = get_businesses_by_lat_long(schedule.hotel.latitude, schedule.hotel.longitude, price=price_preference, categories=categories)

    # Pick a place that hasn't been scheduled yet
    already_scheduled = True
    counter = 0
    while already_scheduled:
        place = top_random_choice(places)
        counter += 1
        already_scheduled = schedule.already_scheduled(place) and counter < 30

    return place
    
def get_non_breakfast_activity(schedule: Schedule, price_preference: Union[int, str], last_location: YelpResult = None) -> YelpResult:
    categories = list(YelpRestaurantsCategory)
    categories.remove(YelpRestaurantsCategory.BreakfastAndBrunch)
    categories = any_of(categories)
    
    if last_location is not None:
        places = get_businesses_by_lat_long(last_location.latitude, last_location.longitude, price=price_preference, categories=categories)
    else:
        places = get_businesses_by_lat_long(schedule.hotel.latitude, schedule.hotel.longitude, price=price_preference, categories=categories)

    # Pick a place that hasn't been scheduled yet
    already_scheduled = True
    counter = 0
    while already_scheduled:
        place = top_random_choice(places)
        counter += 1
        already_scheduled = schedule.already_scheduled(place) and counter < 30
    
    return place

def get_preferred_activity(schedule: Schedule, preference: Enum, last_location: YelpResult, price_preference: Union[int, str]) -> YelpResult:
    if preference == YelpNightlifeCategory:
        categories = list(YelpNightlifeCategory)
    elif preference == YelpActiveLifeCategory:
        categories = list(YelpActiveLifeCategory)
    elif preference == YelpShoppingCategory:
        categories = list(YelpShoppingCategory)
    elif preference == YelpArtsAndEntertainmentCategory:
        categories = list(YelpArtsAndEntertainmentCategory)
    else:
        categories = list(YelpNightlifeCategory) + list(YelpActiveLifeCategory) + list(YelpShoppingCategory) + list(YelpArtsAndEntertainmentCategory)

    categories = any_of(categories)
    places = get_businesses_by_lat_long(last_location.latitude, last_location.longitude, price=price_preference, categories=categories)

    # Pick a place that hasn't been scheduled yet
    already_scheduled = True
    counter = 0
    while already_scheduled:
        place = top_random_choice(places)
        counter += 1
        already_scheduled = schedule.already_scheduled(place) and counter < 30
    
    return place

def is_in_morning(time: datetime.time) -> bool:
    if time is None:
        return False
    return time.hour >= 8 and time.hour < 12

def is_in_afternoon(time: datetime.time) -> bool:
    if time is None:
        return False
    return time.hour >= 12 and time.hour < 18

def is_in_night(time: datetime.time) -> bool:
    if time is None:
        return False
    return time.hour >= 18 and time.hour <= 23

def add_full_day(schedule: Schedule, preference: Enum, price_preference: Union[int, str]):
    # Create new day
    schedule.days.append(Day([]))

    # Start at hotel
    schedule.days[-1].activities.append(schedule.hotel)

    # Add breakfast
    breakfast = get_breakfast_activity(schedule, price_preference)
    schedule.days[-1].activities.append(breakfast)

    # Add first activity
    activity_1 = get_preferred_activity(schedule, preference, breakfast, price_preference)
    schedule.days[-1].activities.append(activity_1)

    # Add second activity
    activity_2 = get_preferred_activity(schedule, preference, activity_1, price_preference)
    schedule.days[-1].activities.append(activity_2)

    # Add lunch
    lunch = get_non_breakfast_activity(schedule, price_preference, activity_2)
    schedule.days[-1].activities.append(lunch)

    # Add third activity
    activity_3 = get_preferred_activity(schedule, preference, lunch, price_preference)
    schedule.days[-1].activities.append(activity_3)

    # Add fourth activity
    activity_4 = get_preferred_activity(schedule, preference, activity_3, price_preference)
    schedule.days[-1].activities.append(activity_4)

    # Add dinner
    dinner = get_non_breakfast_activity(schedule, price_preference)
    schedule.days[-1].activities.append(dinner)

    # End at hotel
    schedule.days[-1].activities.append(schedule.hotel)

def add_arrival_day(schedule: Schedule, preference: Enum, price_preference: Union[int, str], arrival_time: datetime.time):
    # Create new day
    schedule.days.append(Day([]))

    # Start at hotel
    schedule.days[-1].activities.append(schedule.hotel)

    if is_in_morning(arrival_time):
        # Add breakfast
        breakfast = get_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(breakfast)

        # Add first activity
        activity_1 = get_preferred_activity(schedule, preference, breakfast, price_preference)
        schedule.days[-1].activities.append(activity_1)

        # Add second activity
        activity_2 = get_preferred_activity(schedule, preference, activity_1, price_preference)
        schedule.days[-1].activities.append(activity_2)

        # Add lunch
        lunch = get_non_breakfast_activity(schedule, price_preference, activity_2)
        schedule.days[-1].activities.append(lunch)

        # Add third activity
        activity_3 = get_preferred_activity(schedule, preference, lunch, price_preference)
        schedule.days[-1].activities.append(activity_3)

        # Add fourth activity
        activity_4 = get_preferred_activity(schedule, preference, activity_3, price_preference)
        schedule.days[-1].activities.append(activity_4)

        # Add dinner
        dinner = get_non_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(dinner)

        # End at hotel
        schedule.days[-1].activities.append(schedule.hotel)
    elif is_in_afternoon(arrival_time):
        # Add lunch
        lunch = get_non_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(lunch)

        # Add third activity
        activity_3 = get_preferred_activity(schedule, preference, lunch, price_preference)
        schedule.days[-1].activities.append(activity_3)

        # Add fourth activity
        activity_4 = get_preferred_activity(schedule, preference, activity_3, price_preference)
        schedule.days[-1].activities.append(activity_4)

        # Add dinner
        dinner = get_non_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(dinner)

        # End at hotel
        schedule.days[-1].activities.append(schedule.hotel)
    elif is_in_night(arrival_time):
        # Add dinner
        dinner = get_non_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(dinner)

        # End at hotel
        schedule.days[-1].activities.append(schedule.hotel)

def add_departure_day(schedule: Schedule, preference: Enum, price_preference: Union[int, str],  departure_time: datetime.time):
    # Create new day
    schedule.days.append(Day([]))

    # Start at hotel
    schedule.days[-1].activities.append(schedule.hotel)

    if is_in_morning(departure_time):
        # Add breakfast
        breakfast = get_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(breakfast)

        # End at hotel
        schedule.days[-1].activities.append(schedule.hotel)
    elif is_in_afternoon(departure_time):
        # Add breakfast
        breakfast = get_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(breakfast)

        # Add first activity
        activity_1 = get_preferred_activity(schedule, preference, breakfast, price_preference)
        schedule.days[-1].activities.append(activity_1)

        # Add second activity
        activity_2 = get_preferred_activity(schedule, preference, activity_1, price_preference)
        schedule.days[-1].activities.append(activity_2)

        # Add lunch
        lunch = get_non_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(lunch)

        # End at hotel
        schedule.days[-1].activities.append(schedule.hotel)
    elif is_in_night(departure_time):
        # Add breakfast
        breakfast = get_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(breakfast)

        # Add first activity
        activity_1 = get_preferred_activity(schedule, preference, breakfast, price_preference)
        schedule.days[-1].activities.append(activity_1)

        # Add second activity
        activity_2 = get_preferred_activity(schedule, preference, activity_1, price_preference)
        schedule.days[-1].activities.append(activity_2)

        # Add lunch
        lunch = get_non_breakfast_activity(schedule, price_preference, activity_2)
        schedule.days[-1].activities.append(lunch)

        # Add third activity
        activity_3 = get_preferred_activity(schedule, preference, lunch, price_preference)
        schedule.days[-1].activities.append(activity_3)

        # Add fourth activity
        activity_4 = get_preferred_activity(schedule, preference, activity_3, price_preference)
        schedule.days[-1].activities.append(activity_4)

        # Add dinner
        dinner = get_non_breakfast_activity(schedule, price_preference)
        schedule.days[-1].activities.append(dinner)

        # End at hotel
        schedule.days[-1].activities.append(schedule.hotel)

def create_schedule(city: City, preference: Enum, price_preference: Union[int, str], start_date: datetime.date, end_date: datetime.date) -> Schedule:
    inbound_flight = get_flight("CMH", city.airport_code, start_date)
    outbound_flight = get_flight(city.airport_code, "CMH", end_date)

    hotel = get_hotel(city, price_preference)

    schedule = Schedule([], hotel, inbound_flight, outbound_flight)

    add_arrival_day(schedule, preference, price_preference, arrival_time=inbound_flight.arrival_time)
    for _ in range((end_date - start_date).days - 1):
        add_full_day(schedule, preference, price_preference)
    add_departure_day(schedule, preference, price_preference, departure_time=outbound_flight.departure_time)

    return schedule

schedule = create_schedule(City.Paris, YelpNightlifeCategory, "1,2,3,4", datetime.date(2024, 1, 1), datetime.date(2024, 12, 25))
print(schedule)

def handleInput(input):
    # [temp, prev city, activity 1, activity 2, activity 3, start date, end date]
    city = pick_city(input)
    city_rec_name = city.lower().replace(" ", "_")
    if city == "Rio de Janeiro":
        city_rec_name = "rio"
    rec_city = City(city_rec_name)
    # start_date = input[5]
    start_date = datetime.strptime(input[5], '%d/%m/%Y').date()
    # end_date = input[6]
    end_date = datetime.strptime(input[6], '%d/%m/%Y').date()
    cat = ""
    if input[2] == "arts & entertainment":
        cat =  YelpArtsAndEntertainmentCategory
    elif input[2] == "being active":
        cat = YelpActiveLifeCategory
    elif input[2] == "food":
        cat = YelpRestaurantsCategory
    elif input[2] == "nightlife":
        cat = YelpNightlifeCategory
    elif input[2] == "shopping":
        cat = YelpShoppingCategory
    schedule = create_schedule(rec_city, cat, "1,2,3,4", start_date=start_date, end_date=end_date)
    return