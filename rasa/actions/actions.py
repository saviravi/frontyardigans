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
    "maui","cancun","sydney","venice","san francisco","miami","honolulu","rio de janeiro",
    "prague","hong kong","mexico city","los angeles","las vegas","orlando","ibiza","vienna",
    "seville","madrid","lake tahoe","cairns","queenstown","tulum" ]

ALLOWED_ACTIVITIES = ["being active", "active life", "arts & entertainment", "arts and entertainment", "food", "shopping", "shops", "nightlife", "travel", "travelling" ]



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
import Recommendation


class ActionGetRecommendation(Action):

 def name(self) -> Text:
     return "action_GetRecommendation"
 def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         temp = tracker.get_slot("temperature")
         city = tracker.get_slot("city")
         activity = tracker.get_slot("activity")
         startdate = tracker.get_slot("startdate")
         enddate = tracker.get_slot("enddate")
         # example input: ['cold', 'tulum', 'food', '04/04/2023', '04/04/2023']
         try:
            dispatcher.utter_message(text=Recommendation.handleInput([temp, city, activity, startdate, enddate]))
         except:
            dispatcher.utter_message(text="Oops! The program crashed. Try again.")
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
            buttons = list(map(lambda city: {"title": city.title(), "payload":city.title()},random.choices(ALLOWED_CITIES, k=3)))
            dispatcher.utter_message(text=f"We only allow the most popular 30 cities. Here are some suggestions: ", buttons=buttons)
            return {"city": None}
        dispatcher.utter_message(text=f"OK! You liked visiting {city}.")
        return {"city": slot_value}

    def validate_activity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `activity` value."""

        activity = tracker.get_slot("activity")
        if not activity:
            dispatcher.utter_message(text=f"No activity was entered")
            return {"activity": None}
        if slot_value.lower() not in ALLOWED_ACTIVITIES:
            dispatcher.utter_message(text=f"We only the 6 activities shown.")
            return {"activity": None}
        dispatcher.utter_message(text=f"OK! You enjoy {activity} the most.")
        return {"activity": slot_value}

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
         
         buttons = []
         buttons.append({"title": "I'm good." , "payload": "/mood_great"})
         buttons.append({"title": "I'm sad." , "payload": "/mood_unhappy"})
         buttons.append({"title": "I would like to travel" , "payload": "/ask_me_anything"})
         dispatcher.utter_message("OK! All slots have been reset!")
         dispatcher.utter_message("What can I help you with?", buttons=buttons)

         return [AllSlotsReset()]