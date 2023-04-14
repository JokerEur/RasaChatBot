from typing import Any, Text, Dict, List

from translate import Translator
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import emoji


class ActionTranslateToLang(Action):

    def name(self) -> Text:
        return "action_translate_to_lang"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        translate_text=next(tracker.get_latest_entity_values("translate_text"),None)

        target_language=next(tracker.get_latest_entity_values("target_language"),None)

        if not translate_text:
            msg=f"Specify text that I should translate"
            dispatcher.utter_message(text=msg)
            translate_text=next(tracker.get_latest_entity_values("translate_text"), None)
            return[]

        if not target_language:
            msg=f"Specify the language I should translate into"
            dispatcher.utter_message(text=msg)
            target_language=next(tracker.get_latest_entity_values("target_language"), None)
            return []
        
        translator=Translator(from_lang="english", to_lang=target_language)

        translation=translator.translate(translate_text)
        msg=f"Here is yours translation: {translation}"
        dispatcher.utter_message(text=msg)
        return[]
