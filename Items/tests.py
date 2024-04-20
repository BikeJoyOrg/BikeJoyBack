"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from .models import Item, ItemPurchased
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass')


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    title = "Test Item"
    description = "Description of Test Item"
    stock_number = 5
    real_price = 100
    game_currency_price = 50
    item_picture_id = 1


class TestItemViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.item = ItemFactory()
        self.list_url = reverse('list_items')
        self.purchase_url = lambda item_id: reverse('purchase_item', kwargs={'item_id': item_id})

    def test_list_items_shows_only_in_stock(self):
        # Creating items with different stock numbers
        ItemFactory(stock_number=0)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return items with stock_number > 0
        self.assertEqual(len(response.data), 1)

    def test_purchase_item_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.purchase_url(self.item.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = Item.objects.get(id=self.item.id)
        self.assertEqual(item.stock_number, 4)  # Stock should decrease by 1

    def test_purchase_item_out_of_stock(self):
        self.item.stock_number = 0
        self.item.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.purchase_url(self.item.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_purchase_item_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.purchase_url(999))  # Assuming 999 is a non-existent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_purchase_item_unauthenticated(self):
        response = self.client.post(self.purchase_url(self.item.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
"""