from django.db import models


class TemperatureReading(models.Model):
    tempC = models.FloatField()
    tempF = models.FloatField()
    creation_date = models.DateTimeField(auto_now=True)



