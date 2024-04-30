from Users.models import CustomUser
from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=48)
    description = models.TextField()
    stock_number = models.IntegerField()
    real_price = models.PositiveIntegerField()
    game_currency_price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/', null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ItemPurchased(models.Model):
    id = models.AutoField(primary_key=True)
    item_title = models.CharField(max_length=48)
    item_purchased_price = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)
