import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, authentication_classes



from Pets.models import Mascota
from Pets.models import MascotaAconseguida
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_mascotas_aconseguides_usuari(request):
    user = request.user
    try:
        pets = MascotaAconseguida.objects.filter(nicknameUsuari=user)
        serializer = MascotaAconseguidaSerializer(pets, many=True)
        return JsonResponse(serializer.data, safe = False ,status=200)

    except Exception as e:
        print(f"Error al obtener información de mascotas aconseguides: {e}")
        return JsonResponse({'message': f'Error al obtener información de mascotas aconseguides: {str(e)}'}, status=500)

@api_view(['PATCH'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def equipar_mascota(request, name):
    user = request.user
    try:
        # Obtén todas las MascotaAconseguida del mismo nicknameUsuari y establece equipada a False
        MascotaAconseguida.objects.filter(nicknameUsuari=request.user).update(equipada=False)

        # Obtén la MascotaAconseguida específica y establece equipada a True
        mascota = Mascota.objects.get(name=name)
        mascotaA = MascotaAconseguida.objects.get(nicknameUsuari=user, nomMascota=mascota)
        mascotaA.equipada = True
        mascotaA.save()

        return JsonResponse({'message': 'Mascota equipada correctamente'}, status=200)

    except Exception as e:
        return JsonResponse({'message': f'Error al equipar mascota: {e}'}, status=500)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_mascota_aconseguida(request, name):
    user = request.user
    try:
        pet = Mascota.objects.get(name=name)
        mascota_aconseguida = MascotaAconseguida(nomMascota=pet, nicknameUsuari=user)
        mascota_aconseguida.save()

        return Response(status=200)
    except ObjectDoesNotExist:
        return Response({'error': 'Mascota not found'}, status=404)

@api_view(['PATCH'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def lvlUp(request, name):
    user = request.user
    try:
        mascota = Mascota.objects.get(name=name)
        mascota_aconseguida = MascotaAconseguida.objects.get(nomMascota=mascota, nicknameUsuari=user)
        if(mascota_aconseguida.nivell < 3):
            mascota_aconseguida.nivell += 1
        else:
            return JsonResponse({'message': 'La mascota ya ha alcanzado el nivel máximo'}, status=400)
        mascota_aconseguida.save()

        return JsonResponse({'message': 'Mascota nivelada correctamente'}, status=200)
    except Exception as e:
        return JsonResponse({'message': f'Error al subir de nivel la mascota: {e}'}, status=500)