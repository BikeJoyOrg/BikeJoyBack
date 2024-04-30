from django.test import TestCase
from rest_framework.test import APIClient
import json
from django.http import JsonResponse

from Users.models import CustomUser


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registro_exitoso(self):
        data = {
            'username': 'testuser',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_nombre_usuario_existente(self):
        # Primero crea un usuario con el mismo nombre
        CustomUser.objects.create(username='existinguser', password='prova1234', email='test@gmail.com')
        data = {
            'username': 'existinguser',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': 'test1@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': 'Username already exists'})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())
