from rest_framework.serializers import ModelSerializer

from .models import Event, Sensor


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
