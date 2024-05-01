from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Agrega tus campos adicionales aquí. Por ejemplo:
    #campo_extra1 = models.CharField(max_length=100, default='valor predeterminado')
    coins = models.IntegerField(default=0)
    distance = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
