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

from Pets.serializers import MascotaSerializer


# Create your views here.


@api_view(['GET'])
def get_mascota(request, name):
    try:
        mascota = (Mascota.objects.filter(name=name))
        serializer = MascotaSerializer(mascota, many=False)

        if mascota:
            return Response({'state': serializer}, status=200)
        else:
            return Response({'message': 'Mascota no encontrada'}, status=404)

    except Exception as e:
        return Response({'message': f'Error al obtener información de la mascota: {e}'}, status=500)

@api_view(['GET'])
def get_mascotas(request):
    try:
        pets = Mascota.objects.all()
        serializer = MascotaSerializer(pets, many=True)

        return Response({'mascotes': serializer}, status=200)

    except Exception as e:
            print(f"Error al obtener información de mascotas: {e}")
            return Response({'message': 'Error al obtener información de mascotas'}, status=500)


@require_http_methods(["GET"])
def get_mascotas_aconseguides_usuari(request, nicknameUsuari):
    try:
        pets = MascotaAconseguida.objects.filter(nicknameUsuari=nicknameUsuari)
        pet_data = [{
            'nomMascota': pet.nomMascota.name,
            'nicknameUsuari': pet.nicknameUsuari,
            'nivell': pet.nivell,
            'equipada': pet.equipada
        } for pet in pets]

        return JsonResponse({'mascotes': pet_data}, status=200)

    except Exception as e:
            print(f"Error al obtener información de mascotas aconseguides: {e}")
            return JsonResponse({'message': 'Error al obtener información de mascotas aconseguides'}, status=500)
@csrf_exempt
@require_http_methods(["PATCH"])
def equipar_mascota(request, nicknameUsuari, name):
    try:
        # Obtén todas las MascotaAconseguida del mismo nicknameUsuari y establece equipada a False
        MascotaAconseguida.objects.filter(nicknameUsuari=nicknameUsuari).update(equipada=False)

        # Obtén la MascotaAconseguida específica y establece equipada a True
        mascota = Mascota.objects.get(name=name)
        mascotaA = MascotaAconseguida.objects.get(nicknameUsuari=nicknameUsuari, nomMascota=mascota)
        mascotaA.equipada = True
        mascotaA.save()

        return JsonResponse({'message': 'Mascota equipada correctamente'}, status=200)

    except Exception as e:
        return JsonResponse({'message': f'Error al equipar mascota: {e}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def create_mascota_aconseguida(request):
    try:
        data = json.loads(request.body)
        try:
            mascota = Mascota.objects.get(name=data['nomMascota'])
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'La mascota no existe'}, status=404)

        MascotaAconseguida.objects.create(
            nomMascota=mascota,
            nicknameUsuari=data['nicknameUsuari'],
            nivell=data['nivell'],
            equipada=data['equipada']
        )
        return JsonResponse({'message': 'Mascota conseguida creada correctamente'}, status=200)

    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({'message': f'Error al crear mascota conseguida: {e}'}, status=500)