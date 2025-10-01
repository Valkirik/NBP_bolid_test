from .models import Sensor, Event
from .serializers import SensorSerializer, EventSerializer
from rest_framework import permissions, viewsets
from rest_framework import generics

# CRUD
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.AllowAny]


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