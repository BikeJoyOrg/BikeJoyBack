from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Stations.models import Station


# Create your views here.

@api_view(["GET"])
def get_info_stations(request):
    try:
        stations = Station.objects.select_related('PuntId').all()
        station_data = [{
            'station_id': station.station_id,
            'address': station.PuntId.PuntName,
            'lat': station.PuntId.PuntLat,
            'lon': station.PuntId.PuntLong
        } for station in stations]
        return Response({'stations': station_data}, status=200)

    except Exception as e:
        print(f"Error al obtener información de estaciones: {e}")
        return Response({'message': 'Error al obtener información de estaciones'}, status=500)


@api_view(["GET"])
def get_state_stations(request, station_id):
    try:
        station = (Station.objects.filter(station_id=station_id)
                   .values('station_id', 'mechanical', 'ebike', 'num_docks_available').first())

        if station:
            return Response({'state': station}, status=200)
        else:
            return Response({'message': 'Estación no encontrada'}, status=404)

    except Exception as e:
        return Response({'message': f'Error al obtener información del estado de la estación: {e}'}, status=500)

