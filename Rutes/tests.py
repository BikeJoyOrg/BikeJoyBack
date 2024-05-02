import json
import os

from django_mock_queries.query import MockSet
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Rutes, PuntsVisitats
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
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from Rutes.models import Rutes, Comentario
from rest_framework.authtoken.models import Token




class RutesApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.rute1 = Rutes.objects.create(RuteName="Rute1", RuteDescription="Description1", RuteTime=60, RuteDistance=5,
                                          PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user)
        self.rute2 = Rutes.objects.create(RuteName="Rute2", RuteDescription="Description2", RuteTime=120,
                                          RuteDistance=10, PuntIniciLat=41.3723, PuntIniciLong=2.1699,
                                          creador=self.user)
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
        response = self.client.get(reverse('rutesApi'), {'duration': 120})
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)

class AfegirRutaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        token, created = Token.objects.get_or_create(user=self.user)
        self.token = token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_afegir_ruta_with_valid_data(self):
        data = {
            'RuteName': 'Test Ruta',
            'RuteDescription': 'Test Description',
            'RuteTime': 10,
            'RuteDistance': 5,
            'PuntIniciLat': 41.3834,
            'PuntIniciLong': 2.1761
        }
        response = self.client.post('/addruta/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Rutes.objects.count(), 1)
        self.assertEqual(Rutes.objects.get().RuteName, 'Test Ruta')


    def test_afegir_ruta_with_invalid_data(self):
        data = {
            'RuteName': 'Test Ruta',
            'RuteDescription': 'Test Description',
            'RuteTime': 'invalid',
            'RuteDistance': 'invalid',
            'PuntIniciLat': 41.3834,
            'PuntIniciLong': 2.1761
        }
        response = self.client.post('/addruta/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Rutes.objects.count(), 0)
def test_update_existing_punt_in_ruta_with_authenticated_user(self):
    PuntsIntermedis.objects.create(PuntId=self.punt, RuteId=self.rute1, PuntOrder=1)
    request_data = {
        'RuteId': self.rute1.RuteId,
        'PuntLat': self.punt.PuntLat,
        'PuntLong': self.punt.PuntLong,
        'PuntName': self.punt.PuntName,
        'PuntOrder': 2
    }
    request = self.factory.post('/puntsInterRuta/', json.dumps(request_data), content_type='application/json')
    response = AfegirPuntRuta(request)
    self.assertEqual(response.status_code, 200)
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

class RankRouteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.rute1 = Rutes.objects.create(RuteName="Rute1", RuteDescription="Description1", RuteTime=60, RuteDistance=5,
                                          PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Valoracio.objects.filter')
    def test_rank_route_creates_new_rating(self, mock_valoracio_filter, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_valoracio_filter.return_value = Valoracio.objects.none()

        response = self.client.post('/routes/rank/1/', {'mark': 5}, format='json')

        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Valoracio.objects.filter')
    def test_rank_route_updates_existing_rating(self, mock_valoracio_filter, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_valoracio_filter.return_value = Valoracio.objects.filter(mark=3)

        response = self.client.post('/routes/rank/1/', {'mark': 5}, format='json')

        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    def test_rank_route_returns_error_when_rute_does_not_exist(self, mock_rute_get):
        mock_rute_get.side_effect = Rutes.DoesNotExist

        response = self.client.post('/routes/rank/1/', {'mark': 5}, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Route not found'})

    def test_rank_route_returns_error_when_invalid_mark(self):
        response = self.client.post('/routes/rank/1/', {'mark': 6}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid mark'})

class CommentRouteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.rute1 = Rutes.objects.create(RuteName="Rute1", RuteDescription="Description1", RuteTime=60, RuteDistance=5,
                                          PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.Rutes.objects.get')
    def test_comment_route_creates_new_comment(self, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)

        response = self.client.post('/routes/comment/1/', {'text': 'Great route!'}, format='json')

        self.assertEqual(response.status_code, 200)

    @patch('Rutes.views.Rutes.objects.get')
    def test_comment_route_returns_error_when_rute_does_not_exist(self, mock_rute_get):
        mock_rute_get.side_effect = Rutes.DoesNotExist

        response = self.client.post('/routes/comment/1/', {'text': 'Great route!'}, format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Route not found'})

    def test_comment_route_returns_error_when_invalid_text(self):
        response = self.client.post('/routes/comment/1/', {'text': ''}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid text'})

class CompletedRoutesViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.RutesCompletades.objects.filter')
    def test_completed_routes_view_returns_all_completed_routes(self, mock_completed_routes_filter):
        mock_completed_routes_filter.return_value = [
            RutesCompletades(id=1, ruta=Rutes(RuteId=1), user=self.user, date_completed='2022-01-01T00:00:00Z', temps=60.0),
            RutesCompletades(id=2, ruta=Rutes(RuteId=2), user=self.user, date_completed='2022-01-02T00:00:00Z', temps=120.0),
        ]

        response = self.client.get('/routes/completed-routes/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'ruta_id': 1, 'rated': False},
            {'ruta_id': 2, 'rated': False},
        ])

    @patch('Rutes.views.RutesCompletades.objects.filter')
    def test_completed_routes_view_returns_empty_when_no_completed_routes(self, mock_completed_routes_filter):
        mock_completed_routes_filter.return_value = []

        response = self.client.get('/routes/completed-routes/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
"""
class AverageRatingTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.rute1 = Rutes.objects.create(RuteName="Rute1", RuteDescription="Description1", RuteTime=60, RuteDistance=5,
                                          PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Valoracio.objects.filter')
    def test_average_rating_returns_average_rating(self, mock_valoracio_filter, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_valoracio_filter.return_value = [
            Valoracio(id=1, ruta=Rutes(RuteId=1), user=self.user, mark=5),
            Valoracio(id=2, ruta=Rutes(RuteId=1), user=self.user, mark=4),
        ]

        response = self.client.get('/routes/1/average-rating/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 4.5)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Valoracio.objects.filter')
    def test_average_rating_returns_zero_when_no_ratings(self, mock_valoracio_filter, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_valoracio_filter.return_value = []

        response = self.client.get('/routes/1/average-rating/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 0)

    @patch('Rutes.views.Rutes.objects.get')
    def test_average_rating_returns_error_when_rute_does_not_exist(self, mock_rute_get):
        mock_rute_get.side_effect = Rutes.DoesNotExist

        response = self.client.get('/routes/1/average-rating/', format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Route not found'})
"""
class GetRouteCommentsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.rute1 = Rutes.objects.create(RuteName="Rute1", RuteDescription="Description1", RuteTime=60, RuteDistance=5,
                                          PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Comentario.objects.filter')
    def test_get_route_comments_returns_all_comments(self, mock_comment_filter, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_comment_filter.return_value = [
            Comentario(id=1, ruta=Rutes(RuteId=1), user=self.user, text='Great route!'),
            Comentario(id=2, ruta=Rutes(RuteId=1), user=self.user, text='Nice view!'),
        ]

        response = self.client.get('/routes/1/comments/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'id': 1, 'ruta': 1, 'user': self.user.id, 'text': 'Great route!'},
            {'id': 2, 'ruta': 1, 'user': self.user.id, 'text': 'Nice view!'},
        ])

    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Comentario.objects.filter')
    def test_get_route_comments_returns_empty_when_no_comments(self, mock_comment_filter, mock_rute_get):
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_comment_filter.return_value = []

        response = self.client.get('/routes/1/comments/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @patch('Rutes.views.Rutes.objects.get')
    def test_get_route_comments_returns_error_when_rute_does_not_exist(self, mock_rute_get):
        mock_rute_get.side_effect = Rutes.DoesNotExist

        response = self.client.get('/routes/1/comments/', format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'error': 'Route not found'})
class PuntsIntermedisListTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.rute = Rutes.objects.create(RuteId=1, RuteName='Test Rute', RuteDescription='Test Description', RuteDistance=10, RuteTime=60, PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user)
        self.punt = Punts.objects.create(PuntId=1, PuntName='Test Punt', PuntLat=41.3834, PuntLong=2.1761)
        self.punt_intermedi = PuntsIntermedis.objects.create(PuntInterId=1, PuntOrder=1, RuteId=self.rute, PuntId=self.punt)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_punts_intermedis_list_with_existing_intermediary_points(self):
        response = self.client.get('/puntos-intermedios/1/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)

    def test_punts_intermedis_list_with_no_intermediary_points(self):
        response = self.client.get('/puntos-intermedios/2/')
        self.assertEqual(response.status_code, 200)

class AfegirPuntRutaTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Punts.objects.get_or_create')
    @patch('Rutes.views.PuntsIntermedis.objects.get_or_create')
    def test_afegirPuntRuta_creates_new_punt_and_punt_intermedi(
            self, mock_punt_inter_create, mock_punt_create, mock_rute_get, mock_parse):
        mock_parse.return_value = {
            'RuteId': 1,
            'PuntLat': 41.3834,
            'PuntLong': 2.1761,
            'PuntName': 'Test Punt',
            'PuntOrder': 1
        }
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_punt_create.return_value = (Punts(PuntId=1), True)
        mock_punt_inter_create.return_value = (PuntsIntermedis(PuntInterId=1), True)

        response = self.client.post('/puntsInterRuta/', {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Punto intermedio creado correctamente'})

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.Punts.objects.get_or_create')
    @patch('Rutes.views.PuntsIntermedis.objects.get_or_create')
    def test_afegirPuntRuta_updates_existing_punt_and_punt_intermedi(
            self, mock_punt_inter_create, mock_punt_create, mock_rute_get, mock_parse):
        mock_parse.return_value = {
            'RuteId': 1,
            'PuntLat': 41.3834,
            'PuntLong': 2.1761,
            'PuntName': 'Test Punt',
            'PuntOrder': 1
        }
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_punt_create.return_value = (Punts(PuntId=1), False)
        mock_punt_inter_create.return_value = (PuntsIntermedis(PuntInterId=1), False)

        response = self.client.post('/puntsInterRuta/', {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Punto intermedio actualizado correctamente'})

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Rutes.objects.get')
    def test_afegirPuntRuta_returns_error_when_rute_does_not_exist(
            self, mock_rute_get, mock_parse):
        mock_parse.return_value = {
            'RuteId': 1,
            'PuntLat': 41.3834,
            'PuntLong': 2.1761,
            'PuntName': 'Test Punt',
            'PuntOrder': 1
        }
        mock_rute_get.side_effect = Rutes.DoesNotExist

        response = self.client.post('/puntsInterRuta/', {}, format='json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'message': 'Error al procesar la solicitud'})


class RutaCompletadaTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.RutesCompletades.objects.get_or_create')
    def test_ruta_completada_creates_new_entry(self, mock_ruta_completada_create, mock_rute_get, mock_parse):
        mock_parse.return_value = {
            'temps': 120,
        }
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_ruta_completada_create.return_value = (RutesCompletades(id=1), True)

        response = self.client.post('/routes/completed/1/', {}, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Ruta completada guardada correctamente'})

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Rutes.objects.get')
    @patch('Rutes.views.RutesCompletades.objects.get_or_create')
    def test_ruta_completada_updates_existing_entry(self, mock_ruta_completada_create, mock_rute_get, mock_parse):
        mock_parse.return_value = {
            'temps': 120,
        }
        mock_rute_get.return_value = Rutes(RuteId=1)
        mock_ruta_completada_create.return_value = (RutesCompletades(id=1), False)

        response = self.client.post('/routes/completed/1/', {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Ruta completada actualizada correctamente'})

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Rutes.objects.get')
    def test_ruta_completada_returns_error_when_rute_does_not_exist(self, mock_rute_get, mock_parse):
        mock_parse.return_value = {
            'temps': 120,
        }
        mock_rute_get.side_effect = Rutes.DoesNotExist

        response = self.client.post('/routes/completed/1/', {}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Error al guardar ruta completada')

class AddPuntsVisitatsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Punts.objects.update_or_create')
    @patch('Rutes.views.PuntsVisitats.objects.get_or_create')
    def test_add_punts_visitats_creates_new_entry(self, mock_punts_visitats_create, mock_punts_create, mock_parse):
        mock_parse.return_value = {
            'PuntLat': 41.3834,
            'PuntLong': 2.1761,
            'PuntName': 'Test Punt',
        }
        mock_punts_create.return_value = (Punts(PuntId=1), True)
        mock_punts_visitats_create.return_value = (PuntsVisitats(id=1), True)

        response = self.client.post('/routes/add_punt_visitat/', {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Punto visitado creado correctamente'})

    @patch('Rutes.views.JSONParser.parse')
    @patch('Rutes.views.Punts.objects.update_or_create')
    @patch('Rutes.views.PuntsVisitats.objects.get_or_create')
    def test_add_punts_visitats_updates_existing_entry(self, mock_punts_visitats_create, mock_punts_create, mock_parse):
        mock_parse.return_value = {
            'PuntLat': 41.3834,
            'PuntLong': 2.1761,
            'PuntName': 'Test Punt',
        }
        mock_punts_create.return_value = (Punts(PuntId=1), False)
        mock_punts_visitats_create.return_value = (PuntsVisitats(id=1), False)

        response = self.client.post('/routes/add_punt_visitat/', {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Punto visitado actualizado correctament'})

class PuntsVisitatsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.Punts.objects.filter')
    def punts_visitats_returns_all_visited_points(self, mock_punts_filter):
        mock_punts_filter.return_value = [
            Punts(PuntId=1, PuntLat=41.3834, PuntLong=2.1761, PuntName='Test Punt 1'),
            Punts(PuntId=2, PuntLat=41.3835, PuntLong=2.1762, PuntName='Test Punt 2'),
        ]

        response = self.client.get('/routes/punt_visitat/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'PuntId': 1, 'PuntLat': 41.3834, 'PuntLong': 2.1761, 'PuntName': 'Test Punt 1'},
            {'PuntId': 2, 'PuntLat': 41.3835, 'PuntLong': 2.1762, 'PuntName': 'Test Punt 2'},
        ])

    @patch('Rutes.views.Punts.objects.filter')
    def punts_visitats_returns_empty_when_no_visited_points(self, mock_punts_filter):
        mock_punts_filter.return_value = []

        response = self.client.get('/routes/punt_visitat/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
class GetRoutesTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    @patch('Rutes.views.Rutes.objects.all')
    def test_get_routes_returns_all_routes(self, mock_rutes_all):
        mock_rutes_all.return_value = [
            Rutes(RuteId=1, RuteName='Test Route 1', RuteDistance=1000, RuteTime=60, RuteRating=5, PuntIniciLat=41.3834, PuntIniciLong=2.1761, creador=self.user),
            Rutes(RuteId=2, RuteName='Test Route 2', RuteDistance=2000, RuteTime=120, RuteRating=4, PuntIniciLat=41.3835, PuntIniciLong=2.1762, creador=self.user),
        ]

        response = self.client.get('/rutas/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {'RuteId': 1, 'RuteName': 'Test Route 1', 'distance_km': 1.0, 'PuntIniciLat': 41.3834, 'PuntIniciLong': 2.1761, 'PuntFinalLat': None, 'PuntFinalLong': None},
            {'RuteId': 2, 'RuteName': 'Test Route 2', 'distance_km': 2.0, 'PuntIniciLat': 41.3835, 'PuntIniciLong': 2.1762, 'PuntFinalLat': None, 'PuntFinalLong': None},
        ])

    @patch('Rutes.views.Rutes.objects.all')
    def test_get_routes_returns_empty_when_no_routes(self, mock_rutes_all):
        mock_rutes_all.return_value = []

        response = self.client.get('/rutas/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])