import base64
import os

from django.conf import settings
from rest_framework import serializers
from .models import Item, ItemPurchased


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemPurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPurchased
        fields = "__all__"
