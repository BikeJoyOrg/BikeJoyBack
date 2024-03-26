from datetime import datetime

from django.contrib.sites import requests
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.utils import json

from Rutes.models import Punts
from Stations.models import Station


# Create your views here.

@csrf_exempt
def update_stations(request):
    if request.method == 'POST':
        url_state = 'https://65f1c39c034bdbecc763a229.mockapi.io/bikejoy/v1/stations'
        token = '0ca6976cb6d8ac8d0501763c3d03a6cb101f20074b49e2e7781583de19907a9f'
        headers = {
            'Authorization': token,
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url_state, headers=headers)
            response.raise_for_status()
            data = response.json()

            for station_data in data:
                station_id = station_data['station_id']
                station_instance = Station.objects.get(id=station_id)

                # Actualizar los parámetros de la estación
                station_instance.last_updated = datetime.now()
                station_instance.mechanical = station_data['numBicManuals']
                station_instance.ebike = station_data['numBicElectriques']
                station_instance.num_docks_available = station_data['numAnclatges']
                station_instance.save()

            response_data = {'message': 'Informacion de estaciones actualizada correctamente'}
            return JsonResponse(response_data, status=200)

        except requests.exceptions.RequestException as e:
            # Manejar cualquier error de solicitud HTTP
            print(f"Error al obtener información de estaciones: {e}")
            # Devolver un mensaje de error en caso de fallo
            response_data = {'message': 'Error al actualizar estaciones'}
            return JsonResponse(response_data, status=500)

    else:
        return JsonResponse({'message': 'Método HTTP no permitido'}, status=405)

@csrf_exempt
def charge_info_stations(request):
    if request.method == 'POST':
        # URL de la API de OpenData per obtenir dades
        # url_info = 'https://65f1c39c034bdbecc763a229.mockapi.io/bikejoy/v1/stations'
        # url_state = 'https://opendata-ajuntament.barcelona.cat/data/ca/dataset/estat-estacions-bicing'
        url_info = ('https://opendata-ajuntament.barcelona.cat/data/dataset/bd2462df-6e1e-4e37-8205-a4b8e7313b84/resource/f60e9291-5aaa-417d-9b91-612a9de800aa/download')

        token = 'aaa4a177d4280799dfc3f3098ad3a52145decf260487c898b60ed38dcc270dc0'

        headers = {'Authorization': token}

        try:
            response = requests.get(url_info, headers=headers)
            response.raise_for_status()
            data = response.json()

            for station_data in data:
                Station.objects.update_or_create(
                    station_id=station_data['station_id'],
                    defaults={
                        'name': station_data['name'],
                        'latitude': station_data['lat'],
                        'longitude': station_data['lon'],
                        'address': station_data['address'],
                        'last_update_date': station_data['last_updated'],
                        'mechanical': 0,
                        'ebike': 0,
                        'num_docks_available': 0,
                    }
                )

            # Crear una respuesta JSON con un mensaje de éxito
            response_data = {'message': 'Informacion de estaciones obtenida correctamente'}
            return JsonResponse(response_data, status=200)

        except requests.exceptions.RequestException as e:
            # Manejar cualquier error de solicitud HTTP
            print(f"Error al obtener información de estaciones: {e}")
            # Devolver un mensaje de error en caso de fallo
            response_data = {'message': 'Error al obtener información de estaciones'}
            return JsonResponse(response_data, status=500)

    else:
        return JsonResponse({'message': 'Método HTTP no permitido'}, status=405)

@csrf_exempt
def get_info_stations(request):
    if request.method == 'GET':
        try:
            stations = Station.objects.all()
            station_data = []
            for station in stations:
                station_info = {
                    'station_id': station.station_id,
                    'lat': float(str(station.PuntId.PuntLat)),
                    'lon': float(str(station.PuntId.PuntLong)),
                    'address': station.address,
                    'last_updated': station.last_updated,
                    'mechanical': station.mechanical,
                    'ebike': station.ebike,
                    'num_docks_available': station.num_docks_available
                }
                station_data.append(station_info)

            response_data = {'stations': station_data}
            return JsonResponse(response_data, status=200)

        except Exception as e:
            # Manejar cualquier error
            print(f"Error al obtener información de estaciones: {e}")
            response_data = {'message': 'Error al obtener información de estaciones'}
            return JsonResponse(response_data, status=500)

    else:
        return JsonResponse({'message': 'Método HTTP no permitido'}, status=405)

@csrf_exempt
def get_state_stations(request):
    if request.method == 'GET':
        try:
            stations = Station.objects.all()
            state_data = []
            for station in stations:
                station_info = {
                    'id': station.id,
                    'mechanical': station.mechanical,
                    'ebike': station.ebike,
                    'num_docks_available': station.num_docks_available
                }
                state_data.append(station_info)

            response_data = {'state': state_data}
            return JsonResponse(response_data, status=200)

        except Exception as e:
            print(f"Error al obtener informacion del estado de las estaciones: {e}")
            response_data = {'message': 'Error al obtener información del estado de las estaciones'}
            return JsonResponse(response_data, status=500)

    else:
        return JsonResponse({'message': 'Método HTTP no permitido'}, status=405)


@csrf_exempt
def create_station(request):
    if request.method == 'POST':
        try:
            # Convertir el cuerpo de la solicitud JSON en un diccionario Python
            request_data = JSONParser().parse(request)
            punt, created = Punts.objects.get_or_create(
                PuntName=request_data['address'],
                defaults={
                    'PuntLat': request_data['lat'],
                    'PuntLong': request_data['lon']
                }
            )

            # Crear o actualizar la estación con los datos proporcionados
            station, created = Station.objects.update_or_create(
                station_id=request_data['station_id'],
                defaults={
                    'PuntId': punt,
                    'address': request_data['address'],
                    'last_updated': request_data['last_updated'],
                    'mechanical': request_data['mechanical'],
                    'ebike': request_data['ebike'],
                    'num_docks_available': request_data['num_docks_available'],
                }
            )

            # Crear una respuesta JSON
            if created:
                response_data = {'message': 'Estación creada correctamente'}
            else:
                response_data = {'message': 'Estación actualizada correctamente'}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            # En caso de error, imprimirlo y devolver un mensaje de error
            print(f"Error al crear/actualizar la estación: {e}")
            response_data = {'message': 'Error al procesar la solicitud'}
            return JsonResponse(response_data, status=500)
    else:
        return JsonResponse({'message': 'Método HTTP no permitido'}, status=405)
