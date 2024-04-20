from django.core.management.base import BaseCommand, CommandError
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import requests
import pytz

from Stations.models import Station


@csrf_exempt
class Command(BaseCommand):
    help = 'Updates station information from the Barcelona open data portal'

    def handle(self, *args, **options):
        url_state = (
            'https://opendata-ajuntament.barcelona.cat/data/dataset/6aa3416d-ce1a-494d-861b-7bd07f069600/resource'
            '/1b215493-9e63-4a12-8980-2d7e0fa19f85/download')
        token = 'a6f42996c707c1e9bb0bb0438fa3ebf5ef5369c006cdac26b8ecad1e73a00f6a'
        headers = {
            'Authorization': token,
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url_state, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            data = json_data["data"]["stations"]

            for station_data in data:
                stations, created = Station.objects.update_or_create(
                    station_id=station_data['station_id'],
                    defaults={
                        'mechanical': station_data['num_bikes_available_types']['mechanical'],
                        'ebike': station_data['num_bikes_available_types']['ebike'],
                        'num_docks_available': station_data['num_docks_available'],
                    }
                )

            self.stdout.write(self.style.SUCCESS('Información de estaciones actualizada correctamente'))

        except requests.exceptions.RequestException as e:
            raise CommandError(f'Error al obtener información de estaciones: {e}')
