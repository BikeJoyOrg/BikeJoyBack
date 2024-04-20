from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2


from Rutes.models import Rutes, Punts, PuntsIntermedis
from Rutes.serializers import RutesSerializer, PuntsSerializer, PuntsIntermedisSerializer


def get_coords_for_zona(nombreZona):
    zonas_coords = {
        "Barri Gotic": (41.3834, 2.1761),
        "El Poble Sec": (41.3723, 2.1699),
        "El Born": (41.3845, 2.1821),
        "El Clot": (41.4110, 2.1916),
        "El Poblenou": (41.3995, 2.2040),
        "El Putxet": (41.4054, 2.1345),
        "El Raval": (41.3795, 2.1684),
        "El Tibidabo": (41.4218, 2.1187),
        "El Vall d'Hebron": (41.4269, 2.1486),
        "Horta": (41.4285, 2.1456),
        "La Barceloneta": (41.3809, 2.1895),
        "La Sagrada Familia": (41.4036, 2.1744),
        "Les Corts": (41.3833, 2.1167),
        "Sant Andreu": (41.4354, 2.1899),
        "Sant Antoni": (41.3793, 2.1541),
        "Sant Gervasi": (41.4016, 2.1521),
        "Sant Marti": (41.4056, 2.1915),
        "Sants": (41.3781, 2.1319),
        "Sarria": (41.3993, 2.1213),
        "Cualquier zona": None,
    }

    return zonas_coords.get(nombreZona)

def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Create your views here.
@csrf_exempt
def rutesApi(request):
    if request.method == 'GET':
        distance = request.GET.get('distance')
        duration = request.GET.get('duration')
        nombreZona = request.GET.get('nombreZona')
        query = request.GET.get('query')
        radio = 2

        rutes = Rutes.objects.all()
        if query:
            rutes = rutes.filter(Q(RuteName__icontains=query) | Q(RuteDescription__icontains=query))
        else:
            if duration is not None and duration != 0:
                rutes = rutes.filter(RuteTime__lte=duration)

            if distance is not None and distance != 0:
                rutes = rutes.filter(RuteDistance__lte=distance)

            if nombreZona:
                zona_coords = get_coords_for_zona(nombreZona)
                if zona_coords:
                    filtered_rutes = []
                    for rute in rutes:
                        distance_to_zona = haversine(zona_coords[1], zona_coords[0], rute.PuntIniciLong, rute.PuntIniciLat)
                        if distance_to_zona <= radio:
                            filtered_rutes.append(rute)
                    rutes = filtered_rutes

        rutes_serializer = RutesSerializer(rutes, many=True)
        return JsonResponse(rutes_serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        rutes_serializer = RutesSerializer(data=data)
        if rutes_serializer.is_valid():
            rutes_serializer.save()
            return JsonResponse(rutes_serializer.data, status=201)
        return JsonResponse("Error al guardar ruta", safe=False)


def punts_intermedis_list(request, rute_id):
    if request.method == 'GET':
        punts_intermedis = PuntsIntermedis.objects.filter(RuteId=rute_id).select_related('PuntId').order_by('PuntOrder')
        route_coords = [{'lat': pi.PuntId.PuntLat, 'lng': pi.PuntId.PuntLong} for pi in punts_intermedis]
        return JsonResponse(route_coords, safe=False)


@csrf_exempt
def AfegirPuntRuta(request):
    if request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            ruta = Rutes.objects.get(RuteId=request_data['RuteId'])
            punt, created = Punts.objects.get_or_create(
                PuntName=request_data['PuntName'],
                defaults={
                    'PuntLat': request_data['PuntLat'],
                    'PuntLong': request_data['PuntLong']
                }
            )
            station, created = PuntsIntermedis.objects.get_or_create(
                defaults={
                    'PuntId': punt,
                    'RuteId': ruta,
                    'PuntOrder': request_data['PuntOrder'],
                }
            )
            if created:
                response_data = {'message': 'Ruta creada correctamente'}
            else:
                response_data = {'message': 'ruta actualizada correctamente'}
            return JsonResponse(response_data, status=200)
        except Exception as e:
            # En caso de error, imprimirlo y devolver un mensaje de error
            print(f"Error al crear/actualizar la estación: {e}")
            response_data = {'message': 'Error al procesar la solicitud'}
            return JsonResponse(response_data, status=500)

    else:
        return JsonResponse({'message': 'Método HTTP no permitido'}, status=405)





"""
@csrf_exempt
def puntsApi(request):
    if request.method == 'GET':
        punts = Rutes.objects.all()
        punts_serializer = PuntsSerializer(punts, many=True)
        return JsonResponse(punts_serializer.data, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        punts_serializer = PuntsSerializer(data=data)
        print(punts_serializer.is_valid())
        if punts_serializer.is_valid():
            punts_serializer.save()
            return JsonResponse(punts_serializer.data, status=201)
        return JsonResponse("Error al guardar punt", safe=False)
@csrf_exempt
def puntsIntermedisApi(request):
    if request.method == 'GET':
        puntsIntermedis = Rutes.objects.all()
        puntsIntermedis_serializer = PuntsIntermedisSerializer(puntsIntermedis, many=True)
        return JsonResponse(puntsIntermedis_serializer.data, safe=False)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        puntsIntermedis_serializer = PuntsIntermedisSerializer(data=data)
        if puntsIntermedis_serializer.is_valid():
            puntsIntermedis_serializer.save()
            return JsonResponse(puntsIntermedis_serializer.data, status=201)
        return JsonResponse("Error al guardar punt intermig", safe=False)
"""
