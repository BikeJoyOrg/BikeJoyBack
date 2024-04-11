import base64
import os

from django.conf import settings
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    item_picture = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Item
        fields = ('id', 'stock_number', 'real_price', 'game_currency_price', 'item_picture')

    def get_image(self, obj):
        if obj.item_picture:
            with open(os.path.join(settings.MEDIA_ROOT, obj.item_picture.path), 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        else:
            return None
