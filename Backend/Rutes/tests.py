from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apiCrud.settings')
django.setup()

from Rutes.models import Rutes, Punts, PuntsIntermedis
from serializers import RutesSerializer, PuntsSerializer, PuntsIntermedisSerializer


class TestRutesApiView(TestCase):
    def setUp(self):
        self.client = Client()
        Rutes.objects.create(
            RuteId=1,
            RuteName='Test Rute',
            RuteDistance=10.0,
            RuteTime=10,
            RuteRating=5
        )

    def test_get_rutes(self):
        response = self.client.get(reverse('rutesApi'))
        self.assertEqual(response.status_code, 200)

    def test_create_rute(self):
        data = {
            "RuteId": 13,
            "RuteName": "Test Rute2",
            "RuteDistance": 10.0,
            "RuteTime": 10,
            "RuteRating": 5
        }
        response = self.client.post(reverse('rutesApi'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rute_invalid_data(self):
        invalid_data = {
            "RuteId": 2,
            "RuteDistance": 10.0,
            "RuteTime": 10,
            "RuteRating": 5
        }
        response = self.client.post(reverse('rutesApi'), data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_create_rute_nom_duplicated_error(self):
        invalid_data = {
            "RuteId": 2,
            "RuteName": "Test Rute",
            "RuteDistance": 10.0,
            "RuteTime": 10,
            "RuteRating": 5
        }
        response = self.client.post(reverse('rutesApi'), data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)

class TestAfegirPuntRutaView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_afegir_punt_ruta(self):
        data = {
            'RuteId': 1,  # Example data, replace with actual data
            'PuntName': 'Test Punt',
            'PuntLat': 40.0,
            'PuntLong': -74.0,
            'PuntOrder': 1,
        }
        response = self.client.post(reverse('afegir-punt-ruta'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_afegir_punt_ruta_invalid_data(self):
        invalid_data = {
            # Add invalid data here
        }
        response = self.client.post(reverse('afegir-punt-ruta'), data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_afegir_punt_ruta_method_not_allowed(self):
        response = self.client.get(reverse('afegir-punt-ruta'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)