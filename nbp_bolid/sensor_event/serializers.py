from rest_framework.serializers import ModelSerializer

from .models import Sensor, Event

class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"