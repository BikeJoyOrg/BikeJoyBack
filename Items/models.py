from Users.models import CustomUser
from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=48)
    description = models.TextField()
    stock_number = models.IntegerField()
    real_price = models.PositiveIntegerField()
    game_currency_price = models.PositiveIntegerField()
    item_picture_id = models.PositiveSmallIntegerField()



    def __str__(self):
        return str(self.id)


class ItemPurchased(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)