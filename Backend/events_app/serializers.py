from rest_framework import serializers
from .models import Event, RSVP
from user_app.models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "description", "location", "event_date", "attendees"]


class RSVPSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = RSVP
        fields = ["id", "user", "event", "attending"]
