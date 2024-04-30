"""""
from django.test import TestCase, Client
from django.urls import reverse
from .models import BikeLane, LatLng

class GetInfoBikeLanesTest(TestCase):
    def setUp(self):
        # Configura un cliente de prueba
        self.client = Client()
        # Crea datos de prueba
        self.bikeLane1 = BikeLane.objects.create(id="1")
        self.bikeLane2 = BikeLane.objects.create(id="2")
        self.latlng1 = LatLng.objects.create(latitude=40.714224, longitude=-73.961452, bike_lane=self.bikeLane1)
        self.latlng2 = LatLng.objects.create(latitude=40.705, longitude=-74.009, bike_lane=self.bikeLane1)
        self.latlng3 = LatLng.objects.create(latitude=40.71, longitude=-74.01, bike_lane=self.bikeLane1)
        self.latlng4 = LatLng.objects.create(latitude=40.74, longitude=-74.04, bike_lane=self.bikeLane2)
        self.latlng5 = LatLng.objects.create(latitude=40.75, longitude=-74.05, bike_lane=self.bikeLane2)


    def test_get_info_bikelanes_content(self):
        response = self.client.get(reverse('get_info_bikelanes'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('bikelanes', data)
        self.assertEqual(len(data['bikelanes']), 2)
        bikelanes_data = data['bikelanes']
        for bikelane_data in bikelanes_data:
            if bikelane_data['id'] == self.bikeLane1.id:
                self.assertEqual(len(bikelane_data['lat_lngs']), 3)
                self.assertEqual(bikelane_data['lat_lngs'][0]['latitude'], self.latlng1.latitude)
                self.assertEqual(bikelane_data['lat_lngs'][1]['latitude'], self.latlng2.latitude)
                self.assertEqual(bikelane_data['lat_lngs'][2]['latitude'], self.latlng3.latitude)
            elif bikelane_data['id'] == self.bikeLane2.id:
                self.assertEqual(len(bikelane_data['lat_lngs']), 2)
                self.assertEqual(bikelane_data['lat_lngs'][0]['latitude'], self.latlng4.latitude)
                self.assertEqual(bikelane_data['lat_lngs'][1]['latitude'], self.latlng5.latitude)
                
                """""