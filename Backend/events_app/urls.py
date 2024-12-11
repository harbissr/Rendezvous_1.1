from django.urls import path
from .views import eventListView, eventDetailView, RSVPView

urlpatterns = [
    path(
        "", eventListView.as_view(), name="event-list"
    ),  # Lists and creates the events
    path(
        "<int:pk>/", eventDetailView.as_view(), name="event-detail"
    ),  # Retrieves, updates, and deletes events
    path("<int:event_id>/rsvp/", RSVPView.as_view(), name="rsvp"),  # RSVP to an event
]
