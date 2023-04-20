# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import random
import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker, FormValidationAction

from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSayTemperature(Action):

    def name(self) -> Text:
        return "action_say_temperature"

ALLOWED_TEMP = ["hot","cold"]

ALLOWED_CITIES = ["paris", "london", "rome", "barcelona", "amsterdam", "istanbul", "tokyo", "new york city",
    "maui","cancun","sydney",
    # "venice",
    "san francisco","miami","honolulu","rio de janeiro",
    "prague","hong kong","mexico city","los angeles","las vegas","orlando",
    # "ibiza",
    "vienna",
    "seville","madrid",
    # "lake tahoe",
    "cairns",
    # "queenstown",
    # "tulum"
    ]

ALLOWED_ACTIVITIES = ["being active", "active life", "arts & entertainment", "arts and entertainment", "food", "shopping", "shops", "nightlife", "travel", "travelling" ]

PHOTO_URLS = {
    "paris":"https://media.cnn.com/api/v1/images/stellar/prod/230324090551-01-visiting-france-during-protests-what-to-know-top.jpg?c=16x9&q=h_720,w_1280,c_fill",
    "london": "https://assets.editorial.aetnd.com/uploads/2019/03/topic-london-gettyimages-760251843-feature.jpg",
    "rome": "https://www.travelandleisure.com/thmb/QDUywna6SQbiQte-ZmrJmXcywp0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/rome-italy-lead-ROMETG0521-7bd455d3c2b545219498215df7143e0d.jpg",
    "barcelona": "https://media.architecturaldigest.com/photos/5956513b8afbdc247fb26215/4:3/w_4628,h_3471,c_limit/Barcelona_Travel_Guide_GettyImages-543868651.jpg",
    "amsterdam": "https://www.travelandleisure.com/thmb/_3nQ1ivxrnTKVphdp9ZYvukADKQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/amsterdam-nl-AMSTERDAMTG0521-6d2bfaac29704667a950bcf219680640.jpg",
    "istanbul" : "https://a.cdn-hotels.com/gdcs/production6/d781/3bae040b-2afb-4b11-9542-859eeb8ebaf1.jpg",
    "tokyo" : "https://media.cntraveler.com/photos/63482b255e7943ad4006df0b/3:2/w_6000,h_4000,c_limit/tokyoGettyImages-1031467664.jpeg",
    "new york city": "https://www.travelandleisure.com/thmb/91pb8LbDAUwUN_11wATYjx5oF8Q=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/new-york-city-evening-NYCTG0221-52492d6ccab44f328a1c89f41ac02aea.jpg",
    "maui" : "https://www.mauiinformationguide.com/wp-content/uploads/2022/04/mauihawaii.jpg",
    "cancun": "https://res.cloudinary.com/simpleview/image/upload/v1569364497/clients/quintanaroo/Cancun_oficial_22261778-3d43-4408-bc3b-c971b4d82a63.jpg",
    "sydney": "https://www.travelandleisure.com/thmb/6JVbKFFtu7AeQu5rHioeDpcPxko=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/sydney-australia-SYDNEYTG0621-2dcacc38417541f689e293d397da9eaf.jpg",
    "venice": "https://www.travelandleisure.com/thmb/ubTOmrdr85740HVyLq_nGhinVWE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/venice-italy-VENICETG0521-cddab02114ae44f08ba49c8c3fc9158c.jpg",
    "san francisco": "https://www.nomadicmatt.com/wp-content/uploads/2018/04/sanfranguide.jpg",
    "miami": "https://a.travel-assets.com/findyours-php/viewfinder/images/res70/471000/471674-Miami.jpg",
    "honolulu": "https://www.gohawaii.com/sites/default/files/styles/image_gallery_bg_xl/public/hero-unit-images/Oahu%20Honolulu%20View%20from%20Tantalus%20lookout.jpg?itok=OP6Ph4CL",
    "rio de janeiro": "https://www.travelandleisure.com/thmb/x-LBqpaBsbUqGYtHu8gLnRMxPvg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/rio-de-janeiro-RIOTG0721-c59c5e2f3a354e798587d5ef925b23e3.jpg",
    "prague": "https://images.squarespace-cdn.com/content/v1/5a87961cbe42d637c54cab93/1561390086605-O99XX2CO0H9JJQSIAV45/prague-guide-for-first-time-visitors.jpg",
    "hong kong": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Hong_Kong_Harbour_Night_2019-06-11.jpg",
    "mexico city": "https://i.natgeofe.com/n/73d9e4e3-4884-4e93-ac41-6be6a90079f5/mexico-city-travel%20(1).jpg?w=2880&h=1920",
    "los angeles": "https://upload.wikimedia.org/wikipedia/commons/3/32/20190616154621%21Echo_Park_Lake_with_Downtown_Los_Angeles_Skyline.jpg",
    "las vegas": "https://vegasexperience.com/wp-content/uploads/2023/01/Photo-of-Las-Vegas-Downtown-1920x1280.jpg",
    "orlando": "https://cdn.britannica.com/07/201607-050-0B5774CB/Orlando-Florida-aerial-cityscape-towards-Eola-Lake.jpg",
    "ibiza": "https://d1e00ek4ebabms.cloudfront.net/production/032489af-2ff3-4cc1-8768-9176a1a30d35.jpg",
    "vienna": "https://media.architecturaldigest.com/photos/561d6d06ed5c90fd5d6127ee/16:9/w_2640,h_1485,c_limit/Vienna%20Travel.jpg",
    "seville": "https://static.independent.co.uk/s3fs-public/thumbnails/image/2018/01/01/19/istock-494611784.jpg",
    "madrid": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/28/6a/f5/4c/caption.jpg?w=500&h=300&s=1",
    "lake tahoe": "https://travelnevada.com/wp-content/uploads/2022/04/SilverStateReset_Featured-scaled.jpg",
    "cairns": "https://img.traveltriangle.com/blog/wp-content/uploads/2019/12/Cover-image-of-Water-sports_18th-dec.jpg",
    "queenstown": "https://upload.wikimedia.org/wikipedia/commons/c/c9/Queenstown_1_%288168013172%29.jpg",
    "tulum":"https://a.cdn-hotels.com/gdcs/production73/d1624/45ab7e53-4363-41f8-8783-78765ac502ee.jpg"
}


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sys
import os

#import Recommendation
print("--------------")
print(os.path.realpath(__file__)[:len(os.path.realpath(__file__)) - len("rasa\\actions\\actions.py")] + "Recommendation")
print("--------------")

sys.path.append(os.path.realpath(__file__)[:len(os.path.realpath(__file__)) - len("rasa\\actions\\actions.py")] + "Recommendation")
import schedule
import summary

class ActionGetRecommendation(Action):

 def name(self) -> Text:
     return "action_GetRecommendation"
 def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         temp = tracker.get_slot("temperature")
         city = tracker.get_slot("city")
         activity1 = tracker.get_slot("activity1")
         activity2 = tracker.get_slot("activity2")
         activity3 = tracker.get_slot("activity3")
         startdate = tracker.get_slot("startdate")
         enddate = tracker.get_slot("enddate")
         input_values = [temp, city, activity1, activity2, activity3, startdate, enddate]
         # example input: ['cold', 'tulum', 'food', etc.. , '04/04/2023', '04/04/2023']
         if None in input_values:
            buttons = [{"title": "Ask me anything!" , "payload": "/ask_me_anything"}] if not tracker.active_loop else []
            dispatcher.utter_message(text="We still need more information before making your itinerary.", buttons=buttons)
            return []

         try:
            try:
                rec_city = schedule.pick_city([temp, activity1, activity2, activity3])
            except Exception as err1:
                rec_city = city
                print("Error in city picker: " + str(err1))
                print(f"Defaulted to user-chosen city: {city} instead.")
            itinerary = f"Destination: {rec_city.title()}\n\n" + str(schedule.handleSlotInputs(rec_city, activity1, activity2, activity3, startdate, enddate))

            if rec_city.lower() in PHOTO_URLS:
                dispatcher.utter_message(image=PHOTO_URLS[rec_city.lower()])
            dispatcher.utter_message(text=f"Let's go to {rec_city.title()}")
            try:
                city_summary = summary.get_city_info(rec_city.title())
                print(city_summary)
                dispatcher.utter_message(text=city_summary)
            except Exception as err2:
                print("Error in city summary: " + str(err2))
            
            dispatcher.utter_message(text=f"Your {rec_city.title()} itinerary has been generated", attachment=itinerary)
         except Exception as error:
            buttons = [{"title": "Generate" , "payload": "/generate_recommendation"}]
            dispatcher.utter_message(text=f"Oops! The program crashed. Try again. Error: {error}", buttons=buttons)
            print("Error: " + str(error))
         return []

from datetime import datetime
class ValidateTravelForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_travel_form"
    def validate_temperature(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `temperature` value."""
        if slot_value.lower() not in ALLOWED_TEMP:
            dispatcher.utter_message(text=f"We only accept temps: hot/cold")
            return {"temperature": None}
        temperature = tracker.get_slot("temperature")
        dispatcher.utter_message(text=f"OK! You prefer {temperature} weather.")
        return {"temperature": slot_value}

    def validate_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `city` value."""

        city = tracker.get_slot("city")
        if not city:
            dispatcher.utter_message(text=f"No city was entered")
            return {"city": None}
        if slot_value.lower() not in ALLOWED_CITIES:
            buttons = list(map(lambda city: {"title": city.title(), "payload":city.title()},random.sample(ALLOWED_CITIES, len(ALLOWED_CITIES))[:3]))
            dispatcher.utter_message(text=f"We only allow the most popular 30 cities. Here are some suggestions: ", buttons=buttons)
            return {"city": None}
        dispatcher.utter_message(text=f"OK! You liked visiting {city}.")
        return {"city": slot_value}

    def validate_activity1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `activity1` value."""

        activity = tracker.get_slot("activity1")
        if not activity:
            dispatcher.utter_message(text=f"No activity was entered")
            return {"activity1": None}
        if slot_value.lower() not in ALLOWED_ACTIVITIES:
            dispatcher.utter_message(text=f"We only the 6 activities shown.")
            return {"activity1": None}
        dispatcher.utter_message(text=f"OK! Your favorite activity is: {activity}.")
        return {"activity1": slot_value}
    def validate_activity2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `activity2` value."""

        activity1 = tracker.get_slot("activity1")
        activity2 = tracker.get_slot("activity2")
        if not activity2:
            dispatcher.utter_message(text=f"No activity was entered")
            return {"activity2": None}
        if slot_value.lower() not in ALLOWED_ACTIVITIES:
            dispatcher.utter_message(text=f"We only the 6 activities shown.")
            return {"activity2": None}
        if activity1 == activity2:
            dispatcher.utter_message(text=f"You already selected this activity")
            return {"activity2": None}
        dispatcher.utter_message(text=f"OK! Your second favorite activity is: {activity2}.")
        return {"activity2": slot_value}

    def validate_activity3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `activity3` value."""

        activity1 = tracker.get_slot("activity1")
        activity2 = tracker.get_slot("activity2")
        activity3 = tracker.get_slot("activity3")
        if not activity3:
            dispatcher.utter_message(text=f"No activity was entered")
            return {"activity3": None}
        if slot_value.lower() not in ALLOWED_ACTIVITIES:
            dispatcher.utter_message(text=f"We only the 6 activities shown.")
            return {"activity3": None}
        if activity3 == activity1 or activity3 == activity2:
            dispatcher.utter_message(text=f"You already selected this activity")
            return {"activity3": None}
        dispatcher.utter_message(text=f"OK! Your third favorite activity is: {activity3}.")
        return {"activity3": slot_value}

    def validate_startdate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `startddate` value."""
        startdate = tracker.get_slot("startdate")
        startdate = re.sub(r'[^0-9\/]', '', startdate)
        if not re.match(r"^(0[1-9]|1[012])\/(0[1-9]|[12][0-9]|3[01])\/(19|20)\d\d$", startdate):
            dispatcher.utter_message(text=f"Sorry! I didn't quite understand. Try using the date selector!")
            return {"startdate": None}
        todaysDate = datetime.now()
        if datetime.strptime(startdate, '%m/%d/%Y') <  todaysDate:
           dispatcher.utter_message(text=f"Start date must be after today ({ todaysDate.strftime('%m/%d/%Y') })")
           return {"startdate": None}
        dispatcher.utter_message(text=f"OK! You want your vacation to start on {startdate}")
        return {"startdate": startdate}

    def validate_enddate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `enddate` value."""
        enddate = tracker.get_slot("enddate")
        startdate = tracker.get_slot("startdate")
        enddate = re.sub(r'[^0-9\/]', '', enddate)
        if not re.match(r"^(0[1-9]|1[012])\/(0[1-9]|[12][0-9]|3[01])\/(19|20)\d\d$", enddate):
            dispatcher.utter_message(text=f"Sorry! I didn't quite understand. Try using the date selector!")
            return {"enddate": None}
        if startdate is not None and datetime.strptime(enddate, '%m/%d/%Y') <= datetime.strptime(startdate, '%m/%d/%Y'):
           dispatcher.utter_message(text=f"End date must be after start date ({startdate})")
           return {"enddate": None}
        dispatcher.utter_message(text=f"OK! You want your vacation to end on {enddate}")
        return {"enddate": enddate}


class ActionClearSlots(Action):

 def name(self) -> Text:
     return "action_ClearSlots"

 def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("OK! All slots have been reset!")
         if (not tracker.active_loop):
            buttons = []
            buttons.append({"title": "I'm good." , "payload": "/mood_great"})
            buttons.append({"title": "I'm sad." , "payload": "/mood_unhappy"})
            buttons.append({"title": "I would like to travel" , "payload": "/ask_me_anything"})
            dispatcher.utter_message("What can I help you with?", buttons=buttons)

         return [AllSlotsReset()]
