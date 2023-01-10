from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from usos_credentials import usos_key, usos_secret

import json
import requests
import oauth2


class Action_USOS_API_free(Action):

    def name(self) -> Text:
        return "action_USOS_API_free"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        input_prompt = tracker.latest_message["text"]
        base_url = "https://apps.usos.pw.edu.pl/"
        request_url = base_url + input_prompt
        consumer = oauth2.Consumer(usos_key,usos_secret)
        client = oauth2.Client(consumer)
        usos_response = client.request(request_url, "POST")
        response = str(usos_response)
        response += "\n" + "I hope this helps!"
        dispatcher.utter_message(text=str(response))

        return []
