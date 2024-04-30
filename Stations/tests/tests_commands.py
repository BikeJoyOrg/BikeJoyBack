"""""
from django.core.management import call_command
from django.forms import model_to_dict
from django.test import TestCase
from unittest.mock import patch

from Rutes.models import Punts
from Stations.models import Station


class TestCommands(TestCase):
    @patch('Stations.management.commands.charge_stations.requests.get')
    def test_command_charges_stations_successfully(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "data": {
                "stations": [
                    {
                        "station_id": 1,
                        "name": "Test Station 1",
                        "lat": 41,
                        "lon": 2,
                    },
                    {
                        "station_id": 2,
                        "name": "Test Station 2",
                        "lat": 41,
                        "lon": 2,
                    }
                ]
            }
        }

        # Asegúrate de que no hay estaciones antes de ejecutar el comando
        self.assertEqual(Station.objects.count(), 0)
        self.assertEqual(Punts.objects.count(), 0)

        # Ejecuta el comando
        call_command('charge_stations')

        # Verifica que el comando ha creado las estaciones correctamente
        self.assertEqual(Station.objects.count(), 2)
        self.assertEqual(Punts.objects.count(), 2)

        expected_data_1 = {
            "station_id": 1,
            "PuntId": 1,
            "mechanical": 0,
            "ebike": 0,
            "num_docks_available": 0,
        }
        expected_data_2 = {
            "station_id": 2,
            "PuntId": 2,
            "mechanical": 0,
            "ebike": 0,
            "num_docks_available": 0,
        }
        object_data_1 = Station.objects.get(station_id=1)
        self.assertEqual(model_to_dict(object_data_1), expected_data_1)
        object_data_2 = Station.objects.get(station_id=2)
        self.assertEqual(model_to_dict(object_data_2), expected_data_2)

    @patch('Stations.management.commands.update_stations.requests.get')
    def test_update_stations_command_successfully(self, mock_get):
        # Crear objectes necessaris pel test
        punt_1 = Punts.objects.create(PuntId=1, PuntName="Test Punt 1", PuntLat=41, PuntLong=2)
        punt_2 = Punts.objects.create(PuntId=2, PuntName="Test Punt 2", PuntLat=41, PuntLong=2)
        Station.objects.create(station_id=1, PuntId=punt_1, mechanical=0, ebike=0, num_docks_available=0)
        Station.objects.create(station_id=2, PuntId=punt_2, mechanical=0, ebike=0, num_docks_available=0)

        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "data": {
                "stations": [
                    {
                        "station_id": 1,
                        "num_bikes_available_types": {
                            "mechanical": 5,
                            "ebike": 3
                        },
                        "num_docks_available": 10
                    },
                    {
                        "station_id": 2,
                        "num_bikes_available_types": {
                            "mechanical": 2,
                            "ebike": 1
                        },
                        "num_docks_available": 7
                    }
                ]
            }
        }

        # Ejecuta el comando
        call_command('update_stations')

        # Verifica que el comando ha actualizado la información de las estaciones correctamente
        station_1 = Station.objects.get(station_id=1)
        self.assertEqual(station_1.mechanical, 5)
        self.assertEqual(station_1.ebike, 3)
        self.assertEqual(station_1.num_docks_available, 10)

        station_2 = Station.objects.get(station_id=2)
        self.assertEqual(station_2.mechanical, 2)
        self.assertEqual(station_2.ebike, 1)
        self.assertEqual(station_2.num_docks_available, 7)
        
        
        """""
