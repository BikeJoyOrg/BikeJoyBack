from django.db import models


class LatLng(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


class BikeLanes(models.Model):
    id = models.TextField(primary_key=True)
    latLng = models.ManyToManyField(LatLng)
