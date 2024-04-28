import json
import os

from django_mock_queries.query import MockSet
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from .models import Rutes
from .serializers import RutesSerializer
from unittest.mock import patch
from .views import punts_intermedis_list , AfegirPuntRuta
from .models import PuntsIntermedis, Punts, Rutes
from rest_framework.parsers import JSONParser
class RutesApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.rute1 = Rutes.objects.create(RuteName="Rute1", RuteDescription="Description1", RuteTime=10, RuteDistance=5,
                                          PuntIniciLat=41.3834, PuntIniciLong=2.1761)
        self.rute2 = Rutes.objects.create(RuteName="Rute2", RuteDescription="Description2", RuteTime=20,
                                          RuteDistance=10, PuntIniciLat=41.3723, PuntIniciLong=2.1699)
        self.valid_payload = {
            'RuteName': 'Rute3',
            'RuteDescription': 'Description3',
            'RuteTime': 30,
            'RuteDistance': 15,
            'PuntIniciLat': 41.3845,
            'PuntIniciLong': 2.1821
        }
        self.invalid_payload = {
            'RuteName': '',
            'RuteDescription': 'Description4',
            'RuteTime': 40,
            'RuteDistance': 20,
            'PuntIniciLat': 41.4110,
            'PuntIniciLong': 2.1916
        }

    def test_get_all_rutes(self):
        response = self.client.get(reverse('rutesApi'))
        rutes = Rutes.objects.all()
        serializer = RutesSerializer(rutes, many=True)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_rute_by_distance(self):
        response = self.client.get(reverse('rutesApi'), {'distance': 10})
        rutes = Rutes.objects.filter(RuteDistance__lte=10)
        serializer = RutesSerializer(rutes, many=True)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_rute_by_duration(self):
        response = self.client.get(reverse('rutesApi'), {'duration': 15})
        rutes = Rutes.objects.filter(RuteTime__lte=15)
        serializer = RutesSerializer(rutes, many=True)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_create_valid_rute(self):
        response = self.client.post(
            reverse('rutesApi'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_rute(self):
        response = self.client.post(
            reverse('rutesApi'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

class PuntsIntermedisListTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('Rutes.models.PuntsIntermedis.objects.filter')
    def test_punts_intermedis_list_happy_path(self, mock_filter):
        # Mock the PuntsIntermedis objects
        mock_punt = Punts(PuntLat=41.3834, PuntLong=2.1761)
        mock_punts_intermedis = MockSet(*[PuntsIntermedis(PuntId=mock_punt, PuntOrder=i) for i in range(5)])
        mock_filter.return_value = mock_punts_intermedis

        request = self.factory.get('/punts_intermedis_list/1')
        response = punts_intermedis_list(request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode()), [{'lat': 41.3834, 'lng': 2.1761} for _ in range(5)])
    @patch('Rutes.models.PuntsIntermedis.objects.filter')
    def test_punts_intermedis_list_no_punts(self, mock_filter):
        # Mock the case where no PuntsIntermedis are found
        mock_filter.return_value = MockSet()

        request = self.factory.get('/punts_intermedis_list/1')
        response = punts_intermedis_list(request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode()), [])

class AfegirPuntRutaTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.ruta = Rutes.objects.create(RuteName="Test Ruta", RuteDescription="Test Description", RuteDistance=10, RuteTime=20, PuntIniciLat=41.3834, PuntIniciLong=2.1761)
        self.punt = Punts.objects.create(PuntName="Test Punt", PuntLat=41.3834, PuntLong=2.1761)

    def test_add_new_punt_to_ruta(self):
        request_data = {
            'RuteId': self.ruta.RuteId,
            'PuntLat': 41.3835,
            'PuntLong': 2.1762,
            'PuntName': 'New Punt',
            'PuntOrder': 1
        }
        request = self.factory.post('/AfegirPuntRuta/', json.dumps(request_data), content_type='application/json')
        response = AfegirPuntRuta(request)
        self.assertEqual(response.status_code, 200)

    def test_update_existing_punt_in_ruta(self):
        PuntsIntermedis.objects.create(PuntId=self.punt, RuteId=self.ruta, PuntOrder=1)
        request_data = {
            'RuteId': self.ruta.RuteId,
            'PuntLat': self.punt.PuntLat,
            'PuntLong': self.punt.PuntLong,
            'PuntName': self.punt.PuntName,
            'PuntOrder': 2
        }
        request = self.factory.post('/AfegirPuntRuta/', json.dumps(request_data), content_type='application/json')
        response = AfegirPuntRuta(request)
        self.assertEqual(response.status_code, 200)

    def test_add_punt_to_nonexistent_ruta(self):
        request_data = {
            'RuteId': 9999,
            'PuntLat': 41.3835,
            'PuntLong': 2.1762,
            'PuntName': 'New Punt',
            'PuntOrder': 1
        }
        request = self.factory.post('/AfegirPuntRuta/', json.dumps(request_data), content_type='application/json')
        response = AfegirPuntRuta(request)
        self.assertEqual(response.status_code, 500)