import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from models import Mascota
from models import MascotaAconseguida
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import traceback

# Create your views here.
@require_http_methods(["GET"])
def get_mascota(request, name):
    try:
        mascota = (Mascota.objects.filter(name=name)
                   .values('name', 'img1', 'img1l', 'img2', 'img2l', 'img3', 'img3l', 'bonus').first())

        if mascota:
            return JsonResponse({'state': mascota}, status=200)
        else:
            return JsonResponse({'message': 'Mascota no encontrada'}, status=404)

    except Exception as e:
        return JsonResponse({'message': f'Error al obtener información de la mascota: {e}'}, status=500)

@require_http_methods(["GET"])
def get_mascotas(request):
    try:
        pets = Mascota.objects.all()
        pet_data = [{
            'name': pet.name,
            'img1': pet.img1,
            'img1l': pet.img1l,
            'img2': pet.img2,
            'img2l': pet.img2l,
            'img3': pet.img3,
            'img3l': pet.img3l,
            'bonus': pet.bonus
        } for pet in pets]

        return JsonResponse({'mascotes': pet_data}, status=200)

    except Exception as e:
            print(f"Error al obtener información de mascotas: {e}")
            return JsonResponse({'message': 'Error al obtener información de mascotas'}, status=500)


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