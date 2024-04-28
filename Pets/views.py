import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from Pets.models import Mascota
from Pets.models import MascotaAconseguida
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import traceback

from Pets.serializers import MascotaSerializer, MascotaAconseguidaSerializer


# Create your views here.


@api_view(['GET'])
def get_mascota(request, name):
    pets = Mascota.objects.get(name=name)
    serializer = MascotaSerializer(pets, many=False)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_mascotas(request):
    pets = Mascota.objects.all()
    serializer = MascotaSerializer(pets, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def get_mascotas_aconseguides_usuari(request):
    try:
        pets = MascotaAconseguida.objects.filter(nicknameUsuari=request.user)
        serializer = MascotaAconseguidaSerializer(pets, many=True)
        return JsonResponse(serializer.data, status=200)

    except Exception as e:
            print(f"Error al obtener información de mascotas aconseguides: {e}")
            return JsonResponse({'message': 'Error al obtener información de mascotas aconseguides'}, status=500)

@api_view(['PATCH'])
def equipar_mascota(request, name):
    if request.user.is_authenticated:
        try:
            # Obtén todas las MascotaAconseguida del mismo nicknameUsuari y establece equipada a False
            MascotaAconseguida.objects.filter(nicknameUsuari=request.user).update(equipada=False)

            # Obtén la MascotaAconseguida específica y establece equipada a True
            mascota = Mascota.objects.get(name=name)
            mascotaA = MascotaAconseguida.objects.get(nicknameUsuari=request.user, nomMascota=mascota)
            mascotaA.equipada = True
            mascotaA.save()

            return JsonResponse({'message': 'Mascota equipada correctamente'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'Error al equipar mascota: {e}'}, status=500)
    else:
        return Response({'error': 'User not authenticated'}, status=401)


@api_view(['POST'])
def create_mascota_aconseguida(request, name):
    if request.user.is_authenticated:
        try:
            pet = Mascota.objects.get(name=name)

            mascota_aconseguida = MascotaAconseguida(nomMascota=pet, nicknameUsuari=request.user)
            mascota_aconseguida.save()

            return Response(status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'Mascota not found'}, status=404)
    else:
        return Response({'error': 'User not authenticated'}, status=401)