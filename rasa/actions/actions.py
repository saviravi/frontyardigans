# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

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
         dispatcher.utter_message(text=Recommendation.handleInput([]))
         return []
