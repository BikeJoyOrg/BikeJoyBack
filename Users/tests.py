from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import json
from django.http import JsonResponse

from Users.models import CustomUser
from Users.views import actualitzar_stats


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

    def test_sin_username(self):
        data = {
            'username': '',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'username': ['Este campo es requerido.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_sin_password1(self):
        data = {
            'username': 'testuser',
            'password1': '',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'password1': ['Este campo es requerido.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_sin_password2(self):
        data = {
            'username': 'testuser',
            'password1': 'prova1234',
            'password2': '',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'password2': ['Este campo es requerido.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_sin_email(self):
        data = {
            'username': 'testuser',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': ''
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'email': ['Este campo es requerido.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

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

    def test_email_existente(self):
        # Primero crea un usuario con el mismo nombre
        CustomUser.objects.create(username='nonexistinguser', password='prova1234', email='test@gmail.com')
        data = {
            'username': 'existinguser',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'email': ['Este correo electrónico ya está registrado.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_contrasena_no_coincide(self):
        data = {
            'username': 'testuser',
            'password1': 'prova123',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'password2': ['Los dos campos de contraseña no coinciden.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_contrasena_insegura(self):
        data = {
            'username': 'testuser',
            'password1': 'prova',
            'password2': 'prova',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'password2': ['Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.', 'Esta contraseña es demasiado común.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_contrasena_parecida_username(self):
        data = {
            'username': 'testuser',
            'password1': 'testuser1234',
            'password2': 'testuser1234',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'password2': ['La contraseña es demasiado similar a la de nombre de usuario.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_contrasena_parecida_email(self):
        data = {
            'username': 'provauser',
            'password1': 'testuser1234',
            'password2': 'testuser1234',
            'email': 'testuser@gmail.com'
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'password2': ['La contraseña es demasiado similar a la de dirección de correo electrónico.']}})
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())


    def test_login_exitoso(self):
        data = {
            'username': 'testuser',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        self.client.post('/users/register/', data)
        data = {
            'username': 'testuser',
            'password': 'prova1234',
        }
        response = self.client.post('/users/login/', data)
        self.assertEqual(response.status_code, 200)

'''
    def test_login_sin_username(self):
        data = {
            'username': 'testuser',
            'password1': 'prova1234',
            'password2': 'prova1234',
            'email': 'test@gmail.com'
        }
        self.client.post('/users/register/', data)
        data = {
            'username': 'testuser',
            'password1': 'prova1234',
        }
        response = self.client.post('/users/login/', data)
        print(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': {'username': ['Este campo es requerido.']}})
        '''


@override_settings(ROOT_URLCONF='Users.urls')
class ActualitzarStatsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        token, created = Token.objects.get_or_create(user=self.user)
        self.token = token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_successful_stats_update(self):
        response = self.client.put('/updateStats/', {"coins": 10, "distance": 5, "xp": 20}, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.coins, 10)
        self.assertEqual(self.user.distance, 5)
        self.assertEqual(self.user.xp, 20)

    def test_no_stats_update(self):
        response = self.client.put('/updateStats/', {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.coins, 0)
        self.assertEqual(self.user.distance, 0)
        self.assertEqual(self.user.xp, 0)

    def test_unauthorized_stats_update(self):
        client = APIClient()
        response = client.put('/updateStats/', {'coins': 10, 'distance': 5, 'xp': 20}, format='json')
        self.assertEqual(response.status_code, 401)