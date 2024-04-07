from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from Rutes.models import Rutes, Punts, PuntsIntermedis
from Rutes.serializers import RutesSerializer, PuntsSerializer, PuntsIntermedisSerializer


# Create your views here.
@csrf_exempt
def rutesApi(request):
    if request.method == 'GET':
        rutes = Rutes.objects.all()
        rutes_serializer = RutesSerializer(rutes, many=True)
        return JsonResponse(rutes_serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        rutes_serializer = RutesSerializer(data=data)
        if rutes_serializer.is_valid():
            rutes_serializer.save()
            return JsonResponse(rutes_serializer.data, status=201)
        return JsonResponse("Error al guardar ruta", safe=False)


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
            print(f"Error al crear/actualizar punt ruta: {e}")
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
