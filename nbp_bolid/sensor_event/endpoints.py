from django.contrib.admin import action
from django.core.serializers import serialize

from .models import Sensor, Event
from .serializers import SensorSerializer, EventSerializer
from rest_framework import permissions, viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response

# CRUD
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["get"])
    def events(self, request, pk=None):
        sensor = self.get_object()
        events = Event.objects.filter(sensor=sensor)
        serializer= EventSerializer(events, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


# FILTERS
class TemperatureOnlyFilterListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(temperature__isnull=False, humidity__isnull=True)


class HumidityOnlyFilterListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(temperature__isnull=True, humidity__isnull=False)


class TemperatureAndHumidityListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    def get_queryset(self):
        return Event.objects.filter(temperature__isnull=False, humidity__isnull=False)