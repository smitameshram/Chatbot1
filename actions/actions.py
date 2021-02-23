# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
import requests

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World! How you doing?")

        return []


class ActionSearchRestaurant(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'hotel':
                name = e['value']

            if name == "indian":
                message= "Indian1, Indian2, Indian3, Indian4, Indian5"
            
            if name == "chinese":
                message= "Chinese1, Chinese2, Chinese3, Chinese4, Chinese5 "


        dispatcher.utter_message(text=message)

        return []

class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        response= requests.get("https://api.covid19india.org/data.json").json()

        entities= tracker.latest_message['entities']
        print("Last Message Now ", entities)
        state= None
        for e in entities:
            if e['entity'] == "state":
                state= e['value']
        message= "Please enter correct state name"
        
        if state== "india":
            state= "Total"

        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                message= "Active: " + data["active"] + " Confirmed: " + data["confirmed"]


        dispatcher.utter_message(message)

        return []

class ActionCountryPrimeMinister(Action):

    def name(self) -> Text:
        return "action_country_prime"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot("name")
        country = tracker.get_slot("country")

        leader_name= ""
        if country.lower()=="us":
            leader_name= "Donald Trump"
        elif country.lower()=="india":
            leader_name= "Narendra Modi"
        else:
            leader_name= "Database not available"
        
        message = "{} belongs to {} and leader name is {}".format(name, country, leader_name)
        print(message)

        dispatcher.utter_message(text=message)

        return [SlotSet("leader",leader_name)]



