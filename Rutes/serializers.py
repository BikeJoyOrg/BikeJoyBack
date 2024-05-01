from rest_framework import serializers

from Rutes.models import Rutes, Punts, PuntsIntermedis, RutesCompletades, Valoracio, Comentario, PuntsVisitats


class RutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutes
        fields = ('RuteId',
                  'RuteName',
                  'RuteDescription',
                  'RuteDistance',
                  'RuteTime',
                  'RuteRating',
                    'PuntIniciLat',
                    'PuntIniciLong',
                    'creador')

class CompletedRoutesSerializer(serializers.ModelSerializer):
    rated = serializers.SerializerMethodField()

    class Meta:
        model = RutesCompletades
        fields = ['ruta_id', 'rated']

    def get_rated(self, obj):
        user = self.context['request'].user
        return Valoracio.objects.filter(ruta=obj.ruta, user=user).exists()

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

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

#Serializador servicio API
class RouteSerializer(serializers.ModelSerializer):
    distance_km = serializers.SerializerMethodField()
    PuntFinalLat = serializers.SerializerMethodField()
    PuntFinalLong = serializers.SerializerMethodField()
    class Meta:
        model = Rutes
        fields = ['RuteId', 'RuteName', 'distance_km', 'PuntIniciLat', 'PuntIniciLong', 'PuntFinalLat',
                  'PuntFinalLong']
    def get_distance_km(self, obj):
        return obj.RuteDistance / 1000
    def get_PuntFinalLat(self, obj):
        # Lógica para obtener la latitud del punto final
        punts_intermedis = PuntsIntermedis.objects.filter(RuteId=obj).order_by('PuntOrder')
        if punts_intermedis.exists():
            return punts_intermedis.last().PuntId.PuntLat
        return None
    def get_PuntFinalLong(self, obj):
        # Lógica para obtener la longitud del punto final
        punts_intermedis = PuntsIntermedis.objects.filter(RuteId=obj).order_by('PuntOrder')
        if punts_intermedis.exists():
            return punts_intermedis.last().PuntId.PuntLong
        return None
