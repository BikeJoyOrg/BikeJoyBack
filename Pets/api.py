from .models import Mascota, MascotaAconseguida
from rest_framework import viewsets, permissions
from .serializers import MascotaSerializer, MascotaAconseguidaSerializer


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MascotaSerializer

class MascotaAconseguidaViewSet(viewsets.ModelViewSet):
    queryset = MascotaAconseguida.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MascotaAconseguidaSerializer