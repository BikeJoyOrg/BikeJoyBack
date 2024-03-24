import requests
from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from Stations.views import charge_info_stations


class TestApiConnection(TestCase):
    def test_api_connection(self):
        # Simular una solicitud HTTP
        request = HttpRequest()
        response = charge_info_stations(request)

        # Verificar si la vista devuelve una respuesta exitosa (código 200)
        self.assertEqual(response.status_code, 200)

        # Verificar que la respuesta renderizada contiene el mensaje esperado
        expected_message = 'Informacion de estaciones obtenida correctamente'
        self.assertIn(expected_message, response.content.decode())
