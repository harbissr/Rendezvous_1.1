import requests
from django.conf import settings

BASE_URL = "https://www.eventbriteapi.com/v3"


class EventbriteAPI:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.EVENTBRITE_API_KEY}",
        }

    def search_event(self, query, location):
        url = f"{BASE_URL}/events/search/"
        params = {
            "q": query,
            "location.address": location,
        }
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def get_event_details(self, event_id):
        url = f"{BASE_URL}/events/{event_id}/"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        """Handle API response"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error_message = response.json().get("error description", "Unknown error")
            raise Exception(
                f"API error {response.status_code}: {error_message}"
            ) from http_err
