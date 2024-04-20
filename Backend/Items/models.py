from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    stock_number = models.IntegerField()
    real_price = models.PositiveIntegerField()
    game_currency_price = models.PositiveIntegerField()
    item_picture_id = models.PositiveSmallIntegerField()
    description = models.TextField()
    title = models.CharField(max_length=24)

    def __str__(self):
        return str(self.id)
