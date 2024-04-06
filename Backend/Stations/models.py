from datetime import datetime

from django.db import models

from Rutes.models import Punts


# Create your models here.
class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    PuntId = models.ForeignKey(Punts, on_delete=models.CASCADE, default=0)
    mechanical = models.IntegerField(default=0)
    ebike = models.IntegerField(default=0)
    num_docks_available = models.IntegerField(default=0)

    def __str__(self):
        return f"Station: {self.station_id}"
