from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from Users.models import CustomUser
import factory
from .models import Mascota, MascotaAconseguida

from .serializers import MascotaSerializer, MascotaAconseguidaSerializer

class ListPetsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear pet list
        self.mascota1 = Mascota.objects.create(
            name='Mascota 1',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )
        self.item2 = Mascota.objects.create(
            name='Mascota 2',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )
        self.item3 = Mascota.objects.create(
            name='Mascota 3',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )

    def test_list_pets(self):
        # Solicitud GET
        response = self.client.get('/pets/getMascotas/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Obtenim la llista
        pets_list = data

        # Verifiquem que es retornin les 3 mascotes
        self.assertEqual(len(pets_list), 3)

        pets = Mascota.objects.all()

        # Verifiquem que les mascotes retornades siguin les correctes
        serializer = MascotaSerializer(pets, many=True)
        self.assertEqual(pets_list, serializer.data)

    def test_get_pet(self):
        # Solicitud GET
        response = self.client.get(f'/pets/getMascota/{self.mascota1.name}/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Verifiquem que la mascota retornada sigui la correcta
        self.assertEqual(data, MascotaSerializer(self.mascota1).data)



class AdquirirMascotaTest(TestCase):
    def setUp(self):
        # Configurem user i token per fer la crida
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Creem pet per la prova
        self.pet = Mascota.objects.create(
            name='Mascota 1',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )

    def test_adquirir_mascota(self):
        # Solicitud POST
        response = self.client.post(f'/pets/createMascotaAconseguida/{self.pet.name}/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        # Verificació del tipus de l'usuari
        self.assertIsInstance(self.user, CustomUser)

        # Verifiquem que s'hagi creat un ItemPurchased
        self.assertTrue(MascotaAconseguida.objects.filter(
            nomMascota=self.pet,
            nicknameUsuari=self.user,
        ).exists())

class GetPetsUsuariTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.pet1 = Mascota.objects.create(
            name='Mascota 1',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )
        self.pet2 = Mascota.objects.create(
            name='Mascota 2',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )
        self.pet3 = Mascota.objects.create(
            name='Mascota 3',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )

        self.pet1A = MascotaAconseguida.objects.create(
            nomMascota=self.pet1,
            nicknameUsuari=self.user,
            nivell=1,
            equipada=False,
        )
        self.pet2A = MascotaAconseguida.objects.create(
            nomMascota=self.pet2,
            nicknameUsuari=self.user,
            nivell=1,
            equipada=False,
        )

    def test_get_pets_usuari(self):
# Solicitud GET
        response = self.client.get('/pets/getMascotasAconseguidesUsuari/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Obtenim la llista de mascotes aconseguides
        pets_list = data

class EquiparMascotaTest(TestCase):
    def setUp(self):
        # Configurem user i token per fer la crida
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Creem pet per la prova
        self.pet = Mascota.objects.create(
            name='Mascota 1',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )

        # Creem pet aconseguida per la prova
        self.petA = MascotaAconseguida.objects.create(
            nomMascota=self.pet,
            nicknameUsuari=self.user,
            nivell=1,
            equipada=False,
        )

    def test_equipar_mascota(self):
        # Solicitud PATCH
        response = self.client.patch(f'/pets/equiparMascota/{self.pet.name}/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        # Verifiquem que la mascota estigui equipada
        self.assertTrue(MascotaAconseguida.objects.get(nomMascota=self.pet, nicknameUsuari=self.user).equipada)

class LvlUpTest(TestCase):
    def setUp(self):
        # Configurem user i token per fer la crida
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Creem pet per la prova
        self.pet = Mascota.objects.create(
            name='Mascota 1',
            imgEgg='a',
            imgEggl='a',
            img1='a',
            img1l='a',
            img2='a',
            img2l='a',
            img3='a',
            img3l='a',
            bonus1=1,
            bonus2=2,
            bonus3=3,
        )

        # Creem pet aconseguida per la prova
        self.petA = MascotaAconseguida.objects.create(
            nomMascota=self.pet,
            nicknameUsuari=self.user,
            nivell=1,
            equipada=False,
        )

    def test_lvl_up(self):
        # Solicitud PATCH
        response = self.client.patch(f'/pets/lvlUp/{self.pet.name}/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        # Verifiquem que el nivell de la mascota hagi augmentat
        self.assertEqual(MascotaAconseguida.objects.get(nomMascota=self.pet, nicknameUsuari=self.user).nivell, 2)