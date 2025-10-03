from django.urls import include, path
from rest_framework import routers

from .endpoints import (EventViewSet, HumidityOnlyFilterListAPIView,
                        SensorViewSet, TemperatureAndHumidityListAPIView,
                        TemperatureOnlyFilterListAPIView)

router = routers.SimpleRouter()
router.register("sensor_view", SensorViewSet, basename="sensor"),
router.register("event_view", EventViewSet, basename="event"),

urlpatterns = [
    path("", include(router.urls)),
    path(
        "only_temperature/",
        TemperatureOnlyFilterListAPIView.as_view(),
        name="events-only-temperature",
    ),
    path(
        "only_humidity/",
        HumidityOnlyFilterListAPIView.as_view(),
        name="events-only-humidity",
    ),
    path(
        "temperature_and_humidity/",
        TemperatureAndHumidityListAPIView.as_view(),
        name="both-humidity-temperature",
    ),
]
