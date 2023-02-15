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
        dispatcher.utter_message(text=f"OK! You liked visiting {city}.")
        return {"city": slot_value}

class ActionClearSlots(Action):

 def name(self) -> Text:
     return "action_ClearSlots"

 def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("Slots are cleared.")

         return [AllSlotsReset()]