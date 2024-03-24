from datetime import datetime

from django.db import models


# Create your models here.

class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    address = models.CharField(max_length=100)
    last_updated = models.IntegerField(default=0)
    mechanical = models.IntegerField(default=0)
    ebike = models.IntegerField(default=0)
    num_docks_available = models.IntegerField(default=0)

    def __str__(self):
        return f"Station: {self.name}, Last Updated: {self.last_updated}"

