from rest_framework import serializers

from Rutes.models import Rutes, Punts, PuntsIntermedis, RutesCompletades, Valoracio, Comentario


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
                    'PuntIniciLong',)

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
