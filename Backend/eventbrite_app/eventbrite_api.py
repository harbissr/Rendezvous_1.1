import requests
from django.conf import settings


class EventbriteAPI:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.EVENTBRITE_API_KEY}",
        }

    def create_event(self, organization_id):
        url = (
            f"https://www.eventbriteapi.com/v3/organizations/{organization_id}/events/"
        )
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_event_details(self, event_id):
        url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def update_an_event(self, event_id, event_data):
        url = (
            f"https://www.eventbriteapi.com/v3/events/{event_id}/"
            if event_id
            else f"https://www.eventbriteapi.com/v3/events/"
        )
        response = requests.post(url, headers=self.headers, json=event_data)
        return self._handle_response(response)

    def cancel_event(self, event_id):
        url = f"https://www.eventbriteapi.com/v3/events/{event_id}/cancel/"
        response = requests.post(url, headers=self.headers)
        return self._handle_response(response)

    def delete_event(self, event_id):
        url = f"https://www.eventbriteapi.com/v3/events/{event_id}/"
        response = requests.delete(url, headers=self.headers)
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
