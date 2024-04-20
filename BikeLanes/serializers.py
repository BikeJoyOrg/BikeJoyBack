from rest_framework import serializers
from .models import BikeLane, LatLng

class LatLngSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatLng
        fields = ['id', 'latitude', 'longitude']

class BikeLaneSerializer(serializers.ModelSerializer):
    lat_lngs = LatLngSerializer(many=True, read_only=True)

    class Meta:
        model = BikeLane
        fields = ['id', 'lat_lngs']