from rest_framework import routers
from django.urls import include, path

from .endpoints import SensorViewSet, EventViewSet

router = routers.SimpleRouter()
router.register("sensor_viewset", SensorViewSet),
router.register("event_viewset", EventViewSet),

urlpatterns = [
    path("", include(router.urls)),
]