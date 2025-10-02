from .models import Sensor, Event
from .serializers import SensorSerializer, EventSerializer
from rest_framework import permissions, viewsets, status
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

    # adding a new endpoint with a new url (thanks to @action)
    @action(detail=False, methods=["post"], url_path="import")
    def just_import(self, request):
        data = request.data
        # checking if our data is list (or not)
        if not isinstance(data, list):
            return Response({"detail": "It is expecting a JSON-file"},
                            status=status.HTTP_400_BAD_REQUEST)

        #creating a set with real sensors that there are in our data base
        valid_sensors = set(Sensor.objects.values_list("sensor_id", flat=True))

        # a function that normalise our values in our fields.
        # "" and "N/A" are read as None
        def norm(v):
            if v in ("", "N/A"):
                return None
            else:
                return v

        created_ids = []
        skipped = 0
        #normalise all fields
        for idx, item in enumerate(data):
            sensor_id = item.get("sensor_id")
            temperature = norm(item.get("temperature"))
            humidity = norm(item.get("humidity"))

            # we check if a sensor exists and if there are at least one value (temperature or humidity)
            if sensor_id not in valid_sensors:
                skipped += 1
                continue
            if temperature is None and humidity is None:
                skipped +=1
                continue

            # download and creat new events (that have passed)
            obj = Event.objects.create(
            sensor_id=sensor_id,
            temperature=temperature,
            humidity=humidity,
            )
            created_ids.append(obj.pk)

        status_code = 201 if created_ids else 400
        return Response({"created": len(created_ids), "skipped": skipped, "ids": created_ids}, status=status_code)



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