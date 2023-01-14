from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json
import requests
from datetime import date, datetime


class Action_USOS_API_term(Action):

    def name(self) -> Text:
        return "action_USOS_API_term"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_year = date.today().year
        current_year = str(current_year) + "L"
        base_url = f"https://apps.usos.pw.edu.pl/services/terms/term?term_id={current_year}"
        term_request = requests.post(base_url)
        term_request_dict = json.loads(term_request.text)
        term_start_date = datetime.strptime(term_request_dict["start_date"], '%Y-%m-%d')
        term_end_date = datetime.strptime(term_request_dict["end_date"], '%Y-%m-%d')
        is_before_start = term_start_date > datetime.today()
        is_after_finish = term_end_date < datetime.today()
        if is_before_start:
            current_year = str(date.today().year - 1) + "Z"
        elif is_after_finish:
            current_year = current_year[:-1] + "Z"
        base_url = f"https://apps.usos.pw.edu.pl/services/terms/term?term_id={current_year}"
        term_request = requests.post(base_url)
        term_request_dict = json.loads(term_request.text)
        term_start_date = datetime.strptime(term_request_dict["start_date"], '%Y-%m-%d').date()
        term_end_date = datetime.strptime(term_request_dict["end_date"], '%Y-%m-%d').date()
        response = f"Term id is {current_year}. It started on {term_start_date} and it ends on {term_end_date}."

        dispatcher.utter_message(text=str(response))

        return []
