from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

from Users.models import CustomUser
from .models import Item, ItemPurchased
import factory

from .serializers import ItemSerializer, ItemPurchasedSerializer


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
        self.assertTrue(ItemPurchased.objects.filter(
            user=self.user,
            item_title=self.item.title,
            item_purchased_price=self.item.game_currency_price
        ).exists())


class ListPurchasedItemsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', coins=1000)
        self.item_purchased1 = ItemPurchased.objects.create(
            item_title='Item 1',
            item_purchased_price=10,
            user=self.user,
        )
        self.item_purchased2 = ItemPurchased.objects.create(
            item_title='Item 2',
            item_purchased_price=15,
            user=self.user,
        )
        self.item_purchased3 = ItemPurchased.objects.create(
            item_title='Item 3',
            item_purchased_price=20,
            user=self.user,
        )

    def test_list_purchased_items(self):
        # Solicitud GET
        response = self.client.get(f'/user/purchases/{self.user.id}/')

        # Verificació status resposta
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Comprobació clau 'purchased_items' a la resposta
        self.assertIn('purchased_items', data)

        # Comprovar que es retornin els 3 items comprats
        purchased_items_list = data['purchased_items']
        self.assertEqual(len(purchased_items_list), 3)
        serializer = ItemPurchasedSerializer([self.item_purchased1, self.item_purchased2, self.item_purchased3],
                                             many=True)
        self.assertEqual(purchased_items_list, serializer.data)
