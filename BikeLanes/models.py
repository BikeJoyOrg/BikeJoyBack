from django.db import models


class BikeLane(models.Model):
    id = models.TextField(primary_key=True)


class LatLng(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    bike_lane = models.ForeignKey(BikeLane, related_name='lat_lngs', on_delete=models.CASCADE)
