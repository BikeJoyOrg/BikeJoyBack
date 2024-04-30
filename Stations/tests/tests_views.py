"""""
from django.test import TestCase, Client
from django.urls import reverse
from requests import patch

from Stations.models import Station, Punts


class GetInfoStationsTest(TestCase):
    def setUp(self):
        # Configura un cliente de prueba
        self.client = Client()
        # Crea datos de prueba
        self.punt1 = Punts.objects.create(PuntName="Test Location 1", PuntLat=40.714224, PuntLong=-73.961452)
        self.punt2 = Punts.objects.create(PuntName="Test Location 2", PuntLat=40.705, PuntLong=-74.009)
        Station.objects.create(PuntId=self.punt1, mechanical=2, ebike=3, num_docks_available=5)
        Station.objects.create(PuntId=self.punt2, mechanical=4, ebike=1, num_docks_available=10)

    def test_get_info_stations_success(self):
        response = self.client.get(reverse('obtener-informacion-estaciones'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('stations', data)
        self.assertEqual(len(data['stations']), 2)
        self.assertEqual(data['stations'][0]['address'], self.punt1.PuntName)
        self.assertEqual(float(data['stations'][0]['lat']), self.punt1.PuntLat)
        self.assertEqual(float(data['stations'][0]['lon']), self.punt1.PuntLong)


class GetStateStationsTest(TestCase):
    def setUp(self):
        # Configura un cliente de prueba
        self.client = Client()
        # Crea datos de prueba
        self.punt = Punts.objects.create(PuntName="Test Location", PuntLat=40.714224, PuntLong=-73.961452)
        self.station = Station.objects.create(PuntId=self.punt, mechanical=2, ebike=3, num_docks_available=5)

    def test_get_state_stations_success(self):
        # Prueba el caso de éxito
        response = self.client.get(reverse('obtener-estado-estaciones', args=[self.station.station_id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('state', data)
        expected_data = {
            'station_id': self.station.station_id,
            'mechanical': self.station.mechanical,
            'ebike': self.station.ebike,
            'num_docks_available': self.station.num_docks_available,
        }
        self.assertEqual(data['state'], expected_data)

    def test_get_state_stations_not_found(self):
        # Prueba cuando la estación no se encuentra
        response = self.client.get(
            reverse('obtener-estado-estaciones', args=[999]))  # Usamos un ID que sabemos que no existe
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Estación no encontrada')
        
        """""
