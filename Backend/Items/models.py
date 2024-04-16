from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    stock_number = models.IntegerField()
    real_price = models.DecimalField(max_digits=6, decimal_places=2)
    game_currency_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_picture_id = models.IntegerField()

    def __str__(self):
        return str(self.id)


class ItemPurchased(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)
