from django.db import models


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    stock_number = models.IntegerField()
    real_price = models.DecimalField(max_digits=6, decimal_places=2)
    game_currency_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_picture = models.ImageField(upload_to='items/')

    def __str__(self):
        return str(self.id)
