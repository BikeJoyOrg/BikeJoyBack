from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from Users.models import CustomUser
from .models import Item, ItemPurchased
import factory

from .serializers import ItemSerializer


class ListItemsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear item list
        self.item1 = Item.objects.create(
            title='Item 1',
            description='Description 1',
            stock_number=5,
            real_price=10,
            game_currency_price=100,
        )
        self.item2 = Item.objects.create(
            title='Item 2',
            description='Description 2',
            stock_number=0,
            real_price=15,
            game_currency_price=150,
        )
        self.item3 = Item.objects.create(
            title='Item 3',
            description='Description 3',
            stock_number=10,
            real_price=20,
            game_currency_price=200,
        )

    def test_list_items(self):
        # Solicitud GET
        response = self.client.get('/items/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Verifica clau 'items' a la resposta
        self.assertIn('items', data)

        # Obtenim la llista
        items_list = data['items']

        # Verifiquem que es retornin els 2 items amb stock
        self.assertEqual(len(items_list), 2)

        # Verifiquem que els items retornats siguin els correctes
        serializer = ItemSerializer([self.item1, self.item3], many=True)
        self.assertEqual(items_list, serializer.data)


class PurchaseItemTest(TestCase):
    def setUp(self):
        # Configurem user i token per fer la crida
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', coins=1000)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Creem item per la prova
        self.item = Item.objects.create(
            title='test_item',
            description='abcd',
            stock_number=10,
            real_price=10,
            game_currency_price=100,
        )

    def test_purchase_item(self):
        # Solicitud POST
        response = self.client.post(f'/items/purchase/{self.item.id}/')

        # Verificació del codi de resposta
        self.assertEqual(response.status_code, 200)

        # Verificació del tipus de l'usuari
        self.assertIsInstance(self.user, CustomUser)

        # Verifiquem que s'hagi realitzat la compra
        self.item.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.item.stock_number, 9)
        self.assertEqual(self.user.coins, 1000 - self.item.game_currency_price)

        # Verifiquem que s'hagi creat un ItemPurchased
        self.assertTrue(ItemPurchased.objects.filter(user=self.user, item=self.item).exists())
