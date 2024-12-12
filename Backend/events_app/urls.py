from django.urls import path
from .views import (
    eventListView,
    eventDetailView,
    RSVPView,
    EventbriteSearchView,
    EventbriteDetailView,
)

urlpatterns = [
    path(
        "", eventListView.as_view(), name="event-list"
    ),  # Lists and creates the events
    path(
        "<int:pk>/", eventDetailView.as_view(), name="event-detail"
    ),  # Retrieves, updates, and deletes events
    path("<int:event_id>/rsvp/", RSVPView.as_view(), name="rsvp"),  # RSVP to an event
    path(
        "eventbrite/search/", EventbriteSearchView.as_view(), name="eventbrite-search"
    ),
    path(
        "eventbrite/<str:event_id>/",
        EventbriteDetailView.as_view(),
        name="eventbrite-detail",
    ),
]
