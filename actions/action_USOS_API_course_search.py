from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
import requests


class Action_USOS_API_course_search(Action):

    def name(self) -> Text:
        return "action_USOS_API_course_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        input_prompt = tracker.latest_message["text"]
        base_url = "https://apps.usos.pw.edu.pl/services/courses/"
        course_response = requests.get(base_url + "search?lang=pl&name=" + input_prompt)
        course_respons_dict = json.loads(course_response.text)
        #print(course_respons_dict["items"][0]["course_id"])
        course_response = requests.get(base_url + "course?course_id=" + course_respons_dict["items"][0]["course_id"] + "&fields=name|description|profile_url")
        course_respons_dict = json.loads(course_response.text)

        response = ''

        for item in course_respons_dict.values():
            if type(item) is dict:
                response += item["pl"]
                response += '\n'
            else:
                response += item
                response += '\n'

        dispatcher.utter_message(text=str(response))

        return []
