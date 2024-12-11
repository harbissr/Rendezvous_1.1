from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, RSVP
from .serializers import EventSerializer, RSVPSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


# Create your views here.
class eventListView(APIView):
    def get(self, request):
        """This will get a list of events"""
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """This will post a new event"""
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class eventDetailView(APIView):
    def get_object(self, pk):  # pk = Django syntax for "primary key"
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def get(self, request, pk):
        """Allows to search an event by the pk"""
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        """Allows for an event to be updated"""
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        """Allows for an event to be deleted"""
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RSVPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        """RSVP to an event"""
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )
        user = request.user
        """Check if the user has already RSVP'd to an event"""
        existing_rsvp = RSVP.objects.filter(user=user, event=event).first()
        if existing_rsvp:
            return Response(
                {"detail": "You've already RSVP'd to this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        """Create a new RSVP"""
        RSVP.objects.create(user=user, event=event, is_attending=True)
        return Response(
            {"detail": "You've successfully RSVP'd to this event."},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, event_id):
        """Cancel an RSVP to an event"""
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"detail": "This event does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        user = request.user
        """Checks if the user even RSVP'd to the event before canceling"""
        existing_rsvp = RSVP.objects.filter(user=user, event=event).first()
        if not existing_rsvp:
            return Response(
                {"detail": "You haven't RSVP'd to this event."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        """Delete an RSVP"""
        existing_rsvp.delete()
        return Response(
            {"detail": "RSVP has been successfully cancelled."},
            status=status.HTTP_204_NO_CONTENT,
        )
