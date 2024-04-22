from django.core.management.base import BaseCommand
import requests
from django.views.decorators.csrf import csrf_exempt

from Stations.models import Station, Punts


@csrf_exempt
class Command(BaseCommand):
    help = 'Carga la información inicial de las estaciones desde el recurso de Open Data Barcelona.'

    def handle(self, *args, **options):
        url_info = (
            'https://opendata-ajuntament.barcelona.cat/data/dataset/bd2462df-6e1e-4e37-8205-a4b8e7313b84/resource'
            '/f60e9291-5aaa-417d-9b91-612a9de800aa/download')
        token = 'a6f42996c707c1e9bb0bb0438fa3ebf5ef5369c006cdac26b8ecad1e73a00f6a'
        headers = {'Authorization': token}

        try:
            response = requests.get(url_info, headers=headers)
            response.raise_for_status()
            data = response.json()["data"]["stations"]

            for station_data in data:
                # Obtener o crear el punto donde se sitúa la estación
                punt, _ = Punts.objects.update_or_create(
                    PuntLat=station_data['lat'],
                    PuntLong=station_data['lon'],
                    PuntName=station_data['name'],
                )

                # Crear la estación con el punto
                Station.objects.update_or_create(
                    station_id=station_data['station_id'],
                    defaults={
                        'PuntId': punt,
                        'mechanical': 0,
                        'ebike': 0,
                        'num_docks_available': 0
                    }
                )

            self.stdout.write(self.style.SUCCESS('Información de estaciones obtenida correctamente'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error al obtener información de estaciones: {e}'))
