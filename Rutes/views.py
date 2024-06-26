import logging
import math

from django.db import transaction
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg


from Rutes.models import Rutes, Punts, PuntsIntermedis, Valoracio, Comentario, RutesCompletades, PuntsVisitats
from Rutes.serializers import RutesSerializer, PuntsSerializer, PuntsIntermedisSerializer, \
    CompletedRoutesSerializer, ComentarioSerializer, RouteSerializer
from Users.models import CustomUser

logger = logging.getLogger(__name__)


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
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


# Create your views here.
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rutesApi(request):
    if request.method == 'GET':
        distance_param = request.GET.get('distance')
        duration_param = request.GET.get('duration')
        nombreZona = request.GET.get('nombreZona')
        query = request.GET.get('query')
        radio = 2

        try:
            distance = float(distance_param) if distance_param is not None else None
        except ValueError:
            logging.error(f"Invalid distance value: {distance_param}")
            return JsonResponse({"error": "Invalid distance value."}, status=400)

        try:
            duration = int(duration_param) if duration_param is not None else None
        except ValueError:
            logging.error(f"Invalid duration value: {duration_param}")
            return JsonResponse({"error": "Invalid duration value."}, status=400)

        rutes = Rutes.objects.annotate(rating_avg=Avg('valoracio__mark'))

        if query:
            rutes = rutes.filter(Q(RuteName__icontains=query) | Q(RuteDescription__icontains=query))
        else:
            if duration is not None and duration != 0 and duration != 6:
                rutes = rutes.filter(RuteTime__lte=duration * 60)

            if distance is not None and distance != 0 and distance != 10:
                rutes = rutes.filter(RuteDistance__lte=distance * 1000)

            if nombreZona:
                zona_coords = get_coords_for_zona(nombreZona)
                if zona_coords:
                    filtered_rutes = []
                    for rute in rutes:
                        distance_to_zona = haversine(zona_coords[1], zona_coords[0], rute.PuntIniciLong,
                                                     rute.PuntIniciLat)
                        if distance_to_zona <= radio:
                            filtered_rutes.append(rute)
                    rutes = filtered_rutes


        rutes_with_ratings = rutes.filter(rating_avg__isnull=False).order_by('-rating_avg')
        rutes_without_ratings = rutes.filter(rating_avg__isnull=True)
        all_rutes = list(rutes_with_ratings) + list(rutes_without_ratings)
        rutes_serializer = RutesSerializer(all_rutes, many=True)
        return JsonResponse(rutes_serializer.data, safe=False)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def afegirRuta(request):
    user = request.user
    data = JSONParser().parse(request)
    data['creador'] = user.pk
    rutes_serializer = RutesSerializer(data=data)
    if rutes_serializer.is_valid():
        rutes_serializer.save()
        return JsonResponse(rutes_serializer.data, status=201)
    return JsonResponse("Error al guardar ruta", safe=False, status=400)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def rank_route(request, rute_id):
    user = request.user
    try:
        rute = Rutes.objects.get(RuteId=rute_id)
        mark = request.data.get('mark')
        if mark is None or mark < 1 or mark > 5:
            return Response({'error': 'Invalid mark'}, status=400)

        valoracio = Valoracio.objects.filter(ruta=rute, user=user).first()
        if valoracio:
            valoracio.mark = mark
            valoracio.save()
        else:
            valoracio = Valoracio(ruta=rute, user=user, mark=mark)
            valoracio.save()

        return Response(status=200)
    except ObjectDoesNotExist:
        return Response({'error': 'Route not found'}, status=404)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_route(request, rute_id):
    user = request.user
    try:
        rute = Rutes.objects.get(RuteId=rute_id)
        text = request.data.get('text')
        if text == "" or text is None:
            return Response({'error': 'Invalid text'}, status=400)

        comentario = Comentario(ruta=rute, user=user, text=text)
        comentario.save()

        return Response(status=200)
    except ObjectDoesNotExist:
        return Response({'error': 'Route not found'}, status=404)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def completed_routes_view(request):
    completed_routes = RutesCompletades.objects.filter(user=request.user)
    serializer = CompletedRoutesSerializer(completed_routes, many=True, context={'request': request})
    return Response(serializer.data)



@api_view(['GET'])
def average_rating(request, rute_id):
    try:
        rute = Rutes.objects.get(pk=rute_id)
        average = Valoracio.objects.filter(ruta=rute).aggregate(Avg('mark'))['mark__avg']
        if average is not None:
            if average - int(average) >= 0.5:
                rounded_average = math.ceil(average)
            else:
                rounded_average = int(average)
        else:
            rounded_average = 0
        return Response(rounded_average)
    except Rutes.DoesNotExist:
        return Response({'error': 'Route not found'}, status=404)


@api_view(['GET'])
def get_route_comments(request, rute_id):
    try:
        rute = Rutes.objects.get(RuteId=rute_id)
        comments = Comentario.objects.filter(ruta=rute)
        serializer = ComentarioSerializer(comments, many=True)
        return Response(serializer.data)
    except Rutes.DoesNotExist:
        return Response({'error': 'Route not found'}, status=404)


def punts_intermedis_list(request, rute_id):
    if request.method == 'GET':
        punts_intermedis = PuntsIntermedis.objects.filter(RuteId=rute_id).select_related('PuntId').order_by('PuntOrder')
        route_coords = [{'lat': pi.PuntId.PuntLat, 'lng': pi.PuntId.PuntLong} for pi in punts_intermedis]
        return JsonResponse(route_coords, safe=False)


@csrf_exempt
def AfegirPuntRuta(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                request_data = JSONParser().parse(request)
                logger.info(f"Request data: {request_data}")
                ruta = Rutes.objects.get(RuteId=request_data['RuteId'])
                punt, created = Punts.objects.get_or_create(
                    PuntLat=request_data['PuntLat'],
                    PuntLong=request_data['PuntLong'],
                    defaults={
                        'PuntName': request_data['PuntName'],
                    }
                )

                # Crear o actualizar el punto intermedio
                punt_inter, created_inter = PuntsIntermedis.objects.get_or_create(
                    PuntId=punt,
                    RuteId=ruta,
                    PuntOrder=request_data['PuntOrder'],
                    defaults={
                        'PuntOrder': request_data['PuntOrder'],
                    }
                )

                # Si se creó el punto intermedio correctamente, retornar un mensaje adecuado
                if created_inter:
                    response_data = {'message': 'Punto intermedio creado correctamente'}
                else:
                    response_data = {'message': 'Punto intermedio actualizado correctamente'}

            return JsonResponse(response_data, status=200)
        except Exception as e:
            # En caso de error, imprimirlo y devolver un mensaje de error
            print(f"Error al crear/actualizar punt ruta: ")
            response_data = {'message': 'Error al procesar la solicitud' + str(e)}
            return JsonResponse(response_data, status=500)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ruta_completada(request, rute_id):
    try:
        user = request.user
        request_data = JSONParser().parse(request)
        ruta = Rutes.objects.get(RuteId=rute_id)
        ruta_completada, created = RutesCompletades.objects.get_or_create(
            ruta=ruta,
            user=user,
            defaults={
                'temps': request_data['temps'],
            }
        )
        if created:
            user.completed_routes += 1
            user.monthlyCompletedRoutes += 1
            user.weeklyCompletedRoutes += 1
            user.dailyCompletedRoutes += 1
            user.save()
            response_data = {'message': 'Ruta completada guardada correctamente'}
            return Response(response_data, status=201)
        else:
            response_data = {'message': 'Ruta completada actualizada correctamente'}
            return Response(response_data, status=200)
    except Exception as e:
        return Response(f"Error al guardar ruta completada", status=400)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_punts_visitats(request):
    try:
        user = request.user
        request_data = JSONParser().parse(request)
        punt, created = Punts.objects.update_or_create(
            PuntLat=request_data['PuntLat'],
            PuntLong=request_data['PuntLong'],
            defaults={
                'PuntName': request_data['PuntName'],
            }
        )
        punt_visitat, created_visitat = PuntsVisitats.objects.get_or_create(
            punt=punt,
            user=user,
        )

        # Si se creó el punto intermedio correctamente, retornar un mensaje adecuado
        if created_visitat:
            response_data = {'message': 'Punto visitado creado correctamente'}
        else:
            response_data = {'message': 'Punto visitado actualizado correctament'}

        return Response(response_data, status=200)
    except Exception as e:
        # En caso de error, imprimirlo y devolver un mensaje de error
        print(f"Error al crear/actualizar punt ruta: ")
        response_data = {'message': 'Error al procesar la solicitud' + str(e)}
        return Response(response_data, status=500)

@api_view(["GET"])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def punts_visitats(request):
    if request.method == 'GET':
        user = request.user
        punts_visitats = PuntsVisitats.objects.filter(user=user)
        punts_visitats = Punts.objects.filter(puntsvisitats__in=punts_visitats)
        punts_visitats = PuntsSerializer(punts_visitats, many=True)
        return JsonResponse(punts_visitats.data, safe=False)

#Vista servicio API
@api_view(['GET'])
def get_routes(request):
    routes = Rutes.objects.all()
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)


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
