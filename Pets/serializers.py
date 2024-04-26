from rest_framework import serializers
from .models import Mascota, MascotaAconseguida

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

class MascotaAconseguidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MascotaAconseguida
        fields = '__all__'

