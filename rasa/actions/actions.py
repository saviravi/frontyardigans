# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

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

ALLOWED_ACTIVITIES = ["active life", "arts & entertainment", "arts and entertainment", "food", "shopping", "shops", "nightlife", "travel", "travelling" ]



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
         dispatcher.utter_message(text=Recommendation.handleInput([temp]))
         return []

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
            dispatcher.utter_message(text=f"We only allow the most popular 30 cities.")
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

class ActionClearSlots(Action):

 def name(self) -> Text:
     return "action_ClearSlots"

 def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("Slots are cleared.")

         return [AllSlotsReset()]