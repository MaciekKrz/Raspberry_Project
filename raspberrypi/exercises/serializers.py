from .models import TemperatureReading
from rest_framework import serializers


class TempSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TemperatureReading
        fields = ("id", "tempC", "tempF", "creation_date")

