from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from usos_credentials import usos_key, usos_secret

import json
import oauth2


class Action_USOS_API_theses_search(Action):

    def name(self) -> Text:
        return "action_USOS_API_theses_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        input_prompt = tracker.get_slot("usos_thesis_name")
        base_url = "https://apps.usos.pw.edu.pl/services/theses/search?lang=en"
        base_url2 = "https://apps.usos.pw.edu.pl/services/theses/thesis?ths_id="
        request_url = base_url + "&query=" + input_prompt
        consumer = oauth2.Consumer(usos_key, usos_secret)
        client = oauth2.Client(consumer)
        thesis_response = client.request(request_url, "POST")
        response = str(thesis_response[1])[2:-1]
        response_dict = json.loads(response)
        bot_message = ''
        bot_message += "This are theses that I found in PW database with help of USOS: \n"
        for hit in response_dict["items"]:
            ths_id = hit["thesis"]['id']
            request_url = base_url2 + str(ths_id) + "&fields=title|authors|supervisors"
            thesis_response = client.request(request_url, "POST")
            response = str(thesis_response[1])[2:-1]
            response_dict2 = json.loads(response)
            bot_message += response_dict2['title']
            bot_message += ' by '
            authors_text = ''
            for a in response_dict2['authors']:
                authors_text += a['first_name'] + ' ' + a['last_name'] + ' '
            if authors_text == '':
                authors_text = 'unknown author '
            bot_message += authors_text
            bot_message += 'subervised by '
            supervisors_text = ''
            for a in response_dict2['supervisors']:
                supervisors_text += a['first_name'] + ' ' + a['last_name'] + ' '
            if supervisors_text == '':
                supervisors_text = 'unknown supervisors '
            bot_message += supervisors_text
            bot_message += '\n'
        bot_message += "I hope this answer satisfies you."

        dispatcher.utter_message(text=str(bot_message))

        return [SlotSet("usos_thesis_name", None)]
