from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from Stations.models import Station


# Create your views here.

@require_http_methods(["GET"])
def get_info_stations(request):
    try:
        stations = Station.objects.select_related('PuntId').all()
        station_data = [{
            'station_id': station.station_id,
            'address': station.PuntId.PuntName,
            'lat': station.PuntId.PuntLat,
            'lon': station.PuntId.PuntLong
        } for station in stations]

        return JsonResponse({'stations': station_data}, status=200)

    except Exception as e:
        print(f"Error al obtener información de estaciones: {e}")
        return JsonResponse({'message': 'Error al obtener información de estaciones'}, status=500)


@require_http_methods(["GET"])
def get_state_stations(request, station_id):
    try:
        station = (Station.objects.filter(station_id=station_id)
                   .values('station_id', 'mechanical', 'ebike', 'num_docks_available').first())

        if station:
            return JsonResponse({'state': station}, status=200)
        else:
            return JsonResponse({'message': 'Estación no encontrada'}, status=404)

    except Exception as e:
        return JsonResponse({'message': f'Error al obtener información del estado de la estación: {e}'}, status=500)

