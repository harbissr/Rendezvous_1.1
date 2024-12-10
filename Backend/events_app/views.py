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
)


# Create your views here.
class eventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
