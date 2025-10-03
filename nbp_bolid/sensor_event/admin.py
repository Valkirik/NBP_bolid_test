from django.contrib import admin

from .models import Event, Sensor

admin.site.register(Sensor)
admin.site.register(Event)
