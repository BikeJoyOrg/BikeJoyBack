from rest_framework import serializers

from Rutes.models import Rutes, Punts, PuntsIntermedis


class RutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutes
        fields = ('RuteId',
                  'RuteName',
                  'RuteDistance',
                  'RuteTime',
                  'RuteRating')


class PuntsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punts
        fields = ('PuntId',
                  'PuntName',
                  'PuntLat',
                  'PuntLong')


class PuntsIntermedisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntsIntermedis
        fields = ('PuntInterId',
                  'PuntOrder',
                  'RuteId',
                  'PuntId')
