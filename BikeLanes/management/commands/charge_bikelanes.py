from django.core.management.base import BaseCommand
import requests
from BikeLanes.models import BikeLane, LatLng
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
class Command(BaseCommand):
    help = 'Carga la información inicial de las BikeLanes desde un archivo GeoJSON.'

    def handle(self, *args, **options):
        url_info = 'https://opendata-ajuntament.barcelona.cat/resources/bcn/CarrilsBici/CARRIL_BICI.geojson'

        try:
            response = requests.get(url_info)
            response.raise_for_status()
            data = response.json()["features"]

            for feature_data in data:
                # Crear o actualizar la BikeLane
                bike_lane, _ = BikeLane.objects.update_or_create(
                    id=feature_data['properties']['ID'],
                )

                # Crear o actualizar los LatLng asociados a la BikeLane
                for coordinates in feature_data['geometry']['coordinates']:
                    lat_lng, _ = LatLng.objects.update_or_create(
                        latitude=coordinates[1],
                        longitude=coordinates[0],
                        defaults={
                            'bike_lane': bike_lane,
                        }
                    )

            self.stdout.write(self.style.SUCCESS('Información de BikeLanes obtenida correctamente'))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error al obtener información de BikeLanes: {e}'))