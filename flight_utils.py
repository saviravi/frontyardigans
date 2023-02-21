import os
from enum import Enum
from duffel_api import Duffel
import airportsdata
import json
import es_utils
from elasticsearch import helpers
import utils


CLIENT = Duffel(access_token=os.environ.get("DUFFEL_TOK"))

# set up elastic search stuff

DATAFILE = "airportinfo.json"
DOCSFILE = "elasticdocs.json"

def create_airport_json():
	airportinfo = airportsdata.load(code_type="iata")
	with open(DATAFILE, "w") as outfile:
		json.dump(airportinfo, outfile)

def create_airport_index():
	properties = {
		"name": {"type": "text"},
		"iata": {"type": "keyword"},
		"city": {"type": "completion"},
		"subdivision": {"type": "text"},
		"country": {"type": "keyword"},
		"icao": {"type": "keyword"},
		"elevation": {"type": "float"},
		"location": {"type": "geo_point"},
		"timezone": {"type": "text"}
	}
	es_utils.ElasticSearcher.create_index("airport-info", properties=properties)
	return 

def generate_actions():
    elasticdocs = open(DOCSFILE, "w")
    with open(DATAFILE, mode="r") as file:
        info = json.loads(file.read())
        for airport in info.values():
            doc = {
                "_op_type": "index",
                "_index": "airport-info",
                "title": airport["iata"],
                "_id": airport["iata"],
                "name": airport["name"],
                "iata": airport["iata"],
                "city": airport["city"],
                "subdivision": airport["subd"],
                "country": airport["country"],
                "icao": airport["icao"],
                "elevation": airport["elevation"],
                "location": {"lat": float(airport["lat"]), "lon": float(airport["lon"])},
                "timezone": airport["tz"],

            }
            json.dump(doc, elasticdocs)
            elasticdocs.write(",\n")
    elasticdocs.close()

def load_airport_data():
	with open(DOCSFILE, mode="r") as file:
		docs = json.loads(file.read())
		helpers.bulk(es_utils.ElasticSearcher.es, docs)


# classes for getting flight offers

class FlightSlice(object):
	def __init__(self, origin, dest, depart_day, depart_month, depart_year):
		return {"origin": origin, "destination": dest, "departure_day": "{2}-{1}-{0}".format(depart_day, depart_month, depart_year) }

class Passenger(Enum):
	ADULT = "adult"
	CHILD = "child"
	INFANT = "infant_without_seat"

class Cabin(Enum):
	ECONOMY = "economy"
	PREMIUM_ECONOMY = "premium_economy"
	BUSINESS = "business"
	FIRST = "first"

class Airport(object):
	def __init__(self, name, iata, icao, lat, lon, time_zone, city, country):
		self.name = name
		self.iata = iata
		self.icao = icao
		self.lat = lat
		self.lon = lon
		self.time_zone = time_zone
		self.city = city
		self.country = country
		return
	
	def from_duffel(place):
		info = place.__dict__
		airport = Airport(info["name"], info.get("iata_code"), info["icao_code"], info["latitude"], info["longitude"], info["time_zone"], info["city"].__dict__["name"], info["iata_country_code"])
		return airport
	

	

# calls Duffel API

def get_flights(slices: list[FlightSlice], passengers: list(Passenger), cabin_class: Cabin, sort_by_price=True):
	""" gets a list of flight offers, sorted by total_amount or total_duration (default: by price) """
	passengers_list = [{"type": passenger.value} for passenger in passengers]
	reqs = CLIENT.offer_requests.create().slices(slices).passengers(passengers_list).cabin_class(cabin_class.value).execute()
	# CLIENT.offers.list(reqs.id, "total_amount" if sort_by_price else "total_duration", None)
	offers_list = list(CLIENT.offers.list(reqs.id, "total_amount" if sort_by_price else "total_duration", None))
	utils.log(msg=f"Found {len(offers_list)} offers")
	return offers_list



def pretty_print_flight_offers(offers_list):
	for offer in offers_list:
		offer = offer.__dict__
		# print(json.dumps(offer))
		print(offer)
		# print("\n\n\n\n")
		print(offer["slices"][0].__dict__.keys())
		simple_offer = {
		  "id": offer["id"],
		  "base_currency": offer["base_currency"],
		  "created_at": offer["created_at"],
		  "airline": offer["owner"].__dict__["name"],
		  "passengers": [passenger.__dict__["type"] for passenger in offer["passengers"]],
		  "slices": [{"origin": Airport.from_duffel(slice.__dict__["origin"]), "destination": Airport.from_duffel(slice.__dict__["destination"])} for slice in offer["slices"]],
		  "price": offer["total_amount"],
		  # "slices": [{"start_airport": slice.__dict__["destination"].__dict__["name"], "end_airport": slice.__dict__[""]} for slice in offer["slices"]],
		}
		print(simple_offer)









