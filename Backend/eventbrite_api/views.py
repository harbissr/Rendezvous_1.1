import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .eventbrite_api import EventbriteAPI

eventbrite_api = EventbriteAPI()


@api_view(["POST"])
def create_event(request):
    oranization_id = request.data.get("organization_id")
    if not oranization_id:
        return Response({"error": "organization_id is required"}, status=400)

    try:
        data = eventbrite_api.create_event(oranization_id)
        return Response(data, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def get_event_details(request, event_id):
    try:
        data = eventbrite_api.get_event_details(event_id)
        return Response(data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def update_event(request, event_id):
    event_data = request.data.get("event")
    if not event_data:
        return Response({"error": "event data is required"}, status=400)
    try:
        data = eventbrite_api.update_an_event(event_id, event_data)
        return Response(data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def cancel_event(request, event_id):
    try:
        data = eventbrite_api.cancel_event(event_id)
        return Response(data, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["DELETE"])
def delete_event(request, event_id):
    try:
        data = eventbrite_api.delete_event(event_id)
        return Response(data, status=204)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def oauth_redirect(request):
    """
    Handle the redirect from Eventbrite and exchange the authorization code for an access token.
    """
    code = request.GET.get("code")  # Extract the authorization code
    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    # Exchange the authorization code for an access token
    token_url = "https://www.eventbrite.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.EVENTBRITE_API_KEY,
        "client_secret": settings.EVENTBRITE_CLIENT_SECRET,
        "redirect_uri": settings.EVENTBRITE_REDIRECT_URI,  # Must match the one registered
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return JsonResponse(response.json(), status=200)  # Return the access token
    else:
        return JsonResponse({"error": response.json()}, status=response.status_code)
