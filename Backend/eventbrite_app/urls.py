from django.urls import path
from .views import (
    create_event,
    get_event_details,
    update_event,
    cancel_event,
    delete_event,
)
from . import views

urlpatterns = [
    path("api/create/", create_event, name="create-event"),
    path("api/<str:event_id>/", get_event_details, name="get-event-details"),
    path("api/<str:event_id>/update/", update_event, name="update-event"),
    path("api/<str:event_id>/cancel/", cancel_event, name="cancel-event"),
    path("api/<str:event_id>/delete/", delete_event, name="delete-event"),
    path("oauth/redirect/", views.oauth_redirect, name="oauth-redirect"),
]
