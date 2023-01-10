from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from usos_credentials import usos_key, usos_secret

import json
import requests
import oauth2


class Action_USOS_API_does_work(Action):

    def name(self) -> Text:
        return "action_USOS_API_does_work"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        input_prompt = tracker.latest_message["text"]
        base_url = "https://apps.usos.pw.edu.pl/services/users/search2?lang=en"
        request_url = base_url + "&query=" + input_prompt + "&among=staff"
        consumer = oauth2.Consumer(usos_key,usos_secret)
        client = oauth2.Client(consumer)
        staff_response = client.request(request_url, "POST")
        response = str(staff_response[1])[2:-1]
        response_dict = json.loads(response)
        response = "This are people that I found among staff of PW with help of USOS: \n"
        for hit in response_dict["items"]:
            response += hit["match"] + "\n"
        response += "I hope you are looking for one of them."
        
        dispatcher.utter_message(text=str(response))

        return []
