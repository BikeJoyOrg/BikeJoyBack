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
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from Rutes.views import rank_route
from Rutes.models import Valoracio, Comentario, RutesCompletades
from Users.models import CustomUser
from django.contrib.auth.models import User
from Rutes.views import comment_route
from Rutes.views import average_rating
from Rutes.views import get_route_comments
from Rutes.views import completed_routes_view

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



class RankRouteTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.rute = Rutes.objects.create(RuteId=1, RuteName='Test Route', RuteDescription='Test Description')

    @patch('Rutes.views.Rutes.objects.get')
    def test_rank_route_valid_mark(self, mock_get):
        mock_get.return_value = self.rute
        request = self.factory.post('/rank_route/1', {'mark': 3})
        request.user = self.user
        response = rank_route(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    def test_rank_route_invalid_mark(self, mock_get):
        mock_get.return_value = self.rute
        request = self.factory.post('/rank_route/1', {'mark': 6})
        request.user = self.user
        response = rank_route(request, 1)
        self.assertEqual(response.status_code, 400)

    @patch('Rutes.views.Rutes.objects.get')
    def test_rank_route_route_not_found(self, mock_get):
        mock_get.side_effect = Rutes.DoesNotExist
        request = self.factory.post('/rank_route/1', {'mark': 3})
        request.user = self.user
        response = rank_route(request, 1)
        self.assertEqual(response.status_code, 404)

class CommentRouteTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.rute = Rutes.objects.create(RuteId=1, RuteName='Test Route', RuteDescription='Test Description')

    @patch('Rutes.views.Rutes.objects.get')
    def test_valid_comment_submission(self, mock_get):
        mock_get.return_value = self.rute
        request = self.factory.post('/comment_route/1', {'text': 'Great route!'})
        request.user = self.user
        response = comment_route(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    def test_invalid_comment_submission(self, mock_get):
        mock_get.return_value = self.rute
        request = self.factory.post('/comment_route/1', {'text': ''})
        request.user = self.user
        response = comment_route(request, 1)
        self.assertEqual(response.status_code, 400)

    @patch('Rutes.views.Rutes.objects.get')
    def test_comment_route_not_found(self, mock_get):
        mock_get.side_effect = Rutes.DoesNotExist
        request = self.factory.post('/comment_route/1', {'text': 'Great route!'})
        request.user = self.user
        response = comment_route(request, 1)
        self.assertEqual(response.status_code, 404)


class AverageRatingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.rute = Rutes.objects.create(RuteId=1, RuteName='Test Route', RuteDescription='Test Description')

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Valoracio.objects.filter')
    def test_valid_average_rating(self, mock_get, mock_filter):
        mock_get.return_value = self.rute
        mock_filter.return_value.aggregate.return_value = {'mark__avg': 4.5}
        request = self.factory.get('/average_rating/1')
        request.user = self.user
        response = average_rating(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Valoracio.objects.filter')
    def test_no_ratings_for_route(self, mock_get, mock_filter):
        mock_get.return_value = self.rute
        mock_filter.return_value.aggregate.return_value = {'mark__avg': None}
        request = self.factory.get('/average_rating/1')
        request.user = self.user
        response = average_rating(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    def test_average_rating_route_not_found(self, mock_get):
        mock_get.side_effect = Rutes.DoesNotExist
        request = self.factory.get('/average_rating/1')
        request.user = self.user
        response = average_rating(request, 1)
        self.assertEqual(response.status_code, 404)




class GetRouteCommentsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.rute = Rutes.objects.create(RuteId=1, RuteName='Test Route', RuteDescription='Test Description')

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Comentario.objects.filter')
    def test_comments_exist_for_route(self, mock_get, mock_filter):
        mock_get.return_value = self.rute
        mock_filter.return_value.exists.return_value = True
        request = self.factory.get('/get_route_comments/1')
        request.user = self.user
        response = get_route_comments(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Comentario.objects.filter')
    def test_no_comments_for_route(self, mock_get, mock_filter):
        mock_get.return_value = self.rute
        mock_filter.return_value.exists.return_value = False
        request = self.factory.get('/get_route_comments/1')
        request.user = self.user
        response = get_route_comments(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    def test_get_comments_route_not_found(self, mock_get):
        mock_get.side_effect = Rutes.DoesNotExist
        request = self.factory.get('/get_route_comments/1')
        request.user = self.user
        response = get_route_comments(request, 1)
        self.assertEqual(response.status_code, 404)



class CompletedRoutesViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.rute = Rutes.objects.create(RuteId=1, RuteName='Test Route', RuteDescription='Test Description')

    @patch('Rutes.views.RutesCompletades.objects.filter')
    def test_completed_routes_exist(self, mock_filter):
        mock_filter.return_value.exists.return_value = True
        request = self.factory.get('/completed_routes_view')
        request.user = self.user
        response = completed_routes_view(request)
        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.RutesCompletades.objects.filter')
    def test_no_completed_routes(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        request = self.factory.get('/completed_routes_view')
        request.user = self.user
        response = completed_routes_view(request)
        self.assertEqual(response.status_code, 200)