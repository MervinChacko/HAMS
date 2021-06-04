# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction
from typing import Any, Dict, List, NamedTuple, Optional, Set, Text, Tuple, Union
import requests
import csv
import json

class FindHospital(Action):

    def name(self) -> Text:
        return "find_hospital"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")

        data=[]
        with open("hosp.csv") as csvfile:
        	reader = csv.reader(csvfile)
        	for row in reader:
        		data.append(row)

        name = city

        col = [x[1] for x in data]

        if name in col:
        	for x in range(0,len(data)):
        		if name == data[x][1]:
        			dispatcher.utter_message(data[x][2]+"\n"+"Address:"+"\n"+data[x][5])

        else:
            dispatcher.utter_message(text="No hospitals found")

class Disease_request(Action):

    def name(self) -> Text:
        return "disease_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #symptom = tracker.get_slot("symptom")
        #dispatcher.utter_message(symptom)
        symptom = tracker.get_slot("symptom")

        url = 'http://192.168.1.7:5000/api/'

        data = symptom
        j_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url, data=j_data, headers=headers)
        dispatcher.utter_message("From the symptoms you have given, I think the disease is " + r.text)
