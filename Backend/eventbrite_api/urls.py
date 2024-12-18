from django.urls import path
from .views import (
    create_event,
    get_event_details,
    update_event,
    cancel_event,
    delete_event,
)
from . import views

# CRUD
urlpatterns = [
    # Create -- Method:GET -- Creates a new event
    path("api/v1/create/", create_event, name="create-event"),
    # Read -- Method:GET -- Fetches details of an event identified by event_id
    path("api/v1/<str:event_id>/", get_event_details, name="get-event-details"),
    # Update -- Method:POST -- Updates an existing event with new data
    path("api/v1/<str:event_id>/update/", update_event, name="update-event"),
    path("api/v1/<str:event_id>/cancel/", cancel_event, name="cancel-event"),
    # Delete -- Method:DELETE -- Deletes the event permanently
    path("api/v1/<str:event_id>/delete/", delete_event, name="delete-event"),
    path("oauth/redirect/", views.oauth_redirect, name="oauth-redirect"),
]
