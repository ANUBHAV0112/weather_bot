from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker # type: ignore
from rasa_sdk.executor import CollectingDispatcher # type: ignore
import requests

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        api_key = "e0967dcaa9d514d9fd13a4d2fdcf520e"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        # Default fallback location
        location = tracker.get_slot("location") or "Himachal Pradesh"


        # Extract location entity
        for entity in tracker.latest_message.get("entities", []):
            if entity["entity"] == "location":
                location = entity["value"]

        # Prepare API request
        complete_url = f"{base_url}appid={api_key}&q={location}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            temperature = main["temp"]
            weather_desc = data["weather"][0]["description"]

            # 🔍 Smart snow response
            if "snow" in weather_desc.lower():
                reply = f"Yes, it looks like it will snow in {location}."
            else:
                reply = f"No, it's currently {weather_desc} in {location}. Temperature is {temperature}°C."
        else:
            reply = "I couldn't find the weather for that location. Can you try another city?"

        dispatcher.utter_message(text=reply)
        return []
