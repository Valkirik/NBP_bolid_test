from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Sensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)