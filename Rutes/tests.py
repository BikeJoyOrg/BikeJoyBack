import djongo
from django.test import TestCase, Client
from django.urls import reverse
from djongo.database import DatabaseError
from djongo.exceptions import SQLDecodeError
from rest_framework import status
import json
import os
import django


from Rutes.models import Rutes, Punts, PuntsIntermedis
from Rutes.serializers import RutesSerializer, PuntsSerializer, PuntsIntermedisSerializer


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


class TestAfegirPuntRutaView(TestCase):
    def setUp(self):
        self.client = Client()
        Rutes.objects.create(
            RuteId=1,
            RuteName='Test Rute',
            RuteDistance=10.0,
            RuteTime=10,
            RuteRating=5
        )

    def test_afegir_punt_ruta(self):
        data = {
            'RuteId': 1,  # Example data, replace with actual data
            'PuntName': 'Test Punt',
            'PuntLat': 40.0,
            'PuntLong': -74.0,
            'PuntOrder': 1,
        }
        response = self.client.post(reverse('puntsIntermedisApi'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_afegir_punt_ruta_invalid_data(self):
        invalid_data = {
            # Add invalid data here
        }
        response = self.client.post(reverse('puntsIntermedisApi'), data=json.dumps(invalid_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 500)

