from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Event, Sensor


class EventsApiTests(APITestCase):
    def setUp(self):
        self.sensor_1 = Sensor.objects.create(name="Sensor 1", type=1)
        self.sensor_2 = Sensor.objects.create(name="Sensor 2", type=2)
        self.sensor_3 = Sensor.objects.create(name="Sensor 3", type=3)

        Event.objects.create(
            sensor=self.sensor_3,
            temperature=3,
        )
        Event.objects.create(sensor=self.sensor_2, temperature=5, humidity=3)
        Event.objects.create(sensor=self.sensor_1, humidity=8)
        Event.objects.create(sensor=self.sensor_1, temperature=3, humidity=1)
        Event.objects.create(sensor=self.sensor_1, humidity=4)

    def test_getting_all(self):
        url = reverse("event-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.data, dict)
        self.assertEqual(len(resp.data["results"]), 5)

    def test_certain_sensor_events(self):
        url = reverse("sensor-events", kwargs={"pk": self.sensor_1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.data, list)
        self.assertEqual(len(resp.data), 3)

    def test_getting_only_temperature(self):
        url = reverse("events-only-temperature")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        objct = resp.data["results"][0]
        self.assertIsNotNone(objct["temperature"])
        self.assertIsNone(objct["humidity"])
        result = resp.data["results"]
        self.assertEqual(len(result), 1)

    def test_getting_only_humidity(self):
        url = reverse("events-only-humidity")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        objct = resp.data["results"][0]
        self.assertIsNone(objct["temperature"])
        self.assertIsNotNone(objct["humidity"])
        result = resp.data["results"]
        self.assertEqual(len(result), 2)

    def test_getting_both(self):
        url = reverse("both-humidity-temperature")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        objct = resp.data["results"][0]
        self.assertIsNotNone(objct["temperature"])
        self.assertIsNotNone(objct["humidity"])
        result = resp.data["results"]
        self.assertEqual(len(result), 2)
